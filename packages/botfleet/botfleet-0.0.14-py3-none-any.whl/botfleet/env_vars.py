import os
from enum import Enum

PRIVATE_ENV_VAR_PREFIX = "__BOTFLEET__"
PAYLOAD_ROOT_KEY = "root"


def get_private_env_var(name, default=None):
    return os.getenv(PRIVATE_ENV_VAR_PREFIX + name, default)


class EnvVar(Enum):
    PAYLOAD = "PAYLOAD"
    DATASTORE_PROXY_URL = "DATASTORE_PROXY_URL"
    EXECUTION_ENVIRONMENT = "EXECUTION_ENVIRONMENT"
    SCHEDULED = "SCHEDULED"
