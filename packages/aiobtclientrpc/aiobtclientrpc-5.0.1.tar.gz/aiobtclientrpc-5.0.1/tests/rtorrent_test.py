import asyncio
import re
import sys
import xmlrpc
from unittest.mock import Mock, call

import pytest

from aiobtclientrpc import RPCBase, _errors, _rtorrent, _utils

from .common import AsyncMock, make_url_parts


@pytest.mark.parametrize(
    argnames='url, exp',
    argvalues=(
        # Default URL
        ('',
         {'scheme': 'scgi', 'host': '127.0.0.1', 'port': '5000', 'path': None, 'username': None, 'password': None}),

        # RPC socket path
        ('/abs/path/to/rpc.socket',
         {'scheme': 'file', 'host': None, 'port': None, 'path': '/abs/path/to/rpc.socket', 'username': None, 'password': None}),
        ('file:///path/to/rpc.socket',
         {'scheme': 'file', 'host': None, 'port': None, 'path': '/path/to/rpc.socket', 'username': None, 'password': None}),
        ('file://foo:bar@path/to/rpc.socket',
         {'scheme': 'file', 'host': None, 'port': None, 'path': 'foo:bar@path/to/rpc.socket', 'username': None, 'password': None}),
        ('file://path:123/to/rpc.socket',
         {'scheme': 'file', 'host': None, 'port': None, 'path': 'path:123/to/rpc.socket', 'username': None, 'password': None}),

        # SCGI
        ('myhost',
         {'scheme': 'scgi', 'host': 'myhost', 'port': '5000', 'path': None, 'username': None, 'password': None}),
        ('myhost:123',
         {'scheme': 'scgi', 'host': 'myhost', 'port': '123', 'path': None, 'username': None, 'password': None}),
        ('scgi://myhost:123',
         {'scheme': 'scgi', 'host': 'myhost', 'port': '123', 'path': None, 'username': None, 'password': None}),

        # HTTP(s)
        ('http://myhost:123',
         {'scheme': 'http', 'host': 'myhost', 'port': '123', 'path': None, 'username': None, 'password': None}),
        ('http://foo:bar@myhost:123',
         {'scheme': 'http', 'host': 'myhost', 'port': '123', 'path': None, 'username': 'foo', 'password': 'bar'}),
        ('https://foo:bar@myhost:123/RPC123',
         {'scheme': 'https', 'host': 'myhost', 'port': '123', 'path': '/RPC123', 'username': 'foo', 'password': 'bar'}),
        ('https://foo:bar@myhost',
         {'scheme': 'https', 'host': 'myhost', 'port': '5000', 'path': None, 'username': 'foo', 'password': 'bar'}),
        ('https://myhost/RPC/17',
         {'scheme': 'https', 'host': 'myhost', 'port': '5000', 'path': '/RPC/17', 'username': None, 'password': None}),

        # Invalid scheme
        ('arf://myhost',
         _errors.ValueError('Scheme must be "file", "scgi", "http" or "https"')),

        # Invalid scgi URL
        ('scgi://foo:@myhost',
         _errors.ValueError("scgi URLs don't have a username")),
        ('scgi://:foo@myhost',
         _errors.ValueError("scgi URLs don't have a password")),
        ('scgi://myhost/this/is/a/path',
         _errors.ValueError("scgi URLs don't have a path")),
    ),
    ids=lambda v: str(v),
)
def test_RtorrentURL(url, exp):
    if isinstance(exp, Exception):
        with pytest.raises(type(exp), match=rf'^{re.escape(str(exp))}$'):
            _rtorrent.RtorrentURL(url)
    else:
        url = _rtorrent.RtorrentURL(url)
        assert make_url_parts(url) == exp


class AsyncIterator:
    def __init__(self, items):
        self._items = list(items)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._items:
            return self._items.pop(0)
        else:
            raise StopAsyncIteration


