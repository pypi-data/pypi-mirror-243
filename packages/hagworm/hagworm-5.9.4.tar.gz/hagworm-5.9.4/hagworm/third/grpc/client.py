# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import typing
import asyncio
import grpc
import msgpack

from abc import abstractmethod
from collections import OrderedDict

from ...extend.base import Utils


CHANNEL_USABLE_STATE = (grpc.ChannelConnectivity.READY, grpc.ChannelConnectivity.IDLE)


class GRPCClientAbstract:

    def __init__(
            self, *,
            credentials: typing.Optional[grpc.ChannelCredentials] = None,
            options: typing.Optional[grpc.aio.ChannelArgumentType] = None,
            compression: typing.Optional[grpc.Compression] = None,
            interceptors: typing.Optional[typing.Sequence[grpc.aio.ClientInterceptor]] = None,
            request_serializer: typing.Callable = msgpack.dumps,
            response_deserializer: typing.Callable = msgpack.loads
    ):

        self._credentials: typing.Optional[grpc.ChannelCredentials] = credentials
        self._options: typing.Optional[grpc.aio.ChannelArgumentType] = options
        self._compression: typing.Optional[grpc.Compression] = compression
        self._interceptors: typing.Optional[typing.Sequence[grpc.aio.ClientInterceptor]] = interceptors

        self._request_serializer: typing.Callable = request_serializer
        self._response_deserializer: typing.Callable = response_deserializer

    async def _make_channel(self, target: str, timeout: int = 0) -> grpc.aio.Channel:

        channel = None

        try:

            if self._credentials is None:
                channel = grpc.aio.insecure_channel(
                    target, self._options, self._compression, self._interceptors
                )
            else:
                channel = grpc.aio.secure_channel(
                    target, self._credentials, self._options, self._compression, self._interceptors
                )

            if timeout > 0:
                await asyncio.wait_for(channel.channel_ready(), timeout)

        except asyncio.TimeoutError as err:

            await channel.close()

            raise err

        return channel

    @abstractmethod
    async def open(self, targets: typing.List[str], timeout: int = 0):

        raise NotImplementedError()

    @abstractmethod
    async def close(self):

        raise NotImplementedError()

    @abstractmethod
    async def get_channel(self, *args, **kwargs) -> grpc.aio.Channel:

        raise NotImplementedError()

    @abstractmethod
    async def reset_channel(self, targets, timeout=0):

        raise NotImplementedError()

    async def unary_unary(
            self, channel: grpc.aio.Channel,
            method: str, call_params: typing.Dict
    ) -> grpc.aio.UnaryUnaryCall:

        return await channel.unary_unary(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)

    async def unary_stream(
            self, channel: grpc.aio.Channel,
            method: str, call_params: typing.Dict
    ) -> grpc.aio.UnaryStreamCall:

        return channel.unary_stream(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)

    async def stream_unary(
            self, channel: grpc.aio.Channel,
            method: str, call_params: typing.Union[typing.Iterable[typing.Dict], typing.AsyncIterable[typing.Dict]]
    ) -> grpc.aio.StreamUnaryCall:

        return await channel.stream_unary(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)

    async def stream_stream(
            self, channel: grpc.aio.Channel,
            method: str, call_params: typing.Union[typing.Iterable[typing.Dict], typing.AsyncIterable[typing.Dict]]
    ) -> grpc.aio.StreamStreamCall:

        return channel.stream_stream(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)


class GRPCClient(GRPCClientAbstract):

    def __init__(
            self, *,
            credentials: typing.Optional[grpc.ChannelCredentials] = None,
            options: typing.Optional[grpc.aio.ChannelArgumentType] = None,
            compression: typing.Optional[grpc.Compression] = None,
            interceptors: typing.Optional[typing.Sequence[grpc.aio.ClientInterceptor]] = None,
            request_serializer: typing.Callable = msgpack.dumps,
            response_deserializer: typing.Callable = msgpack.loads
    ):

        super().__init__(
            credentials=credentials, options=options, compression=compression, interceptors=interceptors,
            request_serializer=request_serializer, response_deserializer=response_deserializer
        )

        self._lock: asyncio.Lock = asyncio.Lock()
        self._channels: OrderedDict = OrderedDict()

    async def open(self, targets: typing.List[str], timeout: int = 0):

        await self.reset_channel(targets, timeout)

    async def close(self):

        async with self._lock:

            for _channel in self._channels.values():
                await _channel.close()

            self._channels.clear()

    async def get_channel(self) -> grpc.aio.Channel:

        channel = None

        async with self._lock:

            for _ in range(len(self._channels)):

                _target, _channel = self._channels.popitem()
                self._channels[_target] = _channel

                if _channel.get_state() in CHANNEL_USABLE_STATE:
                    channel = _channel
                    break
                else:
                    Utils.log.warning(f'grpc server unusable: {_target}')

            else:

                Utils.log.error(f'all grpc server unusable: {list(self._channels.keys())}')

        return channel

    async def reset_channel(self, targets: typing.List[str], timeout: int = 0):

        async with self._lock:

            if len(self._channels) > 0:

                for _channel in self._channels.values():
                    await _channel.close()

                self._channels.clear()

            for target in set(targets):

                channel = await self._make_channel(target, timeout)

                if channel is not None:
                    self._channels[target] = channel


class GRPCClientSlots(GRPCClientAbstract):

    def __init__(
            self, *,
            credentials: typing.Optional[grpc.ChannelCredentials] = None,
            options: typing.Optional[grpc.aio.ChannelArgumentType] = None,
            compression: typing.Optional[grpc.Compression] = None,
            interceptors: typing.Optional[typing.Sequence[grpc.aio.ClientInterceptor]] = None,
            request_serializer: typing.Callable = msgpack.dumps,
            response_deserializer: typing.Callable = msgpack.loads
    ):

        super().__init__(
            credentials=credentials, options=options, compression=compression, interceptors=interceptors,
            request_serializer=request_serializer, response_deserializer=response_deserializer
        )

        self._lock: asyncio.Lock = asyncio.Lock()
        self._channels: typing.List[grpc.Channel] = []

    async def open(self, targets, timeout=None):

        await self.reset_channel(targets, timeout)

    async def close(self):

        async with self._lock:

            for _channel in self._channels:
                await _channel.close()

            self._channels.clear()

    async def get_channel(self, name) -> grpc.aio.Channel:

        async with self._lock:
            index = Utils.md5_u64(str(name)) % len(self._channels)
            return self._channels[index]

    async def reset_channel(self, targets: typing.List[str], timeout: int = 0):

        async with self._lock:

            if len(self._channels) > 0:

                for _channel in self._channels:
                    await _channel.close()

                self._channels.clear()

            for target in set(targets):

                channel = await self._make_channel(target, timeout)

                if channel is not None:
                    self._channels.append(channel)
