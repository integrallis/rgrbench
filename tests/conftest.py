"""Deterministic randomness: any test that draws from the global `random` module gets a
seed derived from its own node ID, so outcomes are stable regardless of execution order."""

import random
import zlib

import pytest


@pytest.fixture(autouse=True)
def _seed_random(request):
    random.seed(zlib.crc32(request.node.nodeid.encode()))
