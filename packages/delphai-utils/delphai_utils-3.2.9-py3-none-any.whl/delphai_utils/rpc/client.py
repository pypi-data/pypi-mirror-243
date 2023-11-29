import aio_pika
import aio_pika.exceptions
import asyncio
import logging
import socket
import time
import uuid
import weakref

from typing import Any, Dict, Optional

from . import errors
from .models import AbstractOptions, Request, Response
from .types import Message
from .utils import clean_service_name, fix_message_timestamp


logger = logging.getLogger(__name__)


class Options(AbstractOptions):
    timeout: Optional[float] = 60
    priority: Optional[int] = None


class RpcClient:
    def __init__(
        self, client_name, connection_string, *args: Options, **kwargs: Dict[str, Any]
    ):
        self._client_name = clean_service_name(client_name)
        self._connection_string = connection_string
        self._app_id = f"{self._client_name}@{socket.gethostname()}"

        self._options = Options(*args, **kwargs)
        self._connect_lock = asyncio.Lock()
        self._declare_exchange_lock = asyncio.Lock()

        self._reset()

    def _reset(self):
        self._connection = None
        self._channel = None
        self._reply_queue = None

        self._exchanges = {}
        self._futures = weakref.WeakValueDictionary()

    def get_service(self, service_name: str, *args: Options, **kwargs: Dict[str, Any]):
        options = self._options.update(*args, **kwargs)
        return RpcService(self, clean_service_name(service_name), options)

    __getitem__ = __getattr__ = get_service

    async def _ensure_connection_and_queue(self):
        async with self._connect_lock:
            if self._connection:
                return

            connection = await aio_pika.connect_robust(self._connection_string)
            channel = await connection.channel(on_return_raises=True)

            queue_name = f"client.{self._client_name}.{uuid.uuid4().hex}"
            queue = await channel.declare_queue(
                name=queue_name,
                exclusive=True,
                auto_delete=True,
            )
            await queue.consume(fix_message_timestamp(self._on_message))

            self._connection = connection
            self._channel = channel
            self._reply_queue = queue

    async def stop(self):
        connection = self._connection
        if connection:
            self._reset()
            await connection.close()

    async def call(
        self,
        service_name: str,
        method_name: str,
        arguments: Optional[Dict[str, Any]] = None,
        options: Optional[Options] = None,
    ):
        if options.timeout:
            deadline = time.monotonic() + options.timeout
            waiter = lambda coro: asyncio.wait_for(  # noqa: E731
                coro, timeout=(deadline - time.monotonic())
            )
        else:
            waiter = lambda coro: coro  # noqa: E731

        correlation_id = str(uuid.uuid1())

        request = Request(method_name=method_name, arguments=arguments)

        future = asyncio.get_running_loop().create_future()
        self._futures[correlation_id] = future

        await waiter(self._send_request(correlation_id, service_name, request, options))

        try:
            return await waiter(future)
        except asyncio.CancelledError:
            logger.warning(
                "Wait was cancelled but not the request itself. "
                "Pass `timeout` option instead of using `asyncio.wait_for` or similar"
            )
            raise

    async def _send_request(self, correlation_id, service_name, request, options):
        await self._ensure_connection_and_queue()

        request_message = Message(
            body=request,
            app_id=self._app_id,
            priority=options.priority,
            correlation_id=correlation_id,
            reply_to=self._reply_queue.name,
            expiration=options.timeout or None,
            type="rpc.request",
        )

        async with self._declare_exchange_lock:
            if service_name not in self._exchanges:
                try:
                    self._exchanges[service_name] = await self._channel.get_exchange(
                        f"service.{service_name}"
                    )
                except aio_pika.exceptions.ChannelNotFoundEntity:
                    raise errors.UnknownServiceError("Exchange was not found")

        try:
            await self._exchanges[service_name].publish(
                message=request_message,
                routing_key=f"method.{request.method_name}",
            )
        except aio_pika.exceptions.PublishError:
            raise errors.UnknownServiceError("Request was not delivered to a queue")

    async def _on_message(self, message):
        if message.type != "rpc.response":
            logger.warning(
                "[MID:%s] Unexpected message type: `%s`",
                message.message_id,
                message.type,
            )
            await message.reject()
            return

        if not message.correlation_id:
            logger.warning("[MID:%s] `correlation_id` is not set", message.message_id)
            await message.reject()
            return

        future = self._futures.pop(message.correlation_id, None)
        if not future or future.done():
            logger.warning(
                "[MID:%s] [CID:%s] Response is not awaited (too late or duplicate)",
                message.message_id,
                message.correlation_id,
            )
            await message.reject()
            return

        try:
            future.set_result(await self._process_message(message))
        except Exception as error:
            future.set_exception(error)

        await message.ack()

        logger.debug(
            "[MID:%s] [CID:%s] Got `%s` from `%s` service",
            message.message_id,
            message.correlation_id,
            message.type,
            message.app_id or "unknown",
        )

    async def _process_message(self, message) -> Any:
        if message.content_type != "application/msgpack":
            raise errors.ParsingError(
                f"Got a message with unknown content type: {message.content_type}"
            )

        try:
            response = Response.model_validate_msgpack(message.body)
        except ValueError as error:
            raise errors.ParsingError(f"Message deserialization failed `{error!r}`")

        if response.error:
            error_class = getattr(errors, response.error.type, errors.UnknownError)
            raise error_class(response.error.message)

        return response.result


class RpcService:
    def __init__(self, client, service_name, options):
        self._client = client
        self._service_name = service_name
        self._options = options

    def get_method(self, method_name: str, *args: Options, **kwargs: Dict[str, Any]):
        options = self._options.update(*args, **kwargs)
        return RpcMethod(self._client, self._service_name, method_name, options)

    __getitem__ = __getattr__ = get_method

    def __repr__(self):
        class_ = self.__class__
        return f"<{class_.__qualname__} `{self._service_name}`>"


class RpcMethod:
    def __init__(self, client, service_name, method_name, options):
        self._client = client
        self._service_name = service_name
        self._method_name = method_name
        self._options = options

    def __repr__(self):
        class_ = self.__class__
        return (
            f"<{class_.__qualname__} `{self._method_name}` "
            "of service `{self._service_name}`>"
        )

    def __call__(self, *args: Options, **kwargs: Dict[str, Any]):
        options = self._options.update(*args)
        return self._client.call(
            service_name=self._service_name,
            method_name=self._method_name,
            arguments=kwargs,
            options=options,
        )
