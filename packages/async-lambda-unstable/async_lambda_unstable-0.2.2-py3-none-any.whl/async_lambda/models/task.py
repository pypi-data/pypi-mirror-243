from enum import Enum
from typing import Any, Callable, Generic, List, Optional, TypeVar, Union

from .. import env
from ..build_config import get_build_config_for_task
from ..config import config
from .events.managed_sqs_event import ManagedSQSEvent
from .events.scheduled_event import ScheduledEvent
from .events.unmanaged_sqs_event import UnmanagedSQSEvent


class TaskTriggerType(Enum):
    MANAGED_SQS = 1
    UNMANAGED_SQS = 2
    SCHEDULED_EVENT = 3
    API_EVENT = 4


EventType = TypeVar(
    "EventType", bound=Union[ManagedSQSEvent, ScheduledEvent, UnmanagedSQSEvent]
)


class AsyncLambdaTask(Generic[EventType]):
    task_id: str
    trigger_type: TaskTriggerType
    trigger_config: dict

    timeout: int
    memory: int
    ephemeral_storage: int

    executable: Callable[[EventType], Any]

    def __init__(
        self,
        executable: Callable[[EventType], Any],
        task_id: str,
        trigger_type: TaskTriggerType,
        trigger_config: Optional[dict] = None,
        timeout: int = 60,
        memory: int = 128,
        ephemeral_storage: int = 512,
    ):
        AsyncLambdaTask.validate_task_id(task_id)
        self.executable = executable
        self.task_id = task_id
        self.trigger_type = trigger_type
        self.trigger_config = trigger_config if trigger_config is not None else dict()
        self.timeout = timeout
        self.memory = memory
        self.ephemeral_storage = ephemeral_storage

    @staticmethod
    def validate_task_id(task_id: str):
        if not task_id.isalnum():
            raise ValueError("Task ID must contain only A-Za-z0-9")
        if len(task_id) > 60:
            raise ValueError("Task ID must be less than 60 characters long.")

    def get_managed_queue_name(self):
        """
        Returns the managed queue's name for this task.
        """
        if self.trigger_type != TaskTriggerType.MANAGED_SQS:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"{config.name}-{self.task_id}"

    def get_function_name(self):
        return f"{config.name}-{self.task_id}"

    def get_managed_queue_arn(self):
        if self.trigger_type != TaskTriggerType.MANAGED_SQS:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"arn:aws:sqs:{env.get_aws_region()}:{env.get_aws_account_id()}:{self.get_managed_queue_name()}"

    def get_managed_queue_url(self):
        if self.trigger_type != TaskTriggerType.MANAGED_SQS:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"https://sqs.{env.get_aws_region()}.amazonaws.com/{env.get_aws_account_id()}/{self.get_managed_queue_name()}"

    def get_function_logical_id(self):
        return f"{self.task_id}ALFunc"

    def get_managed_queue_logical_id(self):
        if self.trigger_type != TaskTriggerType.MANAGED_SQS:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"{self.task_id}ALQueue"

    def get_template_events(self):
        if self.trigger_type == TaskTriggerType.MANAGED_SQS:
            return {
                f"ManagedSQSQueueEvent{self.task_id}": {
                    "Type": "SQS",
                    "Properties": {
                        "BatchSize": 1,
                        "Enabled": True,
                        "Queue": {
                            "Fn::GetAtt": [
                                self.get_managed_queue_logical_id(),
                                "Arn",
                            ]
                        },
                    },
                }
            }
        elif self.trigger_type == TaskTriggerType.UNMANAGED_SQS:
            return {
                f"UnmanagedSQSQueueEvent{self.task_id}": {
                    "Type": "SQS",
                    "Properties": {
                        "BatchSize": 1,
                        "Enabled": True,
                        "Queue": self.trigger_config["queue_arn"],
                    },
                }
            }
        elif self.trigger_type == TaskTriggerType.SCHEDULED_EVENT:
            return {
                f"ScheduledEvent{self.task_id}": {
                    "Type": "ScheduleV2",
                    "Properties": {
                        "ScheduleExpression": self.trigger_config[
                            "schedule_expression"
                        ],
                    },
                }
            }
        elif self.trigger_type == TaskTriggerType.API_EVENT:
            return {
                f"APIEvent{self.task_id}": {
                    "Type": "Api",
                    "Properties": {
                        "Path": self.trigger_config["path"],
                        "Method": self.trigger_config["method"].lower(),
                        "RestApiId": {"Ref": "AsyncLambdaAPIGateway"},
                    },
                }
            }
        else:
            return {}

    def get_policy_sqs_resources(self):
        if self.trigger_type == TaskTriggerType.MANAGED_SQS:
            return [
                {
                    "Fn::GetAtt": [
                        self.get_managed_queue_logical_id(),
                        "Arn",
                    ]
                }
            ]
        elif self.trigger_type == TaskTriggerType.UNMANAGED_SQS:
            return [self.trigger_config["queue_arn"]]
        return []

    def get_sam_template(
        self,
        module: str,
        tasks: List["AsyncLambdaTask"],
        config_dict: dict,
        stage: Optional[str] = None,
    ) -> dict:
        build_config = get_build_config_for_task(config_dict, self.task_id, stage=stage)
        events = self.get_template_events()
        policy_sqs_resources = self.get_policy_sqs_resources()

        policy_statements = [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:DeleteObject",
                    "s3:PutObject",
                    "s3:GetObject",
                ],
                "Resource": {
                    "Fn::Join": [
                        "",
                        [
                            "arn:aws:s3:::",
                            {"Ref": "AsyncLambdaPayloadBucket"},
                            "/*",
                        ],
                    ]
                },
            },
            {
                "Effect": "Allow",
                "Action": ["sqs:SendMessage"],
                "Resource": [
                    {
                        "Fn::GetAtt": [
                            _task.get_managed_queue_logical_id(),
                            "Arn",
                        ]
                    }
                    for _task in tasks
                    if _task.trigger_type == TaskTriggerType.MANAGED_SQS
                ],
            },
        ]
        if len(policy_sqs_resources) > 0:
            policy_statements.append(
                {
                    "Effect": "Allow",
                    "Action": [
                        "sqs:ChangeMessageVisibility",
                        "sqs:DeleteMessage",
                        "sqs:GetQueueAttributes",
                        "sqs:GetQueueUrl",
                        "sqs:ReceiveMessage",
                    ],
                    "Resource": policy_sqs_resources,
                },
            )
        function_properties = {}
        if len(build_config.layers) > 0:
            function_properties["Layers"] = list(build_config.layers)

        template = {
            self.get_function_logical_id(): {
                "Type": "AWS::Serverless::Function",
                "Properties": {
                    "Handler": f"{module}.handler",
                    "Runtime": config.runtime,
                    "Environment": {
                        "Variables": {
                            "ASYNC_LAMBDA_PAYLOAD_S3_BUCKET": {
                                "Ref": "AsyncLambdaPayloadBucket"
                            },
                            "ASYNC_LAMBDA_TASK_ID": self.task_id,
                            "ASYNC_LAMBDA_ACCOUNT_ID": {"Ref": "AWS::AccountId"},
                            **build_config.environment_variables,
                        }
                    },
                    "FunctionName": self.get_function_name(),
                    "CodeUri": ".async_lambda/build/deployment.zip",
                    "EphemeralStorage": {"Size": self.ephemeral_storage},
                    "MemorySize": self.memory,
                    "Timeout": self.timeout,
                    "Events": events,
                    "Policies": [
                        {"Statement": policy_statements},
                        *build_config.policy_arns,
                    ],
                    **function_properties,
                },
            }
        }

        if self.trigger_type == TaskTriggerType.MANAGED_SQS:
            template[self.get_managed_queue_logical_id()] = {
                "Type": "AWS::SQS::Queue",
                "Properties": {
                    "QueueName": self.get_managed_queue_name(),
                    "RedrivePolicy": {
                        "deadLetterTargetArn": {
                            "Fn::GetAtt": [
                                "AsyncLambdaDLQ",
                                "Arn",
                            ]
                        },
                        "maxReceiveCount": 1,
                    },
                    "VisibilityTimeout": self.timeout,
                },
            }
        return template

    def execute(self, event: EventType) -> Any:
        """
        Executes the tasks function
        """
        return self.executable(event)
