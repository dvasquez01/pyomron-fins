"""
PyOmron FINS - Python wrapper for OMRON FINS Ethernet protocol
==============================================================

This package provides a Python interface to communicate with OMRON PLCs 
using the FINS Ethernet protocol. It's based on the node-red-contrib-omron-fins
JavaScript library.

Author: GitHub Copilot Assistant
License: MIT
Version: 0.1.0
"""

from .fins_client import FinsClient
from .exceptions import FinsError, ConnectionError, TimeoutError

__version__ = "0.1.0"
__author__ = "GitHub Copilot Assistant"
__license__ = "MIT"

__all__ = [
    "FinsClient",
    "FinsError", 
    "ConnectionError",
    "TimeoutError"
]