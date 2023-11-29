"""
This module contains main Singleton class
"""

class SingletonMeta(type):
    """
    The Singleton meta class
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Check for new updates with __init__ method
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
