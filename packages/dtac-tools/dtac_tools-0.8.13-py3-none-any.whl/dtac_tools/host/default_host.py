# default_host.py
import os
import queue
import sys
import json
import grpc
import traceback
import dtac_tools.host.plugin_pb2_grpc

from grpc import ssl_server_credentials
from urllib.parse import quote
from concurrent import futures
from .helpers.debug_sender import DebugSender
from .helpers.encryptor import RpcEncryptor
from .plugin_host import PluginHost
from .helpers.network import get_unused_tcp_port
from ..plugins.types import EndpointRequest, EndpointResponse, AuthGroup
from .plugin_pb2 import EndpointRequestMessage, EndpointResponseMessage, RegisterRequest, RegisterResponse, LogField, LogMessage, PluginEndpoint


class DefaultPluginHost(PluginHost):
    def __init__(self, plugin, debug=False, debug_port=5678):
        self.plugin = plugin
        self.rpc_proto = "grpc"
        self.proto = "tcp"
        self.ip = "127.0.0.1"
        self.interface_version = 'plug_api_1.0'
        self.port = None
        self.route_map = {}
        self.encryptor = RpcEncryptor.new_encryptor()
        self.log_channel = None
        self.debug_sender = None
        self.default_secure = True
        self.debugging_enabled = debug
        if self.debugging_enabled:
            self.debug_sender = DebugSender(debug_port)
            self.debug(f"PluginHost debugging enabled on port {debug_port}")
            self.debug(f"Debugging enabled in host: {self.plugin.name()}")
            self.plugin.enable_debugging()

    def debug(self, message):
        if hasattr(self, "debug_sender") and self.debug_sender is not None:
            self.debug_sender.write(message + "\n")

    # Register is the gRPC handler for the plugin. It will be called by the DTAC Agent when the plugin is loaded and will
    # be used to register the plugin with the DTAC Agent and to set up the endpoints that the plugin will handle.
    def Register(self, request: RegisterRequest, context: grpc.ServicerContext) -> RegisterResponse:

        try :
            params = {}
            if request.config is not None:
                self.debug(f"config: {request.config}")
                params["config"] = request.config

            if request.default_secure is not None:
                self.debug(f"default_secure: {request.default_secure}")
                params["default_secure"] = request.default_secure
                self.plugin.set_default_secure(request.default_secure)

            response = self.plugin.register(params)

            # build the route map
            for endpoint in response:
                self.route_map[endpoint.path] = endpoint

            return_eps = []
            for endpoint in response:
                # Ensure auth_group is set. If it is not set then set it to the most secure auth group
                if endpoint.auth_group is None:
                    endpoint.auth_group = AuthGroup.GroupAdmin

                api_ep = PluginEndpoint(
                    path = endpoint.path,
                    action = endpoint.action,
                    secure = endpoint.secure,
                    auth_group = endpoint.auth_group.value,
                    expected_metadata_schema = endpoint.expected_metadata_schema,
                    expected_headers_schema = endpoint.expected_headers_schema,
                    expected_parameters_schema = endpoint.expected_parameters_schema,
                    expected_body_schema = endpoint.expected_body_schema,
                    expected_output_schema = endpoint.expected_output_schema,
                )
                return_eps.append(api_ep)

            self.debug(f"response: {response}")
            return_val = RegisterResponse(
                endpoints = return_eps,
            )
            return return_val
        except Exception as ex:
            self.debug(f"Exception: {ex}")
            self.debug(traceback.format_exc())
            return RegisterResponse()


    # Call is the gRPC handler for the plugin. It will be called by the DTAC Agent when a request is made to the plugin
    # and will be used to route the call to the correct endpoint handler and return the response to the DTAC Agent
    def Call(self, request: EndpointRequestMessage, context: grpc.ServicerContext) -> EndpointResponseMessage:
        try:
            method = request.method
            request_args = EndpointRequest.from_api_request(request.request)
            self.debug(f"method: {method}")
            self.debug(f"request_args: {request_args}")
            function = self.route_map[method].function
            ret = function(request_args)
            self.debug(f"output: {ret}")

            return EndpointResponseMessage(
                id = 1234, # This isn't used by Python so just populate it with a dummy value
                response = ret.__to_api_response(),
                error = "", # This is a vestage of the old API and should likely be removed as gRPC can return errors directly
            )

        except Exception as ex:
            self.debug(f"Exception: {ex}")
            self.debug(traceback.format_exc())
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal error: {}'.format(ex))
            return EndpointResponseMessage()


    # LoggingStream is the gRPC handler for the logging stream. It will return a stream of log messages to the DTAC Agent
    def LoggingStream(self, request, context):
        try:
            if self.plugin.log_channel is None:
                self.plugin.log_channel = queue.Queue(maxsize=4096)
        except Exception as ex:
            self.debug(f"Exception: {ex}")
            self.debug(traceback.format_exc())
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal error: {}'.format(ex))
            return LogMessage()

        while True:
            try:
                msg = self.plugin.log_channel.get()
                yield msg
            except Exception as e:
                self.debug(f"Logging Exception: {e}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details('Logging error: {}'.format(e))
                break

    # serve is the main entry point for the plugin. It will start the gRPC server and listen for connections from the
    # DTAC Agent
    def serve(self):

        try:
            env_cookie = os.getenv("DTAC_PLUGINS")

            if env_cookie is None:
                print('============================ WARNING ============================')
                print('This is a DTAC plugin and is not designed to be executed directly')
                print('Please use the DTAC agent to load this plugin')
                print('==================================================================')
                sys.exit(-1)

            self.port = get_unused_tcp_port()

            # Check for certificate and key files passed via ENV variables
            cert = os.getenv("DTAC_TLS_CERT")
            key = os.getenv("DTAC_TLS_KEY")

            tls = bool(cert) and bool(key)
            options = [
                f'enc={quote(self.encryptor.key_string())}',
                f'tls={tls}',
            ]

            # Create a gRPC server
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

            # Check if both certificate and key are provided
            if tls:
                # Convert certificate and key strings into bytes
                certificate_chain = cert.encode('utf-8')
                private_key = key.encode('utf-8')

                # Create server SSL credentials
                server_credentials = ssl_server_credentials(
                    [(private_key, certificate_chain)]
                )

                # Add secure port using credentials
                server.add_secure_port(f"[::]:{self.port}", server_credentials)
            else:
                # Add insecure port if no TLS credentials are provided
                server.add_insecure_port(f"[::]:{self.port}")

            dtac_tools.host.plugin_pb2_grpc.add_PluginServiceServicer_to_server(self, server)
            server.start()

            print(f"CONNECT{{{{{self.plugin.name()}:{self.plugin.root_path()}:{self.rpc_proto}:{self.proto}:{self.ip}:{self.port}:{self.interface_version}:[{','.join(options)}]}}}}")
            sys.stdout.flush()

            if self.debugging_enabled:
                self.debug("interactive debugging has been removed from this build")
                # import debugpy
                # debugger_port = 6060
                # debugpy.listen(('localhost', debugger_port))
                # self.debug(f"Waiting for debugger to attach to port {debugger_port}...")
                # debugpy.wait_for_client()

            server.wait_for_termination()
        except Exception as ex:
            self.debug(f"Exception: {ex}")
            self.debug(traceback.format_exc())
            return

    # get_port returns the port that the plugin is listening for connection on
    def get_port(self):
        return self.port