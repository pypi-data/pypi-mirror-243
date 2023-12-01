"""remote.py."""
from abc import ABC, abstractmethod


class RemoteObject(ABC):
    """Class that represents a remote object."""

    @abstractmethod
    def get_sw_status(self):
        """Return Strangeworks Status."""

    @abstractmethod
    def remote_id(self) -> str:
        """Return remote identifier."""

    @abstractmethod
    def remote_status(self) -> str:
        """Return remote status."""
