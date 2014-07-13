"""Test the serialize function of Schema."""

import mock

import argo


@mock.patch.object(argo.Attr, 'serialize')
def test_schema_calls_attr(attr_serialize):
    """Test that schema serialize calls attr serialize with the correct value."""
    class S(argo.Schema):

        """Test schema."""

        key = argo.Attr()

    S.serialize({'key': 1})
    attr_serialize.assert_called_once_with({'key': 1})
