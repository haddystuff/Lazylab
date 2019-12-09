"""Base class you have to inherit from when adding persistency support"""
from abc import ABC


class BasePersistencySupport(ABC):
    """
    Persistency support is in BaseManageVM class so we don't neet to rewrite
    methods here
    """
    pass
