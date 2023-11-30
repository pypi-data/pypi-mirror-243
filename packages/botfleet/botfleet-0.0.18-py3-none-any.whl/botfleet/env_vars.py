import os
from enum import Enum

PRIVATE_ENV_VAR_PREFIX = "__BOTFLEET__"
EMPTY_SCRIPT_PAYLOAD_VALUE = None


def get_private_env_var(name, default=None):
    return os.getenv(PRIVATE_ENV_VAR_PREFIX + name, default)


class EnvVar(Enum):
    SCRIPT_PAYLOAD = "SCRIPT_PAYLOAD"
    DATASTORE_PROXY_URL = "DATASTORE_PROXY_URL"
    EXECUTION_ENVIRONMENT = "EXECUTION_ENVIRONMENT"
    SCHEDULED = "SCHEDULED"
