"""
Transport/protocol layer to extend ftd2xx for asyncronous connections.
"""
from .aio import create_ftd2xx_connection

__version__ = "0.1.0"

__all__ = ["create_ftd2xx_connection"]
