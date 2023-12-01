from dataclasses import dataclass
from typing import Dict, Optional, Set


@dataclass
class AsyncLambdaBuildConfig:
    environment_variables: Dict[str, str]
    policy_arns: Set[str]
    layers: Set[str]
    domain_name: Optional[str] = None
    tls_version: Optional[str] = None
    certificate_arn: Optional[str] = None

    @classmethod
    def new(cls, config: dict) -> "AsyncLambdaBuildConfig":
        return cls(
            policy_arns=set(config.get("policy_arns", set())),
            environment_variables=config.get("environment_variables", dict()),
            layers=set(config.get("layers", set())),
            domain_name=config.get("domain_name"),
            tls_version=config.get("tls_version"),
            certificate_arn=config.get("certificate_arn"),
        )

    def merge(self, other: "AsyncLambdaBuildConfig"):
        self.policy_arns.update(other.policy_arns)
        self.environment_variables.update(other.environment_variables)
        self.layers.update(other.layers)
        if other.domain_name is not None:
            self.domain_name = other.domain_name
        if other.tls_version is not None:
            self.tls_version = other.tls_version
        if other.certificate_arn is not None:
            self.certificate_arn = other.certificate_arn


def get_build_config_for_stage(
    config: dict, stage: Optional[str] = None
) -> AsyncLambdaBuildConfig:
    build_config = AsyncLambdaBuildConfig.new(config)
    if stage is not None:
        # Apply Stage Defaults
        stage_config = config.setdefault("stages", {}).setdefault(stage, {})
        build_config.merge(AsyncLambdaBuildConfig.new(stage_config))

    return build_config


def get_build_config_for_task(
    config: dict, task_id: str, stage: Optional[str] = None
) -> AsyncLambdaBuildConfig:
    # Apply Defaults
    build_config = get_build_config_for_stage(config, stage)

    if task_id in config.setdefault("tasks", {}):
        # Apply task defaults
        task_config = config["tasks"].setdefault(task_id, {})
        build_config.merge(AsyncLambdaBuildConfig.new(task_config))

        if stage is not None:
            # Apply task stage defaults
            task_stage_config = task_config.setdefault("stages", {}).setdefault(
                stage, {}
            )
            build_config.merge(AsyncLambdaBuildConfig.new(task_stage_config))

    return build_config
