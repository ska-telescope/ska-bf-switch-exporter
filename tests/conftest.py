"""
Pytest configuration shared by all test modules.
"""

import logging

import pytest
from prometheus_client import CollectorRegistry


@pytest.hookimpl
def pytest_configure(config: pytest.Config):
    """
    Hook that adds pytest config values dynamically.
    """
    config.addinivalue_line("markers", "debug: Enable debug logging")


@pytest.fixture(name="debug", autouse=True)
def fxt_debug(
    request: pytest.FixtureRequest,
    caplog: pytest.LogCaptureFixture,
):
    """
    Fixture that enables debug logging for tests marked with
    ``@pytest.mark.debug``.
    """
    if request.node.get_closest_marker("debug"):
        caplog.set_level(logging.DEBUG)


@pytest.fixture(name="registry")
def fxt_registry():
    """
    Fixture that creates a new Prometheus registry for each individual test.
    """
    return CollectorRegistry()
