from argparse import Action


class Handler:
    """Base class for handlers"""

    appname = None

    @classmethod
    def named(cls, name):
        """Subclass of the handler that holds the app name as a closure"""
        class NamedHandler(cls):
            appname = name
        return NamedHandler
