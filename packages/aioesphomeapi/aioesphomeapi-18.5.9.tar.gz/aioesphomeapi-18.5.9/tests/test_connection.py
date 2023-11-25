from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from datetime import timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from aioesphomeapi import APIClient
from aioesphomeapi._frame_helper import APIPlaintextFrameHelper
from aioesphomeapi.api_pb2 import (
    DeviceInfoResponse,
    DisconnectRequest,
    HelloResponse,
    PingRequest,
    PingResponse,
)
from aioesphomeapi.connection import APIConnection, ConnectionParams, ConnectionState
from aioesphomeapi.core import (
    APIConnectionError,
    ConnectionNotEstablishedAPIError,
    HandshakeAPIError,
    InvalidAuthAPIError,
    RequiresEncryptionAPIError,
    SocketAPIError,
    TimeoutAPIError,
)

from .common import (
    async_fire_time_changed,
    connect,
    generate_plaintext_packet,
    get_mock_protocol,
    mock_data_received,
    send_ping_request,
    send_ping_response,
    send_plaintext_connect_response,
    send_plaintext_hello,
    utcnow,
)
from .conftest import KEEP_ALIVE_INTERVAL

KEEP_ALIVE_TIMEOUT_RATIO = 4.5


@pytest.mark.asyncio
async def test_connect(
    plaintext_connect_task_no_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ]
) -> None:
    """Test that a plaintext connection works."""
    conn, transport, protocol, connect_task = plaintext_connect_task_no_login
    mock_data_received(
        protocol,
        bytes.fromhex(
            "003602080110091a216d6173746572617672656c61792028657"
            "370686f6d652076323032332e362e3329220d6d617374657261"
            "7672656c6179"
        ),
    )
    mock_data_received(
        protocol,
        bytes.fromhex(
            "005b0a120d6d6173746572617672656c61791a1130383a33413a"
            "46323a33453a35453a36302208323032332e362e332a154a756e"
            "20323820323032332c2031383a31323a3236320965737033322d"
            "65766250506209457370726573736966"
        ),
    )
    await connect_task
    assert conn.is_connected


