"""Halogen basic type validators."""

from argo import exceptions


class Validator(object):

    """Base validator."""

    @classmethod
    def validate(cls, value):
        """Validate the value.

        :param value: Value to validate.

        :raises: :class:`halogen.exception.ValidationError` exception when value is invalid.
        """


class Length(Validator):

    """Length validator that checks the length of a List-like type."""

    def __init__(self, min=None, max=None):
        """Length validator constructor.

        :param min_length: Minimum length, optional.
        :param max_length: Maximum length, optional.
        """
        self.min = min
        self.max = max

    def validate(self, value):
        """Validate the length of a list.

        :param value: List of values.

        :raises: :class:`halogen.exception.ValidationError` exception when length of the list is less than
            minimum or greater than maximum.
        """
        try:
            length = len(value)
        except TypeError:
            length = 0

        if self.min is not None and length < self.min:
            raise exceptions.ValidationError("Length is less than {0}".format(self.min))

        if self.max is not None and length > self.max:
            raise exceptions.ValidationError("Length is greater than {0}".format(self.max))


class Range(object):

    """Range validator."""

    def __init__(self, min=None, max=None):
        """Range validator constructor.

        :param min: Minimal value of range, optional.
        :param max: Maximal value of range, optional.
        """
        self.min = min
        self.max = max

    def validate(self, value):
        """Validate value.

        :param value: Value which should be validated.

        :raises: :class:`argo.exception.ValidationError` exception when either if value less than min in case when
            min is not None or if value greater than max in case when max is not None.
        """
        if self.min is not None:
            if value < self.min:
                raise exceptions.ValidationError("Value is less than minimum value '{0}'.".format(self.min))

        if self.max is not None:
            if value > self.max:
                raise exceptions.ValidationError("Value is greater than maximum value '{0}'.".format(self.max))
