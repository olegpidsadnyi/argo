"""Test configuration."""

import mock
import pytest
from fixtures.common import *


@pytest.fixture(scope="session")
def mocked_get_context():
    """Mock argo.schema._get_context for returning empty dict."""
    patcher = mock.patch("argo.schema._get_context")
    patcher.start()
    patcher.return_value = {}
