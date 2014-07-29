"""Argo exceptions."""


class ValidationError(Exception):

    """Validation failed."""

    def __init__(self, errors, attr=None):
        self.attr = attr
        if isinstance(errors, list):
            self.errors = errors
        else:
            self.errors = [errors]

    @staticmethod
    def dump(error):
        if isinstance(error, ValidationError):
            return error.to_dict()
        return error

    def to_dict(self):
        """Dictionary representation of the error."""
        return {
            "errors": dict((e.attr, [self.dump(error) for error in e.errors]) for e in self.errors),
        }
