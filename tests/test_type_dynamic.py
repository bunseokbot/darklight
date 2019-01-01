from utils.type.dynamic import DynamicObject

import pytest


def test_empty_dynamic():
    do = DynamicObject()
    assert do


def test_dict_dynamic():
    do = DynamicObject({'a': 'aaa'})
    assert do.a == 'aaa'


def test_remove_object():
    do = DynamicObject({'a': 'test', 'b': 'test2'})
    assert do.pop('a') == 'test'

    with pytest.raises(Exception):
        assert do.a

    assert do.b


def test_empty_data():
    do = DynamicObject()
    assert do.is_empty() == True
