import imp

error = False
try:
    import __version__ as version
except:
    from . import __version__ as version
    error = True

if not error:
    __version__ 	= version.version
__email__		= "licface@yahoo.com"
__author__		= "licface@yahoo.com"

from .cmdw import *