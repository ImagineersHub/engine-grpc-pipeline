from engine_grpc import UEGI, GI
from compipe.runtime_env import Environment
from compipe.utils.io_helper import json_loader
import os
import sys
from ugrpc_pipe import FloatArrayRep, GenericResp
import asyncio
from grpclib.client import Channel
from engine_grpc.engine_pipe_impl import BaseEngineImpl
from engine_grpc.engine_pipe_server import run_grpc_server
from engine_grpc.utils.sys_process import kill_process_by_name, get_process_name_lists

from google.protobuf.any_pb2 import Any
from google.protobuf.json_format import MessageToDict


# initialize env and append server config from local json
server_config_path = os.path.join(
    os.path.dirname(__file__), 'debug_runtime_config.json')
server_config = json_loader(
    path=server_config_path).get(sys.platform or 'win32')
Environment.append_server_config(payload=server_config)


if __name__ == "__main__":

    run_grpc_server()

    # result = UEGI().command_parser(
    #     cmd=GI.method_runtime_fetch_scene_hierarchy,
    #     params=[], timeout=3.0)
    # print(result.status)

    # print(result.payload)

    # print(UEI().quit_without_saving())

    # print(get_process_name_lists())

    # kill_process_by_name('Unity.exe')

# Create a channel
# channel = Channel(host='localhost', port=50051)


# async def make_request():
#     # Make a request with a timeout
#     response = await channel.request(
#         service='UGrpcPipe',
#         method='CommandParser',
#         message=my_message,
#         timeout=1.0  # timeout in seconds
#     )
#     return response

# # Get the event loop
# event_loop = asyncio.get_event_loop()

# # Run the coroutine until it completes
# response = event_loop.run_until_complete(make_request())
