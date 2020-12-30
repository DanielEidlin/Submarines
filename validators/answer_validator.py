from parsers.base_parser import BaseParser
from requests.error_request import ErrorRequest
from statuses.error_statuses import ErrorStatus
from exceptions import UnexpectedException, ClosedException
from network_handlers.base_network_handler import BaseNetworkHandler


class AnswerValidator:
    def __init__(self, request: dict, network_handler: BaseNetworkHandler, parser: BaseParser):
        self.request = request
        self.network_handler = network_handler
        self.parser = parser

    def validate_request_type(self):
        request_type = self.request.get("TYPE", None)
        if not request_type:
            raise UnexpectedException
        if request_type == "ERROR" and self.request.get("STATUS") == "CLOSED":
            raise ClosedException
        if request_type != "ANSWER":
            raise UnexpectedException

    def is_valid(self) -> bool:
        try:
            self.validate_request_type()
            return True
        except ClosedException:
            raise
        except UnexpectedException:
            data = self.parser.pack(ErrorRequest(ErrorStatus.UNEXPECTED).to_dict())
            self.network_handler.send(data)
