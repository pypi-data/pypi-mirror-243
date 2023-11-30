import requests
import json

from xflow._utils.component import Component, ComponentTypeCode
from xflow._utils.decorators import client_method
from xflow._private.request_vo import GetComponent
import xflow._private.client as xflow_client


@client_method
def create_component(name: str, func: callable, description: str = '') -> Component:
    xflow_client.init_check()
    client_info: xflow_client.ClientInformation = xflow_client.client_info
    url = client_info.xflow_server_url + client_info.component_path + f"?name={name}"
    try:
        response = requests.get(url=url)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("can't connect to xflow server")
    else:
        if response.status_code == 200:
            print(response)
    # check component is already exist
    return Component(name=name,
                     func=func,
                     desc=description,
                     component_type=ComponentTypeCode.DATA)


@client_method
def get_component(name: str, revision: int = None) -> Component:
    body = GetComponent(CMPNT_NM=name,
                        CMPNT_RVSN=revision)
