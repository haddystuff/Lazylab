"""Base class you have to inherit from when adding qcow2 support"""
from abc import ABC


class BaseQcowSupport(ABC):
    """
    qcow2 support is in BaseManageVM class so we don't neet to rewrite methods
    here
    """
    pass

