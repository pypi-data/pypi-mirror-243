import json
import typing
from enum import Enum
from ..host.plugin_pb2 import LogLevel as apiLogLevel
from ..host.plugin_pb2 import StringList, EndpointRequest as apiEndpointRequest, EndpointResponse as apiEndpointResponse
from ..host.helpers.debug_sender import DebugSender

class AuthGroup(Enum):
    GroupGuest = "guest"
    GroupUser = "user"
    GroupOperator = "operator"
    GroupAdmin = "admin"

# EndpointAction is an enum that represents the actions that the plugin can perform
class EndpointAction(Enum):
    ActionRead = "read"
    ActionWrite = "write"
    ActionDelete = "delete"
    ActionCreate = "create"

class LoggingLevel(Enum):
    LevelDebug = 0
    LevelInfo = 1
    LevelWarning = 2
    LevelError = 3
    LevelFatal = 4

    def to_api_level(self):
        if self == LoggingLevel.LevelDebug:
            return apiLogLevel.Debug
        elif self == LoggingLevel.LevelInfo:
            return apiLogLevel.INFO
        elif self == LoggingLevel.LevelWarning:
            return apiLogLevel.WARNING
        elif self == LoggingLevel.LevelError:
            return apiLogLevel.ERROR
        elif self == LoggingLevel.LevelFatal:
            return apiLogLevel.FATAL
        else:
            return apiLogLevel.ERROR

class LogMessage:
    def __init__(self, level, message, fields):
        self.level = level
        self.message = message
        self.fields = fields

# EndpointRequest is a class that represents the request that is sent to the plugin from the DTAC Agent
# it uses composition and redirection to expose the attributes of the grpc class without exposing the class
# itself directly to SDK users
class EndpointRequest:

    metadata: typing.Mapping[str, str] | None
    headers: typing.Mapping[str, StringList] | None
    parameters: typing.Mapping[str, StringList] | None
    body: bytes | None

    def __init__(self, *args, **kwargs):
        # Initialize the composed object without setting attributes
        self._api_endpoint_request = apiEndpointRequest()

        # Use __setattr__ to set attributes
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __getattr__(self, item):
        value = getattr(self._api_endpoint_request, item)
        if item == 'headers' or item == 'parameters':
            return {k: list(v.values) for k, v in value.items()}
        return value

    def __setattr__(self, key, value):
        if key == '_api_endpoint_request':
            super().__setattr__(key, value)
        elif key == 'headers' or key == 'parameters':
            # Convert list to StringList
            string_list_value = {k: StringList(values=v) for k, v in value.items()}
            setattr(self._api_endpoint_request, key, string_list_value)
        else:
            setattr(self._api_endpoint_request, key, value)

    def __to_api_request(self):
        return self._api_endpoint_request

    @staticmethod
    def __from_api_request(api_request: apiEndpointRequest):
        # Create an SDK object from a gRPC object
        request = EndpointRequest()
        request._api_endpoint_request = api_request
        return request

# EndpointResponse is a class that represents the request that is sent to the plugin from the DTAC Agent
# it uses composition and redirection to expose the attributes of the grpc class without exposing the class
# itself directly to SDK users
class EndpointResponse:

    metadata: typing.Mapping[str, str] | None
    headers: typing.Mapping[str, StringList] | None
    parameters: typing.Mapping[str, StringList] | None
    body: bytes | None

    def __init__(self, headers: typing.Mapping[str, typing.List[str]], parameters: typing.Mapping[str, typing.List[str]], *args, **kwargs):
        # Initialize the composed object without setting attributes
        self._api_endpoint_response = apiEndpointResponse()

        # Use __setattr__ to set attributes
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __getattr__(self, item):
        value = getattr(self._api_endpoint_response, item)
        if item == 'headers' or item == 'parameters':
            return {k: list(v.values) for k, v in value.items()}
        return value

    def __setattr__(self, key, value):
        if key == '_api_endpoint_response':
            super().__setattr__(key, value)
        elif key == 'headers':
            # Convert list to StringList
            headers = {k: StringList(values=v) for k, v in value.items()}
            for key, value in headers.items():
                self._api_endpoint_response.headers[key].values.extend(value)
        elif key == 'parameters':
            # Convert list to StringList
            parameters = {k: StringList(values=v) for k, v in value.items()}
            for key, value in parameters.items():
                self._api_endpoint_response.parameters[key].values.extend(value)
        elif key == 'value':
            # Check if the value is already a byte array
            if not isinstance(value, bytes):
                try:
                    # Serialize to JSON and then to bytes
                    serialized_value = json.dumps(value).encode('utf-8')
                except TypeError:
                    raise ValueError("Provided value is not serializable")
                self._api_endpoint_response.value = serialized_value
            else:
                self._api_endpoint_response.value = value
        else:
            setattr(self._api_endpoint_response, key, value)

    def __to_api_response(self):
        return self._api_endpoint_response

    @staticmethod
    def __from_api_response(api_response: apiEndpointResponse):
        # Create an SDK object from a gRPC object
        response = EndpointResponse()
        response._api_endpoint_response = api_response
        return response

