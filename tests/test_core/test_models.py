import pytest
from core.models import Ratio


def test_ratio_up():
    r = Ratio(500)
    assert r.up(1001) == 1500
    assert r.up(1500) == 1500
    assert r.up(0) == 0
    assert r.up(1) == 500


def test_ratio_down():
    r = Ratio(1000)
    assert r.down(1999) == 1000
    assert r.down(2000) == 2000
    assert r.down(500) == 0
