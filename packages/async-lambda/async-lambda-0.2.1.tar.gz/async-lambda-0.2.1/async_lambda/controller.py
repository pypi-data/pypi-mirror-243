import functools
import json
import logging
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

import boto3  # type: ignore

from . import env
from .build_config import get_build_config_for_stage
from .models.events.api_event import APIEvent
from .models.events.managed_sqs_event import ManagedSQSEvent
from .models.events.scheduled_event import ScheduledEvent
from .models.events.unmanaged_sqs_event import UnmanagedSQSEvent
from .models.mock.mock_context import MockLambdaContext
from .models.mock.mock_event import MockLambdaEvent
from .models.task import AsyncLambdaTask, TaskTriggerType

logger = logging.getLogger(__name__)


class AsyncLambdaController:
    sqs_client: Any
    tasks: Dict[str, AsyncLambdaTask]
    current_task_id: Optional[str] = None
    current_invocation_id: Optional[str] = None

    def __init__(self):
        self.sqs_client = boto3.client("sqs")
        self.tasks = dict()

    def add_task(self, task: AsyncLambdaTask):
        """
        Adds a task to the async lambda controller.
        """
        if task.task_id in self.tasks:
            raise Exception(
                f"A task with the task_id {task.task_id} already exists. DUPLICATE TASK IDS"
            )
        self.tasks[task.task_id] = task

    def generate_sam_template(
        self,
        module: str,
        config_dict: dict,
        stage: Optional[str] = None,
    ) -> dict:
        """
        Generates the SAM Template for this project.
        """
        template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Transform": "AWS::Serverless-2016-10-31",
            "Resources": {
                "AsyncLambdaPayloadBucket": {
                    "Type": "AWS::S3::Bucket",
                },
                "AsyncLambdaDLQ": {
                    "Type": "AWS::SQS::Queue",
                },
            },
        }
        _task_list = list(self.tasks.values())
        has_api_tasks = False
        for task in _task_list:
            if task.trigger_type == TaskTriggerType.API_EVENT:
                has_api_tasks = True
            for logical_id, resource in task.get_sam_template(
                module, _task_list, config_dict, stage
            ).items():
                template["Resources"][logical_id] = resource

        if has_api_tasks:
            build_config = get_build_config_for_stage(config_dict, stage)
            properties: dict = {"StageName": "prod"}
            if build_config.domain_name is not None:
                properties["Domain"] = {
                    "DomainName": build_config.domain_name,
                }
                if build_config.certificate_arn is not None:
                    properties["Domain"][
                        "CertificateArn"
                    ] = build_config.certificate_arn
                    if build_config.tls_version is not None:
                        properties["Domain"][
                            "SecurityPolicy"
                        ] = build_config.tls_version
            template["Resources"]["AsyncLambdaAPIGateway"] = {
                "Type": "AWS::Serverless::Api",
                "Properties": properties,
            }
        return template

    def set_current_task_id(self, task_id: str):
        """
        Set the current_task_id
        """
        self.current_task_id = task_id

    def set_current_invocation_id(self, invocation_id: str):
        """
        Set the current_invocation_id
        """
        self.current_invocation_id = invocation_id

    def handle_invocation(self, event, context, task_id: Optional[str] = None):
        """
        Direct the invocation to the task executor.
        """
        if task_id is None:
            task_id = env.get_current_task_id()
        task = self.tasks[task_id]

        if task.trigger_type == TaskTriggerType.MANAGED_SQS:
            _event = ManagedSQSEvent(event, context)
            self.set_current_invocation_id(_event.invocation_id)
        elif task.trigger_type == TaskTriggerType.UNMANAGED_SQS:
            _event = UnmanagedSQSEvent(event, context)
        elif task.trigger_type == TaskTriggerType.SCHEDULED_EVENT:
            _event = ScheduledEvent(event, context)
        elif task.trigger_type == TaskTriggerType.API_EVENT:
            _event = APIEvent(event, context)
        else:
            raise NotImplementedError(
                f"Trigger type of {task.trigger_type} is not supported."
            )
        return task.execute(_event)

    def async_invoke(
        self,
        destination_task_id: str,
        payload: Any,
        delay: Optional[int] = None,
        force_sync: bool = False,
    ):
        """
        Invoke an 'async-lambda' task asynchronously utilizing it's SQS queue
        """
        if destination_task_id not in self.tasks:
            raise Exception(
                f"No such task exists with the task_id {destination_task_id}"
            )
        destination_task = self.tasks[destination_task_id]
        if destination_task.trigger_type != TaskTriggerType.MANAGED_SQS:
            raise Exception(
                f"Unable to invoke task '{destination_task_id}' because it is a {destination_task.trigger_type} task"
            )
        if self.current_invocation_id is None:
            invocation_id = str(uuid4())
        else:
            invocation_id = self.current_invocation_id

        sqs_payload = json.dumps(
            {
                "source_task_id": self.current_task_id,
                "destination_task_id": destination_task_id,
                "invocation_id": invocation_id,
                "payload": json.dumps(payload),
            }
        )
        if force_sync or env.get_force_sync_mode():
            # Sync invocation with mock event/context
            mock_event = MockLambdaEvent(sqs_payload)
            mock_context = MockLambdaContext(destination_task.task_id)
            return self.handle_invocation(
                mock_event, mock_context, task_id=destination_task_id
            )
        else:
            # Encode/Send payload over sqs
            self.sqs_client.send_message(
                QueueUrl=destination_task.get_managed_queue_url(),
                MessageBody=sqs_payload,
                DelaySeconds=delay,
            )


