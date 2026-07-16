"""pytest plugin: hermeticity enforcement. Any attempt to open a network connection during
the kata suite fails the run — the dataset must be executable fully offline."""

import socket

import pytest


class _NetworkBlocked(RuntimeError):
    pass


def _blocked(*args, **kwargs):
    raise _NetworkBlocked("network access attempted during dataset tests")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    socket.socket.connect = _blocked
    socket.create_connection = _blocked
    socket.getaddrinfo = _blocked
