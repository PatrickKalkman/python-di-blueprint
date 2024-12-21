"""
Python DI Blueprint - A educational implementation of a Dependency Injection container.

This package demonstrates core DI concepts including composition, lifecycle management,
and interception through practical implementation.
"""

from .composition import SimpleContainer
from .composition import Lifetime

__version__ = "0.1.0"
__author__ = "Patrick Kalkman"

# Expose key classes at package level for cleaner imports
__all__ = ["SimpleContainer", "Lifetime"]
