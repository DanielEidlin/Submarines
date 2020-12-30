from parsers.base_parser import BaseParser
from requests.error_request import ErrorRequest
from statuses.error_statuses import ErrorStatus
from network_handlers.base_network_handler import BaseNetworkHandler
from exceptions import UnexpectedException, ClosedException, OutOfRangeException


class AttemptValidator:
    def __init__(self, request: dict, network_handler: BaseNetworkHandler, parser: BaseParser, max_value: int,
                 min_value: int):
        self.request = request
        self.network_handler = network_handler
        self.parser = parser
        self.max_value = max_value
        self.min_value = min_value

    def validate_request_type(self):
        request_type = self.request.get("TYPE", None)
        if not request_type:
            raise UnexpectedException
        if request_type == "ERROR" and self.request.get("STATUS") == "CLOSED":
            raise ClosedException
        if request_type != "ATTEMPT":
            raise UnexpectedException

    def validate_request_fields(self):
        x_coordinate = self.request.get("X-COOR", None)
        y_coordinate = self.request.get("Y-COOR", None)
        if not x_coordinate or not y_coordinate:
            raise UnexpectedException
        if x_coordinate >= self.max_value or x_coordinate < self.min_value:
            raise OutOfRangeException
        if y_coordinate >= self.max_value or y_coordinate < self.min_value:
            raise OutOfRangeException

    def is_valid(self) -> bool:
        try:
            self.validate_request_type()
            self.validate_request_fields()
            return True
        except ClosedException:
            raise
        except UnexpectedException:
            request = ErrorRequest(ErrorStatus.UNEXPECTED)
            data = self.parser.pack(request.to_dict())
            self.network_handler.send(data)
        except OutOfRangeException:
            request = ErrorRequest(ErrorStatus.OUT_OF_RANGE)
            data = self.parser.pack(request.to_dict())
            self.network_handler.send(data)
