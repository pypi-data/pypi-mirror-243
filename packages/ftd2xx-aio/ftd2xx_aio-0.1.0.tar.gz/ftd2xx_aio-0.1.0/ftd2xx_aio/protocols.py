from abc import abstractmethod
import asyncio
from ftd2xx.defines import ModemStatus


class FTD2xxProtocol(asyncio.Protocol):
    """Adds a callback to the standard asyncio.Protocol class for modem signals."""

    @abstractmethod
    def modem_received(self, status: ModemStatus, changed: ModemStatus):
        """Callback for modem status change.

        Args:
            status (ModemStatus): The current status returned from getModemStatus.
            changed (ModemStatus): Indicates which flags have changed state since last callback.
        """
