import re


class Error(Exception):
    """Base class for all exceptions raised by this package"""

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return str(self) == str(other)
        else:
            return NotImplemented


class RPCError(Error):
    """
    Generic RPC error

    This can be some kind of miscommunication with the RPC service (e.g. unknown
    method called, invalid or missing argument, etc), which should be a
    considered a bug. But it can also be a normal error message (e.g. unknown
    torrent), that should be communicated to the user.
    """

    def __init__(self, msg, info=None):
        super().__init__(msg)
        self._info = info

    @property
    def info(self):
        """
        """
        return self._info

    def __repr__(self):
        return f'{type(self).__name__}({str(self)!r}, info={self._info!r})'

    def __eq__(self, other):
        equal = super().__eq__(other)
        if equal is True and hasattr(other, 'info'):
            return other.info == self.info
        else:
            return equal

    def translate(self, map):
        # By using r-string we don't have to escape backslashes
        r"""
        Turn this exception into another one based on regular expressions

        :param map: Mapping of regular expression strings to target exception
            instances

        Each regular expression is matched aagainst the error message of the
        instance (i.e. ``str(self)``). The corresponding target exception of the
        first matching regular expression is returned.

        >>> RPCError("foo is bad").translate({
        >>>     r"^foo": ValueError("Foo is something"),
        >>>     r"is bad$": TypeError("Something is bad"),
        >>> })
        ValueError('bad: Foo')

        If there are no matches, the instance (``self``) is returned.

        >>> RPCError("foo is bad").translate({
        >>>     r"Hello?": ValueError("Anybody out there?"),
        >>> })
        RPCError("foo is bad")

        If the matching target exception is a ``(exception_class, message)``
        tuple, any group references in ``message`` are substituted with the
        groups from the matching regular expression and
        ``exception_class(message_with_group_substitutions)`` is returned.

        >>> for e in (RPCError("foo is bad"), RPCError("bar is good"), RPCError("baz is silly")):
        >>>     e.translate({
        >>>         r"^(\w+) is (\w+)$": (ValueError, r"\2: \1"),
        >>>     })
        ValueError('bad: foo')
        ValueError('good: bar')
        ValueError('silly: baz')

        Keyword arguments are also supported:

        >>> for e in (RPCError("foo is bad"), RPCError("bar is good"), RPCError("baz is silly")):
        >>>     e.translate({
        >>>         r"^(\w+) is (\w+)$": (SomeError, r"\1", kwarg=r"\2"),
        >>>     })
        SomeError('foo', kwarg='bad')
        SomeError('bar', kwarg='good')
        SomeError('baz', kwarg='silly')
        """
        self_msg = str(self)
        for regex, to_exc in map.items():
            match = re.search(regex, self_msg)
            if match:
                if isinstance(to_exc, tuple) and len(to_exc) >= 2:
                    # Split `to_exc` into exception class and its arguments with
                    # group references
                    to_cls, *to_args = to_exc

                    # Split `to_args` into positional and keyword arguments
                    to_posargs = tuple(
                        match.expand(arg)  # Replace group references (\1, \g<1>, \g<name>)
                        for arg in to_args
                        if not isinstance(arg, tuple)
                    )
                    to_kwargs = {
                        k: match.expand(v)  # Replace group references (\1, \g<1>, \g<name>)
                        for k, v in (a for a in to_args if isinstance(a, tuple))
                    }
                    return to_cls(*to_posargs, **to_kwargs)
                else:
                    return to_exc
        return self


class ConnectionError(Error):
    """Failed to connect to the client, e.g. because it isn't running"""

    def __init__(self, msg):
        # python_socks.ProxyConnectionError provides ugly errors messages,
        # e.g. "Could not connect to proxy localhost:1337 [None]".
        msg = re.sub(r'\s+\[.*?\]$', '', str(msg))
        super().__init__(msg)


class TimeoutError(Error, TimeoutError):
    """
    Timeout for sending request and reading response

    Besides :class:`Error`, this is also a subclass of the builtin
    :class:`~exceptions.TimeoutError`.
    """


class AuthenticationError(Error):
    """Failed to prove identity"""


class ValueError(Error, ValueError):
    """
    Invalid value (e.g. port 65536)

    Besides :class:`Error`, this is also a subclass of the builtin
    :class:`~exceptions.ValueError`.
    """
