import os
import json


class Request:
    def __init__(self):
        self.payload = json.loads(os.environ["__BOTFLEET__PAYLOAD"])
