from typing import Optional
from abc import ABC, abstractmethod
from consts import DEFAULT_LISTEN_QUEUE, DEFAULT_BUFFER_SIZE


class BaseNetworkHandler(ABC):
    """
    Class representing an abstract network client.
    """

    @abstractmethod
    def listen(self, bind_ip: str = '', listen_queue: int = DEFAULT_LISTEN_QUEUE):
        """
        Listens for an incoming connection.
        :param bind_ip: IP address to bind to.
        :param listen_queue: Number of incoming connections to hold in queue.
        """
        pass

    @abstractmethod
    def connect(self, ip: str):
        """
        Connects to another network client.
        :param ip: IP address to connect to.
        """
        pass

    @abstractmethod
    def send(self, data: bytes):
        """
        Sends data to network.
        :param data: Data to send.
        """
        pass

    @abstractmethod
    def receive(self, buffer_size: int = DEFAULT_BUFFER_SIZE, timeout: float = None) -> Optional[bytes]:
        """
        Receives data from network.
        :param buffer_size: Size of data to receive.
        :param timeout: Timeout for receiving.
        :return: Received data.
        """
        pass
