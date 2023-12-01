import os


def is_build_mode() -> bool:
    return bool(os.environ.get("ASYNC_LAMBDA_BUILD_MODE", False))


def get_aws_region() -> str:
    return os.environ.get("AWS_REGION", "local")


def get_aws_account_id() -> str:
    return os.environ.get("ASYNC_LAMBDA_ACCOUNT_ID", "localaccount")


def get_current_task_id() -> str:
    return os.environ["ASYNC_LAMBDA_TASK_ID"]


def get_force_sync_mode() -> bool:
    return bool(os.environ.get("ASYNC_LAMBDA_FORCE_SYNC", ""))
