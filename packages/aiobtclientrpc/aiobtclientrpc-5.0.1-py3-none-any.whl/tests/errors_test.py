import pytest

from aiobtclientrpc import _errors


@pytest.mark.parametrize(
    argnames='a, b, exp_equal',
    argvalues=(
        (_errors.Error('foo'), _errors.Error('foo'), True),
        (_errors.Error('foo'), _errors.Error('bar'), False),
        (_errors.Error('foo'), _errors.RPCError('foo'), True),
        (_errors.Error('foo'), _errors.RPCError('bar'), False),
        (_errors.Error('foo'), ValueError('foo'), NotImplemented),
        (_errors.Error('foo'), ValueError('bar'), NotImplemented),
    ),
    ids=lambda v: repr(v),
)
def test_Error_equality(a, b, exp_equal):
    equal = a.__eq__(b)
    assert equal is exp_equal


@pytest.mark.parametrize(
    argnames='msg, info, exp_repr',
    argvalues=(
        ('foo', None, "RPCError('foo', info=None)"),
        ('foo', 'more info', "RPCError('foo', info='more info')"),
        ('foo', {'arbitrary': 'object'}, "RPCError('foo', info={'arbitrary': 'object'})"),
    ),
    ids=lambda v: repr(v),
)
def test_RPCError(msg, info, exp_repr):
    if info is not None:
        exception = _errors.RPCError(msg, info=info)
    else:
        exception = _errors.RPCError(msg)
    assert repr(exception) == exp_repr


@pytest.mark.parametrize(
    argnames='a, b, exp_equal',
    argvalues=(
        (_errors.RPCError('foo'), _errors.RPCError('foo'), True),
        (_errors.RPCError('foo'), _errors.RPCError('bar'), False),
        (_errors.RPCError('foo', info='my info'), _errors.RPCError('foo', info='my info'), True),
        (_errors.RPCError('foo', info='my info'), _errors.RPCError('foo', info='your info'), False),
        (_errors.RPCError('foo'), _errors.Error('foo'), NotImplemented),
        (_errors.RPCError('foo'), _errors.Error('bar'), NotImplemented),
    ),
    ids=lambda v: repr(v),
)
def test_RPCError_equality(a, b, exp_equal):
    equal = a.__eq__(b)
    assert equal is exp_equal


class TranslationTarget(Exception):
    def __init__(self, *posargs, **kwargs):
        args = []
        if posargs:
            args.append(', '.join(f'{arg!r}' for arg in posargs))
        if kwargs:
            args.append(', '.join(f'{k}={v!r}' for k, v in kwargs.items()))
        super().__init__(', '.join(args))

rpc_exception_map = {
    r'^The environment is perfectly safe$': TranslationTarget(r'RUN FOR YOUR LIVES!'),
    # Positional arguments
    r'^The (\w+) fell (\w+)$': (
        TranslationTarget,
        r'\1:', r'I fell \2!', r'Bugger \2!', 'OK!',
    ),
    # Keyword arguments
    r'^A (?P<what>\w+) hit the (?P<who>\w+)$': (
        TranslationTarget,
        ('who', r'\g<who>'), ('says', r'I was hit by a \g<what>!'), ('but', 'Just kidding.'),
    ),
}

@pytest.mark.parametrize(
    argnames='rpc_error, exp_return_value',
    argvalues=(
        # No references
        (_errors.RPCError('The environment is perfectly safe'), TranslationTarget('RUN FOR YOUR LIVES!')),
        (_errors.RPCError('The environment is toppled over'), _errors.RPCError('The environment is toppled over')),

        # Numbered references in positional arguments
        (_errors.RPCError('The front fell off'), TranslationTarget('front:', 'I fell off!', 'Bugger off!', 'OK!')),
        (_errors.RPCError('The bottom fell down'), TranslationTarget('bottom:', 'I fell down!', 'Bugger down!', 'OK!')),
        (_errors.RPCError('The front escalated quickly'), _errors.RPCError('The front escalated quickly')),

        # Named references in positional arguments
        (_errors.RPCError('A wave hit the ship'), TranslationTarget(who='ship', says='I was hit by a wave!', but='Just kidding.')),
        (_errors.RPCError('A whale hit the blimp'), TranslationTarget(who='blimp', says='I was hit by a whale!', but='Just kidding.')),
        (_errors.RPCError('A whale punched the blimp'), _errors.RPCError('A whale punched the blimp')),
    ),
    ids=lambda v: repr(v),
)
def test_RPCError_translate(rpc_error, exp_return_value):
    return_value = rpc_error.translate(rpc_exception_map)
    assert type(return_value) is type(exp_return_value)
    assert str(return_value) == str(exp_return_value)
