
from .base_loader import BaseLoader
from .loader import YamlLoader, JsonLoader
from . import api

__version__ = "1.0.0"
__license__ = "MIT"
__author__ = "GoodAdvice"
__email__ = "nigel@goodadvice.it"
__description__ = "A simple YAML configuration loader for Python"
__all__ = [
    "api",
    'BaseLoader',
    'YamlLoader',
    'JsonLoader',
]

