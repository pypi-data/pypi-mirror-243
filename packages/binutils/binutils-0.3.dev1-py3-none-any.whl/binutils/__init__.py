"""binutils

Python Binary Tools

Note:

    This project is in beta stage.

Viewing documentation using IPython
-----------------------------------
To see which functions are available in `binutils`, type ``binutils.<TAB>`` (where
``<TAB>`` refers to the TAB key), or use ``binutils.*get_version*?<ENTER>`` (where
``<ENTER>`` refers to the ENTER key) to narrow down the list.  To view the
docstring for a function, use ``binutils.get_version?<ENTER>`` (to view the
docstring) and ``binutils.get_version??<ENTER>`` (to view the source code).
"""

import importlib.metadata

from binutils.core import int_to_little_endian_bytes
from binutils.core import little_endian_bytes_to_int
from binutils.core import pretty_hex_str
from binutils.core import int_to_bits
from binutils.core import int_to_bits_str
from binutils.core import bits_to_int
from binutils.core import swap_bytes
from binutils.core import swap_bits_in_bytes
from binutils.core import set_lsb_to_zero
from binutils.core import set_lsb_to_one
from binutils.core import toggle_lsb
from binutils.core import is_lsb_one
from binutils.core import extract_integer_from_bits


# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
# X.Y
# X.Y.Z # For bugfix releases  
# 
# Admissible pre-release markers:
# X.YaN # Alpha release
# X.YbN # Beta release         
# X.YrcN # Release Candidate   
# X.Y # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = importlib.metadata.version("binutils")

def get_version():
    return __version__

__all__ = []
