"""Argo basic types."""


class Type(object):

    """Base class for creating types."""

    def __init__(self, validators=None, *args, **kwargs):
        """Type constructor.

        :param validators: A list of :class:`argo.validators.Validator` objects that check the validity of the
            deserialized value. Validators raise :class:`argo.exception.ValidationError` exceptions when
            value is not valid.
        """
        self.validators = validators or []

    def serialize(self, value):
        """Serialization of the value.

        :param value: Value to serialize.
        :return: Serialized value.
        """
        return value

    def deserialize(self, value):
        """Deserialization of the value.

        :param value: Value to deserialize.

        :return: Deserialized value.
        :raises: :class:`argo.exception.ValidationError` when value is not valid.
        """
        if value is not None:
            for validator in self.validators:
                validator.validate(value)

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
        """Create a new List."""
        super(List, self).__init__()
        self.item_type = item_type or Type()

    def serialize(self, value, **kwargs):
        """Overrided serialize for returning list of value's items."""
        return [self.item_type.serialize(val, **kwargs) for val in value]
