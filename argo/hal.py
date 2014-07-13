"""HAL related attributes."""

from . import schema
from . import types


BYPASS = lambda value: value


class Link(schema.Attr):

    """Link attribute of a schema."""

    def __init__(self, attr_type=None, attr=None, key=None, required=True, curie=None, templated=None, type=None):
        """Link constructor.

        :param attr_type: Type, Schema or constant that does the type conversion of the attribute.
        :param attr: Attribute name, dot-separated attribute path or an `Accessor` instance.
        :param key: Key of the link in the _links compartment, defaults to name.
        :param required: Is this link required to be present.
        :param curie: Link namespace prefix (e.g. "<prefix>:<name>") or Curie object.
        :param templated: Is this link templated.
        :param type: Its value is a string used as a hint to indicate the media type expected when dereferencing
                           the target resource.
        """
        if not types.Type.is_type(attr_type):

            if attr_type is not None:
                attr = BYPASS

            attrs = {
                'templated': templated,
                'type': type,
            }

            class LinkSchema(schema.Schema):
                href = schema.Attr(attr_type=attr_type, attr=BYPASS)

                if attrs['templated'] is not None:
                    templated = schema.Attr(attr=lambda value: templated)

                if attrs['type'] is not None:
                    type = schema.Attr(attr=lambda value: type)

            attr_type = LinkSchema

        super(Link, self).__init__(attr_type=attr_type, attr=attr, required=required)
        self.curie = curie
        self._key = key

    @property
    def compartment(self):
        """Return the compartment in which Links are placed (_links)."""
        return "_links"

    @property
    def key(self):
        """The key of the this attribute will be placed into (within it's compartment).

        :note: Links support curies.
        """
        if self.curie is None:
            return self._key or self.name
        return ":".join((self.curie.name, self.name))

    def deserialize(self, value):
        """Link doesn't support deserialization."""
        raise NotImplementedError


class LinkList(Link):

    """List of links attribute of a schema."""

    def __init__(self, attr_type=None, attr=None, required=True, curie=None):
        """LinkList constructor.

        :param attr_type: Type, Schema or constant that does item type conversion of the attribute.
        :param attr: Attribute name, dot-separated attribute path or an `Accessor` instance.
        :param required: Is this list of links required to be present.
        :param curie: Link namespace prefix (e.g. "<prefix>:<name>") or Curie object.
        """
        super(LinkList, self).__init__(attr_type=attr_type, attr=attr, required=required, curie=curie)
        self.attr_type = types.List(self.attr_type)


class Curie(object):

    """Curie object."""

    def __init__(self, name, href, templated=None, type=None):
        """Curie constructor.

        :param href: Curie link href value.
        :param templated: Is this curie link templated.
        :param type: Its value is a string used as a hint to indicate the media type expected when dereferencing
                     the target resource.
        """
        self.name = name
        self.href = href

        if templated is not None:
            self.templated = templated

        if type is not None:
            self.type = type


class Embedded(schema.Attr):

    """Embedded attribute of schema."""

    def __init__(self, attr_type=None, attr=None, curie=None):
        """Embedded constructor.

        :param attr_type: Type, Schema or constant that does the type conversion of the attribute.
        :param attr: Attribute name, dot-separated attribute path or an `Accessor` instance.
        :param curie: The curie used for this embedded attribute.
        """
        super(Embedded, self).__init__(attr_type, attr)
        self.curie = curie

    @property
    def compartment(self):
        """Embedded objects are placed in the _objects."""
        return "_embedded"

    @property
    def key(self):
        """Embedded supports curies."""
        if self.curie is None:
            return self.name
        return ":".join((self.curie.name, self.name))


class _SchemaType(schema._SchemaType):

    """HAL schema implementation with CURIEs support."""

    def __init__(cls, name, bases, clsattrs):
        super(_SchemaType, cls).__init__(cls, name, bases, clsattrs)
        curies = set([])

        # Collect CURIEs
        for attr in cls.__class_attrs__:
            if isinstance(attr, (Link, Embedded)):
                curie = getattr(attr, "curie", None)
                if curie is not None:
                    curies.add(curie)

        # Collect CURIEs and create the link attribute
        if curies:
            link = LinkList(
                schema.Schema(
                    href=schema.Attr(),
                    name=schema.Attr(),
                    templated=schema.Attr(required=False),
                    type=schema.Attr(required=False),
                ),
                attr=lambda value: list(curies),
                required=False,
            )
            link.name = "curies"

            cls.__class_attrs__.append(link)
            cls.__attrs__.append(link)


Schema = _SchemaType("Schema", (schema._Schema, ), {"__doc__": schema._Schema.__doc__})