@pytest.mark.parametrize('url', (None, 'http://a:b@foo:123'))
@pytest.mark.parametrize(
    argnames='kwargs',
    argvalues=(
        {},
        {'scheme': 'https'},
        {'host': 'asdf'},
        {'port': '123'},
        {'scheme': 'http', 'username': 'this', 'password': 'that'},
        {'timeout': 123},
        {'proxy_url': 'http://hey:ho@bar:456'},
    ),
    ids=lambda v: str(v),
)
def test_RtorrentRPC_instantiation(kwargs, url):
    if url:
        kwargs['url'] = url
    rpc = _rtorrent.RtorrentRPC(**kwargs)

    default_url = _utils.URL(_rtorrent.RtorrentURL.default)
    exp_url = _utils.URL(_rtorrent.RtorrentURL.default)
    if url:
        custom_url = _utils.URL(url)
    for name in ('scheme', 'host', 'port', 'path', 'username', 'password'):
        if name in kwargs:
            exp_value = kwargs[name]
        elif url:
            exp_value = getattr(custom_url, name)
        else:
            exp_value = getattr(default_url, name)
        actual_value = getattr(rpc.url, name)
        assert actual_value == exp_value
        setattr(exp_url, name, exp_value)

    assert rpc.url == exp_url
    assert rpc.timeout == kwargs.get('timeout', RPCBase.default_timeout)
    if 'proxy_url' in kwargs:
        assert rpc.proxy_url == _utils.URL(kwargs['proxy_url'])
    else:
        assert rpc.proxy_url is None

@pytest.mark.parametrize(
    argnames='kwargs, exp_error',
    argvalues=(
        ({'url': 'bar:baz'}, 'Invalid port'),
        ({'port': (1, 2, 3)}, 'Invalid port'),
        ({'scheme': 'file', 'host': 'localhost'}, "file URLs don't have a host"),
        ({'timeout': 'never'}, 'Invalid timeout'),
        ({'proxy_url': 'foo://bar:baz'}, 'Invalid port'),
    ),
    ids=lambda v: str(v),
)
def test_RtorrentRPC_instantiation_with_invalid_argument(kwargs, exp_error):
    with pytest.raises(_errors.ValueError, match=rf'^{re.escape(exp_error)}$'):
        _rtorrent.RtorrentRPC(**kwargs)


@pytest.mark.parametrize('proxy_url', (None, 'http://a:b@proxy.local'))
@pytest.mark.asyncio
async def test_RtorrentRPC_connect(proxy_url, mocker):
    rpc = _rtorrent.RtorrentRPC(proxy_url=proxy_url)
    mocker.patch.object(rpc, '_disconnect', AsyncMock())
    AsyncServerProxy_mock = mocker.patch('aiobtclientrpc._rtorrent._AsyncServerProxy')
    mocker.patch.object(rpc, '_call', AsyncMock())

    await rpc._connect()

    assert rpc._disconnect.call_args_list == [call()]

    if proxy_url:
        assert AsyncServerProxy_mock.call_args_list == [call(
            url=rpc.url,
            proxy_url=rpc.proxy_url,
        )]
    else:
        assert AsyncServerProxy_mock.call_args_list == [call(
            url=rpc.url,
            proxy_url=None,
        )]

    assert rpc._call.call_args_list == [call('system.pid')]


@pytest.mark.parametrize('xmlrpc', (None, AsyncMock()))
@pytest.mark.asyncio
async def test_RtorrentRPC_disconnect(xmlrpc):
    rpc = _rtorrent.RtorrentRPC()
    if xmlrpc is not None:
        rpc._xmlrpc = xmlrpc

    await rpc._disconnect()

    if xmlrpc:
        assert xmlrpc.close.call_args_list == [call()]

    assert not hasattr(rpc, '_xmlrpc')


