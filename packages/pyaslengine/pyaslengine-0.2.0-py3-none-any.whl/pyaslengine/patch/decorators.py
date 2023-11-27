"""pyaslengine.patch.decorators"""
import pdb

from pyaslengine.exceptions import StatePatchBail
from pyaslengine.log import get_logger

logger = get_logger(__name__)


def observe(func):
    def wrapper(*args, **kwargs):
        _ = func(*args, **kwargs)
        return args[1:]  # remove self arg

    return wrapper


def pdb_debug(func):
    def wrapper(*args, **kwargs):
        pdb.set_trace()
        return args[1:]  # remove self arg

    return wrapper


def bail(func):
    def wrapper(*args, **kwargs):
        _ = func(*args, **kwargs)
        raise StatePatchBail()

    return wrapper