controller = AsyncLambdaController()


def async_invoke(
    task_id: str, payload: Any, delay: Optional[int] = 0, force_sync: bool = False
):
    """
    Invoke an Async-Lambda task.
    """
    controller.async_invoke(
        destination_task_id=task_id, payload=payload, delay=delay, force_sync=force_sync
    )


def async_lambda_handler(event, context):
    """
    The handler invoked by Lambda.
    """
    controller.handle_invocation(event, context, task_id=None)


def async_task(task_id: str, **kwargs):
    """
    Decorate a function to register it as an async task.
    These functions can be asynchronously invoked with the `async_invoke` function
    via their `task_id`.
    """
    logger.debug(f"Registering async task '{task_id}' with the controller.")

    def _task(func: Callable[[ManagedSQSEvent], Any]):
        controller.add_task(
            AsyncLambdaTask(
                executable=func,
                task_id=task_id,
                trigger_type=TaskTriggerType.MANAGED_SQS,
                **kwargs,
            )
        )

        @functools.wraps
        def inner(*args, **kwargs):
            controller.set_current_task_id(task_id)
            return func(*args, **kwargs)

        return inner

    return _task


def sqs_task(task_id: str, queue_arn: str, **kwargs):
    """
    Decorate a function to register it as an SQS task.
    These tasks will be triggered by messages in the given queue.
    """
    logger.debug(
        f"Registering sqs task '{task_id}' arn '{queue_arn}' with the controller."
    )

    def _task(func: Callable[[UnmanagedSQSEvent], Any]):
        controller.add_task(
            AsyncLambdaTask(
                executable=func,
                task_id=task_id,
                trigger_type=TaskTriggerType.UNMANAGED_SQS,
                trigger_config={"queue_arn": queue_arn},
                **kwargs,
            )
        )

        @functools.wraps
        def inner(*args, **kwargs):
            controller.set_current_task_id(task_id)
            return func(*args, **kwargs)

        return inner

    return _task


def scheduled_task(task_id: str, schedule_expression: str, **kwargs):
    """
    Decorate a function to register it as a scheduled task.
    These tasks will be triggered by the given schedule expression.
    """
    logger.debug(
        f"Registering scheduled task '{task_id}' with schedule '{schedule_expression}' with the controller."
    )

    def _task(func: Callable[[ScheduledEvent], Any]):
        controller.add_task(
            AsyncLambdaTask(
                executable=func,
                task_id=task_id,
                trigger_type=TaskTriggerType.SCHEDULED_EVENT,
                trigger_config={"schedule_expression": schedule_expression},
                **kwargs,
            )
        )

        @functools.wraps
        def inner(*args, **kwargs):
            controller.set_current_task_id(task_id)
            return func(*args, **kwargs)

        return inner

    return _task


def api_task(task_id: str, path: str, method: str, **kwargs):
    """
    Decorate a function to register it as an API task.
    These tasks will be triggered by an API call.
    """
    logger.debug(
        f"Registering api task '{task_id}' with the path '{path}' and method '{method}' with the controller."
    )

    def _task(func: Callable[[APIEvent], Any]):
        controller.add_task(
            AsyncLambdaTask(
                executable=func,
                task_id=task_id,
                trigger_type=TaskTriggerType.API_EVENT,
                trigger_config={"path": path, "method": method},
                **kwargs,
            )
        )

        @functools.wraps
        def inner(*args, **kwargs):
            controller.set_current_task_id(task_id)
            return func(*args, **kwargs)

        return inner

    return _task
