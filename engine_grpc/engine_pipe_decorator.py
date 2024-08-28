

import wrapt
from compipe.utils.logging import logger
from compipe.utils.singleton import Singleton

from .engine_pipe_abstract import EngineAbstract
from .engine_pipe_channel import general_channel, GrpcChannelConfig


class GrpcCacheConfig(metaclass=Singleton):
    channel: str = None


def grpc_call_general(channel: str = None):
    """
    """
    @wrapt.decorator
    def wrapper(wrapped, engine_impl: EngineAbstract, args, kwds):
        """Simplifies the creation of grpc channels and facilitates the marking of grpc command interfaces
        """
        max_tries = 1
        while max_tries < 4:
            try:
                with general_channel(engine=engine_impl, channel=GrpcCacheConfig().channel or channel):
                    resp = wrapped(**kwds)
                    # check the status code if the resp is an instance of GenericResp
                    if hasattr(resp, 'status') and resp.status.code != 0:
                        logger.error(resp.status.message)
                        logger.error(kwds)

                    return resp
            except Exception as e:
                initial_channel = GrpcChannelConfig.retrieve_grpc_cfg(
                    engine=engine_impl.engine_platform)
                host, port_str = initial_channel.channel.split(':')
                port = int(port_str)
                GrpcCacheConfig().channel = f"{host}:{port+max_tries}"
                max_tries += 1
                if max_tries == 0:
                    logger.error(
                        f"Failed to connect to the channel {host}:{port}")
                    raise e

    return wrapper
