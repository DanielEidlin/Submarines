from abc import ABC, abstractmethod
from socket import socket, AF_INET, SOCK_STREAM

DEFAULT_LISTEN_QUEUE = 5
PORT = 3000
DEFAULT_BUFFER_SIZE = 1024


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
    def receive(self, buffer_size: int = DEFAULT_BUFFER_SIZE) -> bytes:
        """
        Receives data from network.
        :param buffer_size: Size of data to receive.
        :return: Received data.
        """
        pass


class TCPNetworkHandler(BaseNetworkHandler):
    """
    Class representing a TCP network client.
    """

    def __init__(self):
        """
        Default constructor.
        """
        self.socket = socket(AF_INET, SOCK_STREAM)

    def listen(self, bind_ip: str = '', listen_queue: int = DEFAULT_LISTEN_QUEUE):
        """
        Listens for an incoming connection.
        :param bind_ip: IP address to bind to.
        :param listen_queue: Number of incoming connections to hold in queue.
        """
        self.socket.bind((bind_ip, PORT))
        self.socket.listen(listen_queue)

    def connect(self, ip: str):
        """
        Connects to another network client.
        :param ip: IP address to connect to.
        """
        self.socket.connect((ip, PORT))

    def send(self, data: bytes):
        """
        Sends data to network.
        :param data: Data to send.
        """
        self.socket.send(data)

    def receive(self, buffer_size: int = DEFAULT_BUFFER_SIZE) -> bytes:
        """
        Receives data from network.
        :param buffer_size: Size of data to receive.
        :return: Received data.
        """
        return self.socket.recv(buffer_size)
