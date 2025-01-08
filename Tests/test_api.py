import pytest
from Integrations.DnDFiveApi import client as dndfiveapi

def test_get_races():
    races = dndfiveapi.get_request('/races')

    assert isinstance(races, list)
    assert len(races) > 0