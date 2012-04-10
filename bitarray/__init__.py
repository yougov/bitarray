"""
This package defines an object type which can efficiently represent
a bitarray.  Bitarrays are sequence types and behave very much like lists.

Please find a description of this package at:

    http://pypi.python.org/pypi/bitarray/

Author: Ilan Schnell
"""
from bitarray._bitarray import _bitarray, bitdiff, bits2bytes, _sysinfo

__version__ = '0.8.1'


def _tree_insert(tree, sym, ba):
    """
    Insert symbol which is mapped to bitarray into tree
    """
    v = ba[0]
    if len(ba) > 1:
        if tree[v] == []:
            tree[v] = [[], []]
        _tree_insert(tree[v], sym, ba[1:])
    else:
        if tree[v] != []:
            raise ValueError("prefix code ambiguous")
        tree[v] = sym

def _mk_tree(codedict):
    # Generate tree from codedict
    tree = [[], []]
    for sym, ba in codedict.items():
        _tree_insert(tree, sym, ba)
    return tree

def _check_codedict(codedict):
    if not isinstance(codedict, dict):
        raise TypeError("dictionary expected")
    if len(codedict) == 0:
        raise ValueError("prefix code empty")
    for k, v in codedict.items():
        if not isinstance(v, (bitarray, frozenbitarray)):
            raise TypeError("bitarray expected for dictionary value")
        if v.length() == 0:
            raise ValueError("non-empty bitarray expected")


class bitarray(_bitarray):
    """bitarray([initial], [endian=string])

Return a new bitarray object whose items are bits initialized from
the optional initial, and endianness.
If no object is provided, the bitarray is initialized to have length zero.
The initial object may be of the following types:

int, long
    Create bitarray of length given by the integer.  The initial values
    in the array are random, because only the memory allocated.

string
    Create bitarray from a string of '0's and '1's.

list, tuple, iterable
    Create bitarray from a sequence, each element in the sequence is
    converted to a bit using truth value value.

bitarray
    Create bitarray from another bitarray.  This is done by copying the
    memory holding the bitarray data, and is hence very fast.

The optional keyword arguments 'endian' specifies the bit endianness of the
created bitarray object.
Allowed values are 'big' and 'little' (default is 'big').

Note that setting the bit endianness only has an effect when accessing the
machine representation of the bitarray, i.e. when using the methods: tofile,
fromfile, tobytes, frombytes."""

    def fromstring(self, string):
        """fromstring(string)

Append from a string, interpreting the string as machine values.
Deprecated since version 0.4.0, use ``frombytes()`` instead."""
        return self.frombytes(string.encode())

    def tostring(self):
        """tostring() -> string

Return the string representing (machine values) of the bitarray.
When the length of the bitarray is not a multiple of 8, the few remaining
bits (1..7) are set to 0.
Deprecated since version 0.4.0, use ``tobytes()`` instead."""
        return self.tobytes().decode()

    def decode(self, codedict):
        """decode(code) -> list

Given a prefix code (a dict mapping symbols to bitarrays),
decode the content of the bitarray and return the list of symbols."""
        _check_codedict(codedict)
        return self._decode(_mk_tree(codedict))

    def iterdecode(self, codedict):
        """iterdecode(code) -> iterator

Given a prefix code (a dict mapping symbols to bitarrays),
decode the content of the bitarray and iterate over the symbols."""
        _check_codedict(codedict)
        return self._iterdecode(_mk_tree(codedict))

    def encode(self, codedict, iterable):
        """encode(code, iterable)

Given a prefix code (a dict mapping symbols to bitarrays),
iterates over iterable object with symbols, and extends the bitarray
with the corresponding bitarray for each symbols."""
        _check_codedict(codedict)
        self._encode(codedict, iterable)

    def __hash__(self):
        raise TypeError("unhashable type: 'bitarray.bitarray'")


class frozenbitarray(_bitarray):
    """bitarray([initial], [endian=string])

Creates a frozenbitarray object, which is very much like the bitarray object,
except that it is immutable, and therefore hashable."""

    def __repr__(self):
        return 'frozen' + _bitarray.__repr__(self)

    # the following methods need to be made unavailable,
    # as they may mutate the object

    def append(self, item):
        raise NotImplementedError

    def bytereverse(self):
        raise NotImplementedError

    def extend(self, arg):
        raise NotImplementedError

    def _encode(self):
        raise NotImplementedError

    def fill(self):
        raise NotImplementedError

    def fromfile(self, n=0):
        raise NotImplementedError

    def frombytes(self, bytes):
        raise NotImplementedError

    def insert(self, i, item):
        raise NotImplementedError

    def invert(self):
        raise NotImplementedError

    def pack(self, bytes):
        raise NotImplementedError

    def pop(self, i=0):
        raise NotImplementedError

    def remove(self, item):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def setall(self, v):
        raise NotImplementedError

    def sort(self, reverse=False):
        raise NotImplementedError

    def __delitem__(self, arg):
        raise NotImplementedError

    def __setitem__(self, *args):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def __imul__(self, num):
        raise NotImplementedError

    def __iand__(self, other):
        raise NotImplementedError

    def __ior__(self, other):
        raise NotImplementedError

    def __ixor__(self, other):
        raise NotImplementedError

    def __invert__(self):
        raise NotImplementedError


def test(verbosity=1, repeat=1):
    """test(verbosity=1, repeat=1) -> TextTestResult

Run self-test, and return unittest.runner.TextTestResult object.
"""
    from bitarray import test_bitarray
    return test_bitarray.run(verbosity=verbosity, repeat=repeat)
