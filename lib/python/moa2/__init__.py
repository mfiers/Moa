"""
Version 2 of the moa python library
"""

from moa2.job import Job
from moa2.config import Config
from moa2.pluginHandler import PluginHandler
from moa2 import logger

#convenience functions
def getLogger(name):
    return logger.getLogger(name)
