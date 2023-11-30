from storedict import create_store

from .env_vars import EnvVar, get_private_env_var
from .request import Request

__version__ = "0.0.18"

store = create_store(get_private_env_var(EnvVar.DATASTORE_PROXY_URL.value))
request = Request()
