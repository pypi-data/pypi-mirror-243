import json

from .env_vars import EMPTY_SCRIPT_PAYLOAD_VALUE, EnvVar, get_private_env_var


class Request:
    def __init__(self):
        # User in a dev environment must get production=False, scheduled=False
        # and payload=EMPTY_SCRIPT_PAYLOAD_VALUE.
        self.production = (
            get_private_env_var(EnvVar.EXECUTION_ENVIRONMENT.value) == "production"
        )
        self.scheduled = get_private_env_var(EnvVar.SCHEDULED.value) == "True"

        payload = get_private_env_var(EnvVar.SCRIPT_PAYLOAD.value)
        self.payload = (
            EMPTY_SCRIPT_PAYLOAD_VALUE if payload is None else json.loads(payload)
        )
