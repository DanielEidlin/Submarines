from parsers.base_parser import BaseParser
from requests.error_request import ErrorRequest
from statuses.error_statuses import ErrorStatus
from statuses.answer_statuses import AnswerStatus
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

    def validate_request_fields(self):
        answer_statuses = self.request.get("STATUS")
        available_statuses = [status_name for status_name, _ in AnswerStatus.__members__.items()]
        if not answer_statuses:
            raise UnexpectedException
        if not all(status in available_statuses for status in answer_statuses):
            raise UnexpectedException

    def is_valid(self) -> bool:
        try:
            self.validate_request_type()
            self.validate_request_fields()
            return True
        except ClosedException:
            raise
        except UnexpectedException:
            data = self.parser.pack(ErrorRequest(ErrorStatus.UNEXPECTED).to_dict())
            self.network_handler.send(data)
