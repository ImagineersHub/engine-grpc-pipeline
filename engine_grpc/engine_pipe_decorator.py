import wrapt

from compipe.runtime_env import Environment as env
from compipe.utils.logging import logger
from inspect import signature, _empty

from .engine_pipe_abstract import EngineAbstract
from .engine_pipe_channel import general_channel
from ugrpc_pipe import GenericResp
from betterproto import Message


def grpc_call_general(channel: str = None):
    """
    """
    @wrapt.decorator
    def wrapper(wrapped, engine_impl: EngineAbstract, args, kwds):
        """Simplifies the creation of grpc channels and facilitates the marking of grpc command interfaces
        """
        with general_channel(engine=engine_impl, channel=channel):
            resp = wrapped(**kwds)
            # check the status code if the resp is an instance of GenericResp
            if hasattr(resp, 'status') and resp.status:
                logger.error(resp.status.message)
                logger.error(kwds)

            return resp

    return wrapper
