from engine_grpc import UEI, GI
from compipe.runtime_env import Environment
from compipe.utils.io_helper import json_loader
import os
import sys

# initialize env and append server config from local json
server_config_path = os.path.join(os.path.dirname(__file__), 'debug_runtime_config.json')
server_config = json_loader(path=server_config_path).get(sys.platform or 'win32')
Environment.append_server_config(payload=server_config)


if __name__ == "__main__":
    result = UEI().find_assets(filter="t:prefab", paths=["Assets/Content/HKG/Dev/Case0011/model"])

    print(result)
