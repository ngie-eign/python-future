"""
A module that brings in equivalents of the new and modified Python 3
builtins into Py2. Has no effect on Py3.

The builtin functions are:

- ``ascii``
- ``hex``
- ``oct``
- ``chr`` (equivalent to ``unichr`` on Py2)
- ``input`` (equivalent to ``raw_input`` on Py2)
- ``open`` (equivalent to io.open on Py2)

and:
- ``int`` (currently unchanged)

"""

from future import utils

if not utils.PY3:
    from io import open
    from future_builtins import ascii, oct, hex
    from __builtin__ import unichr as chr
    # Was:
    # from __builtin__ import long as int
    # Was this safe? Probably not: it makes isinstance(1, int) == False
    # Stick to this:
    from __builtin__ import int

    # The following seems like a good idea, but it may be a bit
    # paranoid and the implementation may be fragile:

    # Python 2's input() is unsafe and MUST not be able to be used
    # accidentally by someone who expects Python 3 semantics but forgets
    # to import it on Python 2. So we delete it from __builtin__. We
    # keep a copy though:
    import __builtin__
    __builtin__._oldinput = __builtin__.input
    delattr(__builtin__, 'input')

    input = raw_input
    
    __all__ = ['ascii', 'oct', 'hex', 'chr', 'int', 'input', 'open']

else:
    import builtins
    ascii, oct, hex = builtins.ascii, builtins.oct, builtins.hex
    chr = builtins.chr
    int = builtins.int
    input = builtins.input
    open = builtins.open

    __all__ = []

    # From Pandas, for Python versions 3.0 and 3.1 only. The callable()
    # function was removed from Py3.0 and 3.1 and reintroduced into Py3.2.
    try:
        # callable reintroduced in later versions of Python
        callable = callable
    except NameError:
        def callable(obj):
            return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)
        __all__.append('callable')