@pytest.mark.parametrize(
    argnames='raised_exception, exp_exception',
    argvalues=(
        (
            xmlrpc.client.ProtocolError('http://url', 401, 'Something went wrong', {'head': 'ers'}),
            _errors.AuthenticationError('Authentication failed'),
        ),
        (
            xmlrpc.client.ProtocolError('http://url', 123, 'Something went wrong', {'head': 'ers'}),
            _errors.RPCError('Something went wrong'),
        ),
        (
            xmlrpc.client.Fault(123, 'Something else went wrong'),
            _errors.RPCError('Something else went wrong'),
        ),
        (
            None,
            None,
        ),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_RtorrentRPC_call(raised_exception, exp_exception, mocker):
    rpc = _rtorrent.RtorrentRPC()
    rpc._xmlrpc = Mock(call=Mock())
    catch_connection_exceptions_mock = mocker.patch('aiobtclientrpc._utils.catch_connection_exceptions', AsyncMock())
    if raised_exception:
        catch_connection_exceptions_mock.side_effect = raised_exception

    method = 'some_method'
    args = ('foo', 'bar', 'baz')

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            await rpc._call(method, *args)
    else:
        return_value = await rpc._call(method, *args)
        assert return_value is catch_connection_exceptions_mock.return_value

    assert catch_connection_exceptions_mock.call_args_list == [call(rpc._xmlrpc.call.return_value)]
    assert rpc._xmlrpc.call.call_args_list == [call(method, *args)]


@pytest.mark.parametrize(
    argnames='calls, responses, kwargs, exp_result, exp_system_multicall_called',
    argvalues=(
        (
            [('foo', 'a', 'b'), ['bar'], ('baz', 123, '456'), ('foo', 'f00')],
            [['first response'], {'faultString': 'Bad!'}, [789], ['00']],
            {'raise_errors': False},
            ['first response', _errors.RPCError('Bad!'), 789, '00'],
            True,
        ),
        (
            [('foo', 'a', 'b'), ['bar'], ('baz', 123, '456'), ('foo', 'f00')],
            [['first response'], [['b', 'a', 'r']], {'faultString': 'Bad!'}, ['00']],
            {'raise_errors': True},
            _errors.RPCError('Bad!'),
            True,
        ),
        (
            [('foo', 'a', 'b'), ['bar'], ('baz', 123, '456'), ('foo', 'f00')],
            [['first response'], {'faultString': 'Bad!'}, [789], ['00']],
            {'raise_errors': False, 'as_dict': True},
            RuntimeError("Multiple foo calls: foo('a', 'b'), foo('f00')"),
            False,
        ),
        (
            [('foo', 'a', 'b'), ['bar'], ('baz', 123, '456')],
            [['first response'], {'faultString': 'Bad!'}, [789]],
            {'raise_errors': False, 'as_dict': True},
            {'foo': 'first response', 'bar': _errors.RPCError('Bad!'), 'baz': 789},
            True,
        ),
        (
            [('foo', 'a', 'b'), ['bar'], ('baz', 123, '456')],
            [['first response'], {'faultString': 'Bad!'}, [789]],
            {'raise_errors': True, 'as_dict': True},
            _errors.RPCError('Bad!'),
            True,
        ),
        (
            [('foo', 'a', 'b'), ['bar'], ('baz', 123, '456')],
            [['first response'], 'unexpected return value', [789]],
            {},
            RuntimeError("Unexpected response: 'unexpected return value'"),
            True,
        ),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_RtorrentRPC__multicall_rt(calls, responses, kwargs, exp_result, exp_system_multicall_called, mocker):
    rpc = _rtorrent.RtorrentRPC()
    mocker.patch.object(rpc, 'call', AsyncMock(return_value=responses))

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await rpc._multicall_rt(*calls, **kwargs)
    else:
        return_value = await rpc._multicall_rt(*calls, **kwargs)
        assert return_value == exp_result

    if exp_system_multicall_called:
        assert rpc.call.call_args_list == [call('system.multicall', [
            {'methodName': method, 'params': params}
            for method, *params in calls
        ])]
    else:
        assert rpc.call.call_args_list == []


@pytest.mark.parametrize(
    argnames='supported_methods, candidates, exp_method, exp_exception',
    argvalues=(
        (
            ('foo', 'bar', 'baz'),
            ('bar', 'baz'),
            'bar',
            None,
        ),
        (
            ('foo', 'bar', 'baz'),
            ('asdf', 'f00'),
            None,
            _errors.ValueError("Unsupported method(s): 'asdf', 'f00'"),
        ),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_RtorrentRPC_get_supported_method(supported_methods, candidates, exp_method, exp_exception, mocker):
    rpc = _rtorrent.RtorrentRPC()
    mocker.patch.object(rpc, 'call', AsyncMock(return_value=supported_methods))

    if not type(rpc)._supported_methods:
        exp_calls = [call('system.listMethods')]
    else:
        exp_calls = []

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            await rpc.get_supported_method(*candidates)
    else:
        # Multiple get_supported_method() calls, but only one "system.list_method" request
        for _ in range(3):
            return_value = await rpc.get_supported_method(*candidates)
            assert return_value == exp_method

    assert rpc.call.call_args_list == exp_calls


@pytest.mark.parametrize('proxy_url', (None, _utils.URL('http://proxy.local')))
@pytest.mark.parametrize(
    argnames='url, exp_transport, exp_exception',
    argvalues=(
        (_utils.URL('http://foo.local:123'), '_HttpTransport', None),
        (_utils.URL('https://foo.local:123'), '_HttpTransport', None),
        (_utils.URL('scgi://foo.local:123'), '_ScgiHostTransport', None),
        (_utils.URL('file://path/to/socket'), '_ScgiSocketTransport', None),
        (_utils.URL('foo://bar.baz'), None, _errors.ValueError('Unsupported protocol: foo://bar.baz')),
    ),
    ids=lambda v: str(v),
)
def test_AsyncServerProxy(url, exp_transport, exp_exception, proxy_url, mocker):
    transport_mocks = {
        '_HttpTransport': mocker.patch('aiobtclientrpc._rtorrent._HttpTransport'),
        '_ScgiHostTransport': mocker.patch('aiobtclientrpc._rtorrent._ScgiHostTransport'),
        '_ScgiSocketTransport': mocker.patch('aiobtclientrpc._rtorrent._ScgiSocketTransport'),
    }

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            _rtorrent._AsyncServerProxy(url, proxy_url)
    else:
        if str(url).startswith('file://') and proxy_url:
            with pytest.raises(_errors.ValueError, match=rf'^You cannot use a proxy to connect to {url}$'):
                _rtorrent._AsyncServerProxy(url, proxy_url)
        else:
            proxy = _rtorrent._AsyncServerProxy(url, proxy_url)
            assert proxy._transport is transport_mocks[exp_transport].return_value

            if str(url).startswith('file://'):
                assert transport_mocks[exp_transport].call_args_list == [
                    call(url=url),
                ]
            elif proxy_url:
                assert transport_mocks[exp_transport].call_args_list == [
                    call(url=url, proxy_url=proxy_url),
                ]
            else:
                assert transport_mocks[exp_transport].call_args_list == [
                    call(url=url, proxy_url=None),
                ]


@pytest.mark.asyncio
async def test_AsyncServerProxy_call(mocker):
    proxy = _rtorrent._AsyncServerProxy(_utils.URL('http://foo.baz'))

    dumps_mock = mocker.patch('xmlrpc.client.dumps')
    convert_to_basic_type_mock = mocker.patch('aiobtclientrpc._utils.convert_to_basic_type')
    mocker.patch.object(proxy._transport, 'request', Mock())
    mocker.patch.object(proxy, '_parse_response', AsyncMock())

    return_value = await proxy.call('foo', 'bar', 'baz')
    assert return_value is proxy._parse_response.return_value
    assert proxy._parse_response.call_args_list == [call(proxy._transport.request.return_value)]
    assert proxy._transport.request.call_args_list == [call(dumps_mock.return_value.encode.return_value)]
    assert dumps_mock.call_args_list == [call(
        convert_to_basic_type_mock.return_value,
        'foo',
        encoding='utf-8',
        allow_none=False,
    )]
    assert dumps_mock.return_value.encode.call_args_list == [call('utf-8', 'xmlcharrefreplace')]


@pytest.mark.parametrize(
    argnames='u_close_return_value, exp_return_value',
    argvalues=(
        (['single return value'], 'single return value'),
        (['multiple', 'return values'], ['multiple', 'return values']),
    ),
)
@pytest.mark.asyncio
async def test_AsyncServerProxy_parse_response(u_close_return_value, exp_return_value, mocker):
    proxy = _rtorrent._AsyncServerProxy(_utils.URL('http://foo.baz'))

    mocks = Mock()
    mocks.u.close.return_value = u_close_return_value
    mocker.patch('xmlrpc.client.getparser', return_value=(mocks.p, mocks.u))

    async def chunk_generator():
        for chunk in ('foo', 'bar', 'baz'):
            yield chunk

    chunks = chunk_generator()
    return_value = await proxy._parse_response(chunks)
    assert return_value == exp_return_value
    assert mocks.mock_calls == [
        call.p.feed('foo'),
        call.p.feed('bar'),
        call.p.feed('baz'),
        call.p.close(),
        call.u.close(),
    ]


@pytest.mark.asyncio
async def test_AsyncServerProxy_close(mocker):
    proxy = _rtorrent._AsyncServerProxy(_utils.URL('http://foo.baz'))
    mocker.patch.object(proxy._transport, 'close', AsyncMock())
    assert proxy._transport.close.call_args_list == []
    await proxy.close()
    assert proxy._transport.close.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='url, proxy_url, exp_url, exp_exception',
    argvalues=(
        (_utils.URL('file://path/to/proxy'), None, None, _errors.ValueError('Unsupported protocol: file')),
        (_utils.URL('http://a:b@foo.bar:123'), None, 'http://foo.bar:123/RPC2', None),
        (_utils.URL('http://a:b@foo.bar:123/custom/path'), None, 'http://foo.bar:123/custom/path', None),
        (_utils.URL('http://a:b@foo.bar/path'), _utils.URL('http://a:b@proxy'), 'http://foo.bar/path', None),
        (_utils.URL('https://foo.bar'), _utils.URL('https://proxy'), 'https://foo.bar/RPC2', None),
    ),
)
def test_HttpTransport(url, proxy_url, exp_url, exp_exception, mocker):
    create_http_client_mock = mocker.patch('aiobtclientrpc._utils.create_http_client', Mock())

    url = _utils.URL(url)
    if proxy_url:
        proxy_url = _utils.URL(proxy_url)

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            _rtorrent._HttpTransport(url, proxy_url=proxy_url)
    else:
        transport = _rtorrent._HttpTransport(url, proxy_url=proxy_url)
        assert transport._url == exp_url
        assert transport._http_client is create_http_client_mock.return_value
        assert isinstance(transport._request_lock, asyncio.Lock)

        if proxy_url:
            assert create_http_client_mock.call_args_list == [call(
                auth=(url.username, url.password),
                proxy_url=proxy_url.with_auth,
            )]
        else:
            assert create_http_client_mock.call_args_list == [call(
                auth=(url.username, url.password),
                proxy_url=None,
            )]


@pytest.mark.asyncio
async def test_HttpTransport_request_and_close(mocker):
    transport = _rtorrent._HttpTransport(_utils.URL('http://foo'))
    chunks = ('a', 'b', 'c')
    delays = (0.1, 0.2, 0.3)
    aiterator = AsyncIterator(chunks)
    mocks = Mock(
        aclose=AsyncMock(),
        _request=Mock(return_value=aiterator),
    )
    mocker.patch.object(transport._http_client, 'aclose', mocks.aclose)
    mocker.patch.object(transport, '_request', mocks._request)

    async def make_request(data):
        exp_chunks = list(chunks)
        my_delays = list(delays)
        async for x in transport.request(data):
            assert x == exp_chunks.pop(0)
            await asyncio.sleep(my_delays.pop(0))

    calls = [
        make_request('foo'),
        transport.close(),
        make_request('bar'),
        transport.close(),
        make_request('baz'),
        transport.close(),
    ]
    await asyncio.gather(*calls)

    # Even though each requested chunk is is received after an increasing delay,
    # and close() calls are not delayed at all, calls should be made in the same
    # order as they were dispatched.
    assert mocks.mock_calls == [
        call._request('foo'),
        call.aclose(),
        call._request('bar'),
        call.aclose(),
        call._request('baz'),
        call.aclose(),
    ]


@pytest.mark.parametrize(
    argnames='url, exp_url, status_code, reason_phrase, headers, raises',
    argvalues=(
        ('http://foo', 'http://foo/RPC2', 200, None, None, False),
        ('http://foo', 'http://foo/RPC2', 123, 'No such method', {'foo': 'bar'}, True),
    ),
)
@pytest.mark.asyncio
# I don't know how to mock async context managers in Python < 3.8.
@pytest.mark.skipif(sys.version_info < (3, 8), reason='requires Python 3.8 or higher')
async def test_HttpTransport_request(url, exp_url, status_code, reason_phrase, headers, raises, mocker):
    transport = _rtorrent._HttpTransport(_utils.URL(url))
    chunks = ('a', 'b', 'c')
    aiterator = AsyncIterator(chunks)
    response = Mock(
        aiter_bytes=Mock(return_value=aiterator),
        status_code=status_code,
        reason_phrase=reason_phrase,
        headers=headers,
    )

    # IMPORTANT: Tests pass without this, but any exception raised in
    #            HttpTransport._request() is ignored unless we explicitly raise
    #            it in __aexit__().
    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        if exc_value:
            raise exc_value

    mocker.patch.object(transport._http_client, 'stream', return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=response),
        __aexit__=__aexit__,
    ))

    mock_data = 'mock data'
    exp_chunks = list(chunks)

    if raises:
        exp_exception = xmlrpc.client.ProtocolError(
            url=exp_url,
            errcode=status_code,
            errmsg=reason_phrase,
            headers=headers,
        )
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            async for chunk in transport._request(mock_data):
                pass
            assert exp_chunks != []

    else:
        async for chunk in transport._request(mock_data):
            assert chunk is exp_chunks.pop(0)
        assert exp_chunks == []

    assert transport._http_client.stream.call_args_list == [call('POST', transport._url, content=mock_data)]


@pytest.mark.asyncio
async def test_ScgiTransportBase_close(mocker):
    class ScgiTestTransport(_rtorrent._ScgiTransportBase):
        _get_reader_writer = AsyncMock()

    transport = ScgiTestTransport()
    await transport.close()

@pytest.mark.asyncio
async def test_ScgiTransportBase_request(mocker):
    mock_reader, mock_writer = Mock(), Mock()

    class ScgiTestTransport(_rtorrent._ScgiTransportBase):
        _get_reader_writer = AsyncMock(return_value=(mock_reader, mock_writer))

    chunks = ('foo', 'bar', 'baz')
    transport = ScgiTestTransport()
    mocker.patch.object(transport, '_send', AsyncMock())
    mocker.patch.object(transport, '_read', Mock(return_value=AsyncIterator(chunks)))

    mocks = Mock(
        _get_reader_writer=transport._get_reader_writer,
        _send=transport._send,
        _read=transport._read,
    )

    mock_data = 'mock data'
    exp_chunks = list(chunks)
    async for cunk in transport.request(mock_data):
        assert cunk is exp_chunks.pop(0)
    assert exp_chunks == []

    assert mocks.mock_calls == [
        call._get_reader_writer(),
        call._send(mock_writer, mock_data),
        call._read(mock_reader, mock_writer, 1024),
    ]

@pytest.mark.parametrize('payload_length', range(1, 16))
@pytest.mark.parametrize('headers_length', range(1, 16))
@pytest.mark.parametrize('chunk_size', (8,))
@pytest.mark.asyncio
async def test_ScgiTransportBase_read(chunk_size, headers_length, payload_length, mocker):
    headers = (b'Status: 200 OK\r\n' * headers_length)[:headers_length]
    print('headers:', headers)
    assert len(headers) == headers_length

    payload = (b'mock payload ' * payload_length)[:payload_length]
    print('payload:', payload)
    assert len(payload) == payload_length

    headers_delim = b'\r\n\r\n'
    stream = headers + headers_delim + payload
    print('stream:', stream)
    stream_chunks = [stream[i:i + chunk_size]
                     for i in range(0, len(stream), chunk_size)]
    print('stream chunks:', stream_chunks)

    first_payload_chunk_size = chunk_size - ((len(headers) + len(headers_delim)) % chunk_size)
    print('first_payload_chunk_size:', first_payload_chunk_size)
    first_payload_chunk = payload[:first_payload_chunk_size]
    print('first_payload_chunk:', first_payload_chunk)
    remaining_payload_chunks = [
        payload[i:i + chunk_size]
        for i in range(len(first_payload_chunk), len(payload), chunk_size)
    ]
    print('remaining_payload_chunks:', remaining_payload_chunks)
    exp_payload_chunks = [first_payload_chunk] + remaining_payload_chunks
    print('exp_payload_chunks:', exp_payload_chunks)

    def get_next_chunk(given_chunk_size, _my_stream_chunks=list(stream_chunks)):
        assert given_chunk_size == chunk_size
        if _my_stream_chunks:
            return _my_stream_chunks.pop(0)
        else:
            return b''

    mocks = Mock(
        read=AsyncMock(side_effect=get_next_chunk),
        close=Mock(),
        wait_closed=AsyncMock(),
    )
    mock_reader = Mock(read=mocks.read)
    mock_writer = Mock(close=mocks.close, wait_closed=mocks.wait_closed)

    class ScgiTestTransport(_rtorrent._ScgiTransportBase):
        _get_reader_writer = AsyncMock(return_value=(mock_reader, mock_writer))

    transport = ScgiTestTransport()
    async for chunk in transport._read(mock_reader, mock_writer, chunk_size):
        print('read chunk:', chunk)
        assert chunk == exp_payload_chunks.pop(0)
    assert exp_payload_chunks == []

    assert mocks.mock_calls == (
        [call.read(chunk_size)] * (len(stream_chunks) + 1)
        + [call.close(), call.wait_closed()]
    )


@pytest.mark.asyncio
async def test_ScgiTransportBase_send(mocker):
    class ScgiTestTransport(_rtorrent._ScgiTransportBase):
        _get_reader_writer = AsyncMock()

    transport = ScgiTestTransport()

    mocks = Mock(
        _encode_request=Mock(),
        write=Mock(),
        drain=AsyncMock(),
    )
    mocker.patch.object(transport, '_encode_request', mocks._encode_request)
    writer = Mock(
        write=mocks.write,
        drain=mocks.drain,
    )
    data = 'mock data'

    await transport._send(writer, data)

    assert mocks.mock_calls == [
        call._encode_request(data),
        call.write(mocks._encode_request.return_value),
        call.drain(),
    ]


@pytest.mark.parametrize(
    argnames='data, path',
    argvalues=(
        (b'foo', b'/RPC2'),
        (b'bar', b'/RPC3'),
    ),
)
def test_ScgiTransportBase_encode_request(data, path):
    class ScgiTestTransport(_rtorrent._ScgiTransportBase):
        _get_reader_writer = AsyncMock()
        _path = path

    exp_headers = (
        b'CONTENT_LENGTH\x003\x00'
        b'SCGI\x001\x00'
        b'REQUEST_METHOD\x00POST\x00'
        b'REQUEST_URI\x00' + path + b'\x00'
    )
    exp_request = (str(len(exp_headers)).encode() + b':' + exp_headers + b',' + data)

    transport = ScgiTestTransport()
    request = transport._encode_request(data)
    assert request == exp_request


@pytest.mark.parametrize(
    argnames='url, exp_host, exp_port, exp_path, proxy_url, exp_exception',
    argvalues=(
        ('http://foo:123', None, None, None, None, _errors.ValueError('Unsupported protocol: http')),
        ('scgi://foo', None, None, None, None, _errors.ValueError('No port specified')),
        ('scgi://foo:123', 'foo', 123, b'/RPC2', None, None),
        ('scgi://foo:123/bar', 'foo', 123, b'/bar', None, None),
        ('scgi://foo:123', 'foo', 123, b'/RPC2', 'http://proxy', None),
    ),
)
def test_ScgiHostTransport(url, exp_host, exp_port, exp_path, proxy_url, exp_exception):
    url = _utils.URL(url)
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            _rtorrent._ScgiHostTransport(url, proxy_url)
    else:
        transport = _rtorrent._ScgiHostTransport(url, proxy_url)
        assert isinstance(transport, _rtorrent._ScgiTransportBase)
        assert transport._host == exp_host
        assert transport._port == exp_port
        assert transport._path == exp_path
        assert transport._proxy_url is proxy_url


@pytest.mark.parametrize(
    argnames='proxy_url, host, port, exception, exp_exception',
    argvalues=(
        ('http://proxy', 'localhost', 123, ValueError('Bad URL'), _errors.ValueError('Bad URL')),
        ('http://proxy', 'localhost', 123, None, None),
        ('http://a:b@proxy', 'localhost', 123, None, None),
        (None, 'localhost', 123, None, None),
    ),
)
@pytest.mark.asyncio
async def test_ScgiHostTransport_get_reader_writer(proxy_url, host, port, exception, exp_exception, mocker):
    transport = _rtorrent._ScgiHostTransport(
        url=_utils.URL(f'scgi://{host}:{port}'),
        proxy_url=_utils.URL(proxy_url) if proxy_url else None,
    )

    if exception:
        Proxy_from_url_mock = mocker.patch('python_socks.async_.asyncio.Proxy.from_url',
                                           side_effect=exception)
    else:
        Proxy_from_url_mock = mocker.patch('python_socks.async_.asyncio.Proxy.from_url', return_value=Mock(
            connect=AsyncMock(return_value='mock sock'),
        ))
    reader_mock, writer_mock = Mock(), Mock()
    open_connection_mock = mocker.patch('asyncio.open_connection', AsyncMock(
        return_value=(reader_mock, writer_mock),
    ))

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            await transport._get_reader_writer()
    else:
        reader, writer = await transport._get_reader_writer()
        assert reader is reader_mock
        assert writer is writer_mock
        if proxy_url:
            assert Proxy_from_url_mock.call_args_list == [call(proxy_url)]
            assert Proxy_from_url_mock.return_value.connect.call_args_list == [call(
                dest_host=host,
                dest_port=port,
                timeout=float('inf'),
            )]
            assert open_connection_mock.call_args_list == [call(
                sock='mock sock',
            )]
        else:
            assert open_connection_mock.call_args_list == [call(
                host=host,
                port=port,
            )]


@pytest.mark.parametrize(
    argnames='url, exp_socket_path, exp_path, exp_exception',
    argvalues=(
        ('http://path/to/socket', None, None, _errors.ValueError('Unsupported protocol: http')),
        ('file://relative/path/to/socket', 'relative/path/to/socket', b'/RPC2', None),
        ('file:///absolute/path/to/socket', '/absolute/path/to/socket', b'/RPC2', None),
    ),
)
def test_ScgiSocketTransport(url, exp_socket_path, exp_path, exp_exception):
    print(url, exp_socket_path, exp_path, exp_exception)

    url = _utils.URL(url)
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            _rtorrent._ScgiSocketTransport(url)
    else:
        transport = _rtorrent._ScgiSocketTransport(url)
        assert isinstance(transport, _rtorrent._ScgiTransportBase)
        assert transport._socket_path == exp_socket_path
        assert transport._path == exp_path


@pytest.mark.asyncio
async def test_ScgiSocketTransport_get_reader_writer(mocker):
    transport = _rtorrent._ScgiSocketTransport(_utils.URL('file:///path/to/socket'))
    reader_mock, writer_mock = Mock(), Mock()
    open_unix_connection_mock = mocker.patch('asyncio.open_unix_connection', AsyncMock(
        return_value=(reader_mock, writer_mock),
    ))

    reader, writer = await transport._get_reader_writer()

    assert reader is reader_mock
    assert writer is writer_mock
    assert open_unix_connection_mock.call_args_list == [call(path='/path/to/socket')]
