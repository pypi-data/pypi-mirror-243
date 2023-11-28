import json
import queue
import traceback
import typing

from pydantic import BaseModel
from typing import TypeVar, Type
from ..host.helpers.debug_sender import DebugSender
from .types import LoggingLevel, PluginEndpoint, EndpointAction, AuthGroup
from ..host.plugin_pb2 import LogField as apiLogField, LogLevel as apiLogLevel, LogMessage as apiLogMessage

# Base Config class, this is used to help deserialize configuration options for plugins
class BaseConfig(BaseModel):
    pass


class PluginShared:
    @staticmethod
    def name() -> str:
        return "UnnamedPlugin"
    
    @staticmethod
    def root_path() -> str:
        return ""
    
    @staticmethod
    def serialize(v: object) -> bytes:
        return json.dumps(v).encode('utf-8')

class PluginBase(PluginShared):

    T = TypeVar("T", bound=BaseConfig)
    log_channel: queue.Queue = None
    default_secure: bool = True

    # set_default_secure is a helper function that allows plugins to set the default secure value for all endpoints
    def set_default_secure(self, default_secure: bool):
        self.default_secure = default_secure

    # enable_debugging enables debugging for the plugin. This will open a port on the local machine and will allow the
    # plugin to send debug messages to the local udp port. This is not intended on being long-lived and is only meant
    # to be used for debugging purposes during the early development of this sdk
    def enable_debugging(self):
        self.debug_sender = DebugSender(5678)
        self.debug(f"Debugging enabled in plugin: {self.name()}")

    # debug prints out a debug message over the debug_sender if it is enabled.
    def debug(self, message):
        if hasattr(self, "debug_sender") and self.debug_sender is not None:
            self.debug_sender.write(message + "\n")

    # load_config is a helper class that will deserialize the configuration json into the provided config_class
    def load_config(self, config_json: str, config_class: Type[T]) -> T:
        return config_class.parse_raw(config_json)

    # register is a function that must be in all plugins with this signature. It is used to setup the handlers that the
    # plugin will support. At this level in the code it is just here to provide a default implementation that will
    # raise a NotImplementedError if it is not overridden by the plugin.
    def register(self, args):
        raise NotImplementedError("this method must be implemented")

    # log is a function to allow plugins to use the central logging facilities of the DTAC Agent. It takes a log_level
    # which is a LoggingLevel enum value, a message string, and a fields dictionary which is a dictionary of key/value
    def log(self, log_level: LoggingLevel, message: str, fields: dict):
        try:
            if self.log_channel is None:
                self.log_channel = queue.Queue(maxsize=4096)

            msg_fields = []
            for k, v in fields.items():
                msg_fields.append(apiLogField(key=k, value=v))

            log_message = apiLogMessage(level=log_level.to_api_level(), message=message, fields=msg_fields)
            self.log_channel.put(log_message)
        except Exception as ex:
            self.debug(f"Exception: {ex}")
            self.debug(traceback.format_exc())

    # name is a function that gets the name of the class which is used as the name of the plugin. --TOOD: check to see
    # if this is still needed as it shouldn't be since the default is to use the name of the plugin file minus the
    # .plugin extension as seen by the DTAC Agent.
    def name(self) -> str:
        return self.__class__.__name__

    def new_read_endpoint(self,
                          function: typing.Callable,
                          path: str,
                          description: str,
                          override_default_secure: bool = False,
                          secure: bool = True,
                          auth_group: AuthGroup | None = None,
                          expected_headers_schema: str | None = None,
                          expected_parameters_schema: str | None = None,
                          expected_body_schema: str | None = None,
                          expected_output_schema: str | None = None) -> PluginEndpoint:
        return self.new_endpoint(function=function, path=path,
                            action=EndpointAction.ActionRead.value,
                            description=description,
                                 override_default_secure=override_default_secure,
                                 secure=secure,
                                 auth_group=auth_group,
                                 expected_headers_schema=expected_headers_schema,
                                 expected_parameters_schema=expected_parameters_schema,
                                 expected_body_schema=expected_body_schema,
                                 expected_output_schema=expected_output_schema)

    def new_write_endpoint(self,
                           function: typing.Callable,
                           path: str,
                           description: str,
                           override_default_secure: bool = False,
                           secure: bool = True,
                           auth_group: AuthGroup | None = None,
                           expected_headers_schema: str | None = None,
                           expected_parameters_schema: str | None = None,
                           expected_body_schema: str | None = None,
                           expected_output_schema: str | None = None) -> PluginEndpoint:
        return self.new_endpoint(function=function, path=path,
                                 action=EndpointAction.ActionWrite.value,
                                 description=description,
                                 override_default_secure=override_default_secure,
                                 secure=secure,
                                 auth_group=auth_group,
                                 expected_headers_schema=expected_headers_schema,
                                 expected_parameters_schema=expected_parameters_schema,
                                 expected_body_schema=expected_body_schema,
                                 expected_output_schema=expected_output_schema)

    def new_create_endpoint(self,
                            function: typing.Callable,
                            path: str,
                            description: str,
                            override_default_secure: bool = False,
                            secure: bool = True,
                            auth_group: AuthGroup | None = None,
                            expected_headers_schema: str | None = None,
                            expected_parameters_schema: str | None = None,
                            expected_body_schema: str | None = None,
                            expected_output_schema: str | None = None) -> PluginEndpoint:
        return self.new_endpoint(function=function, path=path,
                                 action=EndpointAction.ActionCreate.value,
                                 description=description,
                                 override_default_secure=override_default_secure,
                                 secure=secure,
                                 auth_group=auth_group,
                                 expected_headers_schema=expected_headers_schema,
                                 expected_parameters_schema=expected_parameters_schema,
                                 expected_body_schema=expected_body_schema,
                                 expected_output_schema=expected_output_schema)

    def new_delete_endpoint(self,
                            function: typing.Callable,
                            path: str,
                            description: str,
                            override_default_secure: bool = False,
                            secure: bool = True,
                            auth_group: AuthGroup | None = None,
                            expected_headers_schema: str | None = None,
                            expected_parameters_schema: str | None = None,
                            expected_body_schema: str | None = None,
                            expected_output_schema: str | None = None) -> PluginEndpoint:
        return self.new_endpoint(function=function, path=path,
                                 action=EndpointAction.ActionDelete.value,
                                 description=description,
                                 override_default_secure=override_default_secure,
                                 secure=secure,
                                 auth_group=auth_group,
                                 expected_headers_schema=expected_headers_schema,
                                 expected_parameters_schema=expected_parameters_schema,
                                 expected_body_schema=expected_body_schema,
                                 expected_output_schema=expected_output_schema)

    def new_endpoint(self,
                     function: typing.Callable,
                     path: str,
                     action: str,
                     description: str,
                     override_default_secure: bool = False,
                     secure: bool = True,
                     auth_group: AuthGroup | None = None,
                     expected_headers_schema: str | None = None,
                     expected_parameters_schema: str | None = None,
                     expected_body_schema: str | None = None,
                     expected_output_schema: str | None = None) -> PluginEndpoint:
        make_secure = self.default_secure
        if override_default_secure:
            make_secure = secure

        return PluginEndpoint(
            function=function,
            path=path,
            action=action,
            description=description,
            secure=make_secure,
            auth_group=auth_group,
            expected_headers_schema=expected_headers_schema,
            expected_parameters_schema=expected_parameters_schema,
            expected_body_schema=expected_body_schema,
            expected_output_schema=expected_output_schema
        )