class PluginEndpoint:
    def __init__(self,
                 function: typing.Callable,
                 path: str,
                 action: str,
                 description: str,
                 secure: bool = True,
                 auth_group: str | None = None,
                 expected_metadata_schema: str | None = None,
                 expected_headers_schema: str | None = None,
                 expected_parameters_schema: str | None = None,
                 expected_body_schema: str | None = None,
                 expected_output_schema: str | None = None
                 ):
        self.function = function
        self.function_name = function.__name__
        self.path = path
        self.action = action
        self.description = description
        self.secure = secure
        self.auth_group = auth_group
        self.expected_metadata_schema = expected_metadata_schema
        self.expected_headers_schema = expected_headers_schema
        self.expected_parameters_schema = expected_parameters_schema
        self.expected_body_schema = expected_body_schema
        self.expected_output_schema = expected_output_schema

    def to_dict(self):
        return {
            "function_name": self.function_name,
            "path": self.path,
            "action": self.action,
            "description": self.description,
            "secure": self.secure,
            "auth_group": self.auth_group,
            "expected_metadata_schema": self.expected_metadata_schema,
            "expected_headers_schema": self.expected_headers_schema,
            "expected_parameters_schema": self.expected_parameters_schema,
            "expected_body_schema": self.expected_body_schema,
            "expected_output_schema": self.expected_output_schema
        }

    def to_json(self):
        return json.dumps(self, default=lambda o: {k: v for k, v in o.__dict__.items() if v is not None and not callable(v)}, indent=4)



# class InputArgs:
#     def __init__(self, headers=None, params=None, body=None):
#         if headers is None:
#             headers = {}
#         if params is None:
#             params = {}
#         self.headers = headers
#         self.params = params
#         self.body = body
#
#     def to_dict(self):
#         return {
#             "headers": self.headers,
#             "params": self.params,
#             "body": self.body.decode('utf-8') if self.body else None
#         }
#
#     def to_json(self):
#         return json.dumps(self.to_dict())
#
#     @classmethod
#     def from_json(cls, json_str):
#         data = json.loads(json_str)
#         body = data.get("body")
#         if body is not None:
#             body = body.encode('utf-8')
#         return cls(
#             headers=data.get("headers"),
#             params=data.get("params"),
#             body=body
#         )
#
#     @classmethod
#     def from_dict(cls, data):
#         body = data.get("body")
#         if body is not None:
#             body = body.encode('utf-8')
#         return cls(
#             headers=data.get("headers"),
#             params=data.get("params"),
#             body=body
#         )
#
#     @classmethod
#     def from_grpc(cls, grpc_obj: ApiInputArgs):
#         headers = {}
#         # for key, value in grpc_obj.headers.items():
#         #     headers[key] = value
#         #
#         params = {}
#         # for key, value in grpc_obj.params.items():
#         #     params[key] = value
#
#         return cls(
#             headers=headers,
#             params=params,
#             body=grpc_obj.body
#         )
#
# class ReturnVal:
#     def __init__(self, headers=None, params=None, value=None):
#         if headers is None:
#             headers = {}
#         if params is None:
#             params = {}
#         self.headers = headers
#         self.params = params
#         self.value = value
#
#     def value_to_json(self):
#         # Convert the value attribute to a JSON string
#         try:
#             return json.dumps(self.value)
#         except TypeError as e:
#             # Handle the error if value is not serializable
#             return str(e)
#
#     def to_dict(self):
#         return {
#             "headers": self.headers,
#             "params": self.params,
#             "value": self.value
#         }
#
#     def to_json(self):
#         return json.dumps(self.to_dict())
#
#     def to_grpc(self):
#         headers = {}
#         for key, values in self.headers.items():
#             headers[key] = StringList(values=values)
#
#         params = {}
#         for key, values in self.params.items():
#             params[key] = StringList(values=values)
#
#         return ApiReturnVal(
#             headers=headers,
#             params=params,
#             value=self.value
#         )