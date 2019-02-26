from flake8_plugin_utils import Plugin

from .visitors import ReturnVisitor

__version__ = '0.3.0'


class ReturnPlugin(Plugin):
    name = 'flake8-return'
    version = __version__
    visitors = [ReturnVisitor]
