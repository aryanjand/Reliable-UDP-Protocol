import pickle
from typing import TypeVar

T = TypeVar("T")


def serialize(obj: T) -> bytes:
    """
    Serialize an object into bytes using pickle.

    Args:
    - obj: The object to serialize.

    Returns:
    - bytes: The serialized object as bytes.
    """
    return pickle.dumps(obj)


def deserialize(data: bytes) -> T:
    """
    Deserialize bytes into an object using pickle.

    Args:
    - data: The serialized bytes.

    Returns:
    - obj: The deserialized object.
    """
    return pickle.loads(data)
