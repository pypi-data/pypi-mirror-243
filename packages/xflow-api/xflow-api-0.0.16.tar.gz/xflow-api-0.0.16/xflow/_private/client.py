import sys
import os
import requests
import traceback
import json

from pydantic import BaseModel, Extra

this = sys.modules[__name__]


class ClientInformation(BaseModel):
    xflow_server_url: str
    project: str
    user: str
    is_init: bool = False
    component_path: str = "/api/component"
    pipeline_path: str = "/api/pipeline"

    class Config:
        extra = Extra.forbid


def init():
    if os.getenv("SERVER_MODE") == "True":
        print("no need to init xflow on server.")
        return
    if hasattr(this, "client_info"):
        if this.client_info.is_init:
            return
    try:
        with open("/etc/xflow/config.json", 'r') as conf_file:
            conf_data = json.load(conf_file)
    except Exception as exc:
        raise RuntimeError(f"can't load client configuration: {exc.__str__()}")
    else:
        xflow_server_url = ''
        service_discovery_url = conf_data["WB_SERVER_URL"] + "/api/service?name=xflow"
        res = requests.get(url=service_discovery_url, verify=False)
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "00":
                xflow_server_url = res.json().get("URL")
        if xflow_server_url == '':
            raise InitError("can't find xflow server")
        this.client_info = ClientInformation(xflow_server_url=xflow_server_url,
                                             project=conf_data["PRJ_ID"],
                                             user=conf_data["USER_ID"],
                                             is_init=True)


class InitError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.traceback = traceback.format_exc()


def init_check() -> None:
    if hasattr(this, "client_info"):
        if not this.client_info.is_init:
            init()
            # raise RuntimeError("xflow didn't initiated. call xflow.init() before using xflow")
    else:
        init()
        # raise RuntimeError("xflow didn't initiated. call xflow.init() before using xflow")
