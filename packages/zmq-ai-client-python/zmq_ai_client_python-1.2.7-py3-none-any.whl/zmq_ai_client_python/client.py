from typing import TypeVar, Optional, List
import zmq

from zmq_ai_client_python.schema import HealthCheck
from zmq_ai_client_python.schema.base import Base
from zmq_ai_client_python.schema.completion import ChatCompletionRequest, ChatCompletion
from zmq_ai_client_python.schema.zmq_message_header import ZmqMessageType, create_message_header, ZmqMessageHeader, \
    ZmqMessageStatus
from zmq_ai_client_python.schema.session_state import SessionStateRequest, SessionState
from zmq_ai_client_python.error import LlamaClientError

T = TypeVar('T', bound=Base)


class LlamaClient:
    """
    LlamaClient is a client class to communicate with a server using ZeroMQ and MessagePack, with a timeout feature.
    """

    def __init__(self, host: str, timeout: int = 360000):
        """
        Initializes the LlamaClient with the specified host and an optional timeout.

        :param host: The server host to connect to.
        :param timeout: The reception timeout in milliseconds. Default is 360000ms (6 minutes).
        """
        self.host = host
        self.timeout = timeout
        self.context = zmq.Context()
        self._create_socket()

    def _create_socket(self):
        """
        Creates a new socket with the current timeout setting. If a socket already exists, it is closed before creating a new one.
        """
        if hasattr(self, 'socket'):
            self.socket.close()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.socket.connect(self.host)

    def _send_request(self,
                      zmq_message_type: ZmqMessageType,
                      request: Optional[T] = None) -> Optional[T]:
        """
        Sends a request to the server, according to the specified message type, and waits for a response, handling timeouts.

        :param zmq_message_type: The type of the ZeroMQ message to be sent.
        :param request: The request object to be sent, if applicable.
        :return: The unpacked response if successful, or raises a timeout exception.
        """

        message_header: ZmqMessageHeader = create_message_header(zmq_message_type)

        message_parts: List = [message_header.msgpack_pack()]
        if request:
            message_parts.append(request.msgpack_pack())

        self.socket.send_multipart(message_parts)

        try:
            resp_messages = self.socket.recv_multipart()
            if len(resp_messages) > 2:
                raise ValueError("Invalid response length")

            response_header: ZmqMessageHeader = ZmqMessageHeader.msgpack_unpack(resp_messages[0])
            if response_header.status == ZmqMessageStatus.ERROR:
                raise LlamaClientError(response_header)

            response_body: Base = zmq_message_type.get_associated_class
            return response_body.msgpack_unpack(resp_messages[1])
        except zmq.Again:
            self._create_socket()
            raise TimeoutError(f"Request timed out after {self.timeout} milliseconds")

    def send_chat_completion_request(self, request: ChatCompletionRequest) -> Optional[ChatCompletion]:
        """
        Sends a ChatCompletionRequest to the server and waits for a ChatCompletion response.

        :param request: The ChatCompletionRequest to send.
        :return: A ChatCompletion response or None if timed out.
        """
        return self._send_request(ZmqMessageType.CHAT_COMPLETION, request)

    def send_session_state_request(self, request: SessionStateRequest) -> Optional[SessionState]:
        """
        Sends a SessionStateRequest to the server and waits for a SessionState response.

        :param request: The SessionStateRequest to send.
        :return: A SessionState response or None if timed out.
        """
        return self._send_request(ZmqMessageType.SESSION_STATE, request)

    def send_health_check_request(self) -> Optional[HealthCheck]:
        """
        Sends a HealthCheck request to the server and waits for a HealthCheck response.

        :return: A HealthCheck response or None if timed out.
        """
        return self._send_request(ZmqMessageType.HEALTH_CHECK)
