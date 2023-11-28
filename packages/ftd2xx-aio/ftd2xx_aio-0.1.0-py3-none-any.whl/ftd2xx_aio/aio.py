#
# Parts of this code are inspired by or directly copied from the work of the
# pyserial team (pyserial-asyncio) which is under BSD3 license.
# Project Homepage: https://github.com/pyserial/pyserial-asyncio
#

from typing import Union, Callable
import sys
import asyncio
import ftd2xx as ftd
import ftd2xx.defines as ft_defs

from .transports import FTD2xxTransport


async def create_ftd2xx_connection(
    loop: asyncio.AbstractEventLoop,
    protocol_factory: Callable,
    dev_id: Union[int, bytes] = 0,
    flags: ft_defs.OpenExFlags = ft_defs.OPEN_BY_SERIAL_NUMBER,
):
    """Create a connection to a new ftd2xx instance.
    This function is a coroutine which will try to establish the
    connection.
    The chronological order of the operation is:
    1. protocol_factory is called without arguments and must return
       a protocol instance.
    2. The protocol instance is tied to the transport
    3. This coroutine returns successfully with a (transport,
       protocol) pair.
    4. The connection_made() method of the protocol
       will be called at some point by the event loop.
    Note:  protocol_factory can be any kind of callable, not
    necessarily a class. For example, if you want to use a pre-created
    protocol instance, you can pass lambda: my_protocol.
    Any additional arguments will be forwarded to open() or openEx() to create
    an FTD2XX instance.
    """

    async def create_tp_pair():
        if isinstance(dev_id, int):
            if sys.platform == "win32" and flags == ft_defs.OPEN_BY_LOCATION:
                ftd2xx_instance = ftd.openEx(dev_id, ft_defs.OpenExFlags(flags))
            else:
                ftd2xx_instance = ftd.open(dev_id)
        else:
            ftd2xx_instance = ftd.openEx(dev_id, ft_defs.OpenExFlags(flags))

        protocol = protocol_factory()

        return FTD2xxTransport(loop, protocol, ftd2xx_instance), protocol

    return await create_tp_pair()


async def open_ftd2xx_connection(*, loop=None, limit=None, **kwargs):
    """A wrapper for create_ftd2xx_connection() returning a (reader,
    writer) pair.
    The reader returned is a StreamReader instance; the writer is a
    StreamWriter instance.
    The arguments are all the usual arguments to open(). Additional
    optional keyword arguments are loop (to set the event loop instance
    to use) and limit (to set the buffer limit passed to the
    StreamReader.
    This function is a coroutine.
    """
    # if loop is None:
    #     loop = asyncio.get_event_loop()
    # if limit is None:
    #     limit = asyncio.streams._DEFAULT_LIMIT
    # reader = asyncio.StreamReader(limit=limit, loop=loop)
    # protocol = asyncio.StreamReaderProtocol(reader, loop=loop)
    # transport, _ = await create_serial_connection(
    #     loop=loop, protocol_factory=lambda: protocol, **kwargs
    # )
    # writer = asyncio.StreamWriter(transport, protocol, reader, loop)
    # return reader, writer
    raise NotImplementedError