@pytest.mark.asyncio
async def test_timeout_sending_message(
    plaintext_connect_task_no_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
    caplog: pytest.LogCaptureFixture,
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_no_login

    mock_data_received(
        protocol,
        b'\x00@\x02\x08\x01\x10\x07\x1a(m5stackatomproxy (esphome v2023.1.0-dev)"\x10m'
        b"5stackatomproxy"
        b"\x00\x00$"
        b"\x00\x00\x04"
        b'\x00e\n\x12\x10m5stackatomproxy\x1a\x11E8:9F:6D:0A:68:E0"\x0c2023.1.0-d'
        b"ev*\x15Jan  7 2023, 13:19:532\x0cm5stack-atomX\x03b\tEspressif",
    )

    await connect_task

    with pytest.raises(TimeoutAPIError):
        await conn.send_messages_await_response_complex(
            (PingRequest(),), None, None, (PingResponse,), 0
        )

    transport.reset_mock()
    with patch("aioesphomeapi.connection.DISCONNECT_RESPONSE_TIMEOUT", 0.0):
        await conn.disconnect()

    transport.write.assert_called_with(b"\x00\x00\x05")

    assert "disconnect request failed" in caplog.text
    assert " Timeout waiting for DisconnectResponse after 0.0s" in caplog.text


@pytest.mark.asyncio
async def test_disconnect_when_not_fully_connected(
    plaintext_connect_task_no_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
    caplog: pytest.LogCaptureFixture,
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_no_login

    # Only send the first part of the handshake
    # so we are stuck in the middle of the connection process
    mock_data_received(
        protocol,
        b'\x00@\x02\x08\x01\x10\x07\x1a(m5stackatomproxy (esphome v2023.1.0-dev)"\x10m',
    )

    await asyncio.sleep(0)
    transport.reset_mock()

    with patch("aioesphomeapi.connection.DISCONNECT_CONNECT_TIMEOUT", 0.0), patch(
        "aioesphomeapi.connection.DISCONNECT_RESPONSE_TIMEOUT", 0.0
    ):
        await conn.disconnect()

    with pytest.raises(
        APIConnectionError,
        match="Timed out waiting to finish connect before disconnecting",
    ):
        await connect_task

    transport.write.assert_called_with(b"\x00\x00\x05")

    assert "disconnect request failed" in caplog.text
    assert " Timeout waiting for DisconnectResponse after 0.0s" in caplog.text


@pytest.mark.asyncio
async def test_requires_encryption_propagates(conn: APIConnection):
    loop = asyncio.get_event_loop()
    protocol = get_mock_protocol(conn)
    with patch.object(loop, "create_connection") as create_connection:
        create_connection.return_value = (MagicMock(), protocol)

        conn._socket = MagicMock()
        await conn._connect_init_frame_helper()
        loop.call_soon(conn._frame_helper._ready_future.set_result, None)
        conn.connection_state = ConnectionState.CONNECTED

        with pytest.raises(RequiresEncryptionAPIError):
            task = asyncio.create_task(conn._connect_hello_login(login=True))
            await asyncio.sleep(0)
            mock_data_received(protocol, b"\x01\x00\x00")
            await task


@pytest.mark.asyncio
async def test_plaintext_connection(
    plaintext_connect_task_no_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that a plaintext connection works."""
    messages = []
    conn, transport, protocol, connect_task = plaintext_connect_task_no_login

    def on_msg(msg):
        messages.append(msg)

    remove = conn.add_message_callback(on_msg, (HelloResponse, DeviceInfoResponse))
    mock_data_received(
        protocol,
        b'\x00@\x02\x08\x01\x10\x07\x1a(m5stackatomproxy (esphome v2023.1.0-dev)"\x10m',
    )
    mock_data_received(protocol, b"5stackatomproxy")
    mock_data_received(protocol, b"\x00\x00$")
    mock_data_received(protocol, b"\x00\x00\x04")
    mock_data_received(
        protocol,
        b'\x00e\n\x12\x10m5stackatomproxy\x1a\x11E8:9F:6D:0A:68:E0"\x0c2023.1.0-d',
    )
    mock_data_received(
        protocol, b"ev*\x15Jan  7 2023, 13:19:532\x0cm5stack-atomX\x03b\tEspressif"
    )
    await asyncio.sleep(0)
    await connect_task
    assert conn.is_connected
    assert len(messages) == 2
    assert isinstance(messages[0], HelloResponse)
    assert isinstance(messages[1], DeviceInfoResponse)
    assert messages[1].name == "m5stackatomproxy"
    remove()
    await conn.force_disconnect()
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_start_connection_socket_error(
    conn: APIConnection, resolve_host, socket_socket
):
    """Test handling of socket error during start connection."""
    loop = asyncio.get_event_loop()

    with patch.object(loop, "create_connection", side_effect=OSError("Socket error")):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await asyncio.sleep(0)
        with pytest.raises(APIConnectionError, match="Socket error"):
            await connect_task

    async_fire_time_changed(utcnow() + timedelta(seconds=600))
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_start_connection_times_out(
    conn: APIConnection, resolve_host, socket_socket
):
    """Test handling of start connection timing out."""
    loop = asyncio.get_event_loop()

    async def _mock_socket_connect(*args, **kwargs):
        await asyncio.sleep(500)

    with patch.object(loop, "sock_connect", side_effect=_mock_socket_connect), patch(
        "aioesphomeapi.connection.TCP_CONNECT_TIMEOUT", 0.0
    ):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await asyncio.sleep(0)

        async_fire_time_changed(utcnow() + timedelta(seconds=200))
        await asyncio.sleep(0)

    with pytest.raises(APIConnectionError, match="Timeout while connecting"):
        await connect_task

    async_fire_time_changed(utcnow() + timedelta(seconds=600))
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_start_connection_os_error(
    conn: APIConnection, resolve_host, socket_socket
):
    """Test handling of start connection has an OSError."""
    loop = asyncio.get_event_loop()

    with patch.object(loop, "sock_connect", side_effect=OSError("Socket error")):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await asyncio.sleep(0)
        with pytest.raises(APIConnectionError, match="Socket error"):
            await connect_task

    async_fire_time_changed(utcnow() + timedelta(seconds=600))
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_start_connection_is_cancelled(
    conn: APIConnection, resolve_host, socket_socket
):
    """Test handling of start connection is cancelled."""
    loop = asyncio.get_event_loop()

    with patch.object(loop, "sock_connect", side_effect=asyncio.CancelledError):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await asyncio.sleep(0)
        with pytest.raises(APIConnectionError, match="Starting connection cancelled"):
            await connect_task

    async_fire_time_changed(utcnow() + timedelta(seconds=600))
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_finish_connection_is_cancelled(
    conn: APIConnection, resolve_host, socket_socket
):
    """Test handling of finishing connection being cancelled."""
    loop = asyncio.get_event_loop()

    with patch.object(loop, "create_connection", side_effect=asyncio.CancelledError):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await asyncio.sleep(0)
        with pytest.raises(APIConnectionError, match="Finishing connection cancelled"):
            await connect_task

    async_fire_time_changed(utcnow() + timedelta(seconds=600))
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_finish_connection_times_out(
    plaintext_connect_task_no_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test handling of finish connection timing out."""
    conn, transport, protocol, connect_task = plaintext_connect_task_no_login
    messages = []

    def on_msg(msg):
        messages.append(msg)

    remove = conn.add_message_callback(on_msg, (HelloResponse, DeviceInfoResponse))
    mock_data_received(
        protocol,
        b'\x00@\x02\x08\x01\x10\x07\x1a(m5stackatomproxy (esphome v2023.1.0-dev)"\x10m',
    )
    await asyncio.sleep(0)

    async_fire_time_changed(utcnow() + timedelta(seconds=200))
    await asyncio.sleep(0)

    with pytest.raises(APIConnectionError, match="Hello timed out"):
        await connect_task

    async_fire_time_changed(utcnow() + timedelta(seconds=600))
    await asyncio.sleep(0)

    assert not conn.is_connected
    remove()
    await conn.force_disconnect()
    await asyncio.sleep(0)


@pytest.mark.parametrize(
    ("exception_map"),
    [
        (OSError("Socket error"), HandshakeAPIError),
        (asyncio.TimeoutError, TimeoutAPIError),
        (asyncio.CancelledError, APIConnectionError),
    ],
)
@pytest.mark.asyncio
async def test_plaintext_connection_fails_handshake(
    conn: APIConnection,
    resolve_host: AsyncMock,
    socket_socket: MagicMock,
    exception_map: tuple[Exception, Exception],
) -> None:
    """Test that the frame helper is closed before the underlying socket.

    If we don't do this, asyncio will get confused and not release the socket.
    """
    loop = asyncio.get_event_loop()
    exception, raised_exception = exception_map
    protocol = get_mock_protocol(conn)
    messages = []
    protocol: APIPlaintextFrameHelper | None = None
    transport = MagicMock()
    connected = asyncio.Event()

    class APIPlaintextFrameHelperHandshakeException(APIPlaintextFrameHelper):
        """Plaintext frame helper that raises exception on handshake."""

        def perform_handshake(self, timeout: float) -> Coroutine[Any, Any, None]:
            raise exception

    def _create_mock_transport_protocol(create_func, **kwargs):
        nonlocal protocol
        protocol = create_func()
        protocol.connection_made(transport)
        connected.set()
        return transport, protocol

    def on_msg(msg):
        messages.append(msg)

    remove = conn.add_message_callback(on_msg, (HelloResponse, DeviceInfoResponse))
    transport = MagicMock()

    with patch(
        "aioesphomeapi.connection.APIPlaintextFrameHelper",
        APIPlaintextFrameHelperHandshakeException,
    ), patch.object(
        loop, "create_connection", side_effect=_create_mock_transport_protocol
    ):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await connected.wait()

    assert conn._socket is not None
    assert conn._frame_helper is not None

    mock_data_received(
        protocol,
        b'\x00@\x02\x08\x01\x10\x07\x1a(m5stackatomproxy (esphome v2023.1.0-dev)"\x10m',
    )
    mock_data_received(protocol, b"5stackatomproxy")
    mock_data_received(protocol, b"\x00\x00$")
    mock_data_received(protocol, b"\x00\x00\x04")
    mock_data_received(
        protocol,
        b'\x00e\n\x12\x10m5stackatomproxy\x1a\x11E8:9F:6D:0A:68:E0"\x0c2023.1.0-d',
    )
    mock_data_received(
        protocol, b"ev*\x15Jan  7 2023, 13:19:532\x0cm5stack-atomX\x03b\tEspressif"
    )

    call_order = []

    def _socket_close_call():
        call_order.append("socket_close")

    def _frame_helper_close_call():
        call_order.append("frame_helper_close")

    with patch.object(
        conn._socket, "close", side_effect=_socket_close_call
    ), patch.object(
        conn._frame_helper, "close", side_effect=_frame_helper_close_call
    ), pytest.raises(
        raised_exception
    ):
        await asyncio.sleep(0)
        await connect_task

    # Ensure the frame helper is closed before the socket
    # so asyncio releases the socket
    assert call_order == ["frame_helper_close", "socket_close"]
    assert not conn.is_connected
    assert len(messages) == 2
    assert isinstance(messages[0], HelloResponse)
    assert isinstance(messages[1], DeviceInfoResponse)
    assert messages[1].name == "m5stackatomproxy"
    remove()
    await conn.force_disconnect()
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_connect_wrong_password(
    plaintext_connect_task_with_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_with_login

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, True)

    with pytest.raises(InvalidAuthAPIError):
        await connect_task

    assert not conn.is_connected


@pytest.mark.asyncio
async def test_connect_correct_password(
    plaintext_connect_task_with_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_with_login

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, False)

    await connect_task

    assert conn.is_connected


@pytest.mark.asyncio
async def test_force_disconnect_fails(
    caplog: pytest.LogCaptureFixture,
    plaintext_connect_task_with_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_with_login

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, False)

    await connect_task
    assert conn.is_connected

    with patch.object(protocol, "_writer", side_effect=OSError):
        await conn.force_disconnect()
    assert "Failed to send (forced) disconnect request" in caplog.text


@pytest.mark.asyncio
async def test_disconnect_fails_to_send_response(
    connection_params: ConnectionParams,
    event_loop: asyncio.AbstractEventLoop,
    resolve_host,
    socket_socket,
) -> None:
    loop = asyncio.get_event_loop()
    protocol: APIPlaintextFrameHelper | None = None
    transport = MagicMock()
    connected = asyncio.Event()
    client = APIClient(
        address="mydevice.local",
        port=6052,
        password=None,
    )
    expected_disconnect = None

    async def _on_stop(_expected_disconnect: bool) -> None:
        nonlocal expected_disconnect
        expected_disconnect = _expected_disconnect

    conn = APIConnection(connection_params, _on_stop)

    def _create_mock_transport_protocol(create_func, **kwargs):
        nonlocal protocol
        protocol = create_func()
        protocol.connection_made(transport)
        connected.set()
        return transport, protocol

    with patch.object(event_loop, "sock_connect"), patch.object(
        loop, "create_connection", side_effect=_create_mock_transport_protocol
    ):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await connected.wait()
        send_plaintext_hello(protocol)
        client._connection = conn
        await connect_task
        transport.reset_mock()

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, False)

    await connect_task
    assert conn.is_connected

    with patch.object(protocol, "_writer", side_effect=OSError):
        disconnect_request = DisconnectRequest()
        mock_data_received(protocol, generate_plaintext_packet(disconnect_request))

    # Wait one loop iteration for the disconnect to be processed
    await asyncio.sleep(0)
    assert expected_disconnect is True


@pytest.mark.asyncio
async def test_disconnect_success_case(
    connection_params: ConnectionParams,
    event_loop: asyncio.AbstractEventLoop,
    resolve_host,
    socket_socket,
) -> None:
    loop = asyncio.get_event_loop()
    protocol: APIPlaintextFrameHelper | None = None
    transport = MagicMock()
    connected = asyncio.Event()
    client = APIClient(
        address="mydevice.local",
        port=6052,
        password=None,
    )
    expected_disconnect = None

    async def _on_stop(_expected_disconnect: bool) -> None:
        nonlocal expected_disconnect
        expected_disconnect = _expected_disconnect

    conn = APIConnection(connection_params, _on_stop)

    def _create_mock_transport_protocol(create_func, **kwargs):
        nonlocal protocol
        protocol = create_func()
        protocol.connection_made(transport)
        connected.set()
        return transport, protocol

    with patch.object(event_loop, "sock_connect"), patch.object(
        loop, "create_connection", side_effect=_create_mock_transport_protocol
    ):
        connect_task = asyncio.create_task(connect(conn, login=False))
        await connected.wait()
        send_plaintext_hello(protocol)
        client._connection = conn
        await connect_task
        transport.reset_mock()

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, False)

    await connect_task
    assert conn.is_connected

    disconnect_request = DisconnectRequest()
    mock_data_received(protocol, generate_plaintext_packet(disconnect_request))

    # Wait one loop iteration for the disconnect to be processed
    await asyncio.sleep(0)
    assert expected_disconnect is True
    assert not conn.is_connected


@pytest.mark.asyncio
async def test_ping_disconnects_after_no_responses(
    plaintext_connect_task_with_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_with_login

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, False)

    await connect_task

    ping_request_bytes = b"\x00\x00\x07"

    assert conn.is_connected
    transport.reset_mock()
    expected_calls = []
    start_time = utcnow()
    max_pings_to_disconnect_after = int(KEEP_ALIVE_TIMEOUT_RATIO)
    for count in range(1, max_pings_to_disconnect_after + 1):
        async_fire_time_changed(
            start_time + timedelta(seconds=KEEP_ALIVE_INTERVAL * count)
        )
        assert transport.write.call_count == count
        expected_calls.append(call(ping_request_bytes))
        assert transport.write.mock_calls == expected_calls

    assert conn.is_connected is True

    # We should disconnect once we reach more than 4 missed pings
    async_fire_time_changed(
        start_time
        + timedelta(seconds=KEEP_ALIVE_INTERVAL * (max_pings_to_disconnect_after + 1))
    )
    assert transport.write.call_count == max_pings_to_disconnect_after

    assert conn.is_connected is False


@pytest.mark.asyncio
async def test_ping_does_not_disconnect_if_we_get_responses(
    plaintext_connect_task_with_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_with_login

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, False)

    await connect_task
    ping_request_bytes = b"\x00\x00\x07"

    assert conn.is_connected
    transport.reset_mock()
    start_time = utcnow()
    max_pings_to_disconnect_after = int(KEEP_ALIVE_TIMEOUT_RATIO)
    for count in range(1, max_pings_to_disconnect_after + 2):
        async_fire_time_changed(
            start_time + timedelta(seconds=KEEP_ALIVE_INTERVAL * count)
        )
        send_ping_response(protocol)

    # We should only send 1 ping request if we are getting responses
    assert transport.write.call_count == 1
    assert transport.write.mock_calls == [call(ping_request_bytes)]

    # We should disconnect if we are getting ping responses
    assert conn.is_connected is True


def test_raise_during_send_messages_when_not_yet_connected(conn: APIConnection) -> None:
    """Test that we raise when sending messages before we are connected."""
    with pytest.raises(ConnectionNotEstablishedAPIError):
        conn.send_message(PingRequest())


@pytest.mark.asyncio
async def test_respond_to_ping_request(
    caplog: pytest.LogCaptureFixture,
    plaintext_connect_task_with_login: tuple[
        APIConnection, asyncio.Transport, APIPlaintextFrameHelper, asyncio.Task
    ],
) -> None:
    conn, transport, protocol, connect_task = plaintext_connect_task_with_login

    send_plaintext_hello(protocol)
    send_plaintext_connect_response(protocol, False)

    await connect_task
    assert conn.is_connected

    transport.reset_mock()
    send_ping_request(protocol)
    # We should respond to ping requests
    ping_response_bytes = b"\x00\x00\x08"
    assert transport.write.call_count == 1
    assert transport.write.mock_calls == [call(ping_response_bytes)]
