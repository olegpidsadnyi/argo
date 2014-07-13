"""Argo basic types."""


class Type(object):

    """Base class for creating types."""

    @classmethod
    def serialize(cls, value):
        """Serialization of value."""
        return value

    @classmethod
    def deserialize(cls, value):
        """Desirialization of value."""
        return value

    @staticmethod
    def is_type(value):
        """Is value an instance or subclass of the class Type."""
        if isinstance(value, type):
            return issubclass(value, Type)
        return isinstance(value, Type)


class List(Type):
    """List type for Argo schema attribute."""

    def __init__(self, item_type=None):
        super(List, self).__init__()
        self.item_type = item_type or Type

    def serialize(self, value):
        """Overrided serialize for returning list of value's items."""
        return [self.item_type.serialize(val) for val in value]
