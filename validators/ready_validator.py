from base_validator import BaseValidator
from parsers.base_parser import BaseParser
from requests.error_request import ErrorRequest
from statuses.error_statuses import ErrorStatus
from network_handlers.base_network_handler import BaseNetworkHandler


class ReadyValidator(BaseValidator):
    def __init__(self, request: dict, network_handler: BaseNetworkHandler, parser: BaseParser):
        self.request = request
        self.network_handler = network_handler
        self.parser = parser

    def validate_request_type(self):
        request_type = self.request.get("TYPE", None)
        if not request_type:
            raise UnexcpectedException
        if request_type == "ERROR" and self.request.get("STATUS") == "CLOSED":
            raise ClosedException
        if request_type != "READY":
            raise UnexcpectedException

    def validate(self):
        try:
            self.validate_request_type()
        except ClosedException:
            raise
        except UnexcpectedException:
            data = self.parser.pack(ErrorRequest(ErrorStatus.UNEXPECTED).to_dict())
            self.network_handler.send(data)
