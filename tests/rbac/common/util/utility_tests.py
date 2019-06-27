# Copyright 2019 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
"""Test the common utility functions"""
import pytest

# pylint: disable=redefined-outer-name,missing-docstring
from rbac.common.util import get_attribute
from rbac.common.util import bytes_from_hex
from rbac.common.util import has_duplicates
from rbac.common.util import duplicates
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


@pytest.fixture
def test_object():
    class TestObject:
        @property
        def test_property(self):
            return "bar"

        def test_method(self):
            return "foobar"

    return TestObject()


@pytest.mark.utility
@pytest.mark.library
def test_get_attribute(test_object):
    """Tests that get_attribute will:
    1. return the value of a property, if it exists
    2. return a reference to a method, if it exists
    3. return None if a property or method does not exist
    """
    assert get_attribute(test_object, "test_property") == "bar"
    assert callable(get_attribute(test_object, "test_method"))
    assert get_attribute(test_object, "test_method")() == "foobar"
    assert get_attribute(test_object, "no_property") is None


@pytest.mark.utility
@pytest.mark.library
def test_bytes_from_hex():
    """Tests that bytes_from_hex will:
    1. return the byte representation of a hexadecimal string
    2. return None if None is passed to it
    """
    assert bytes_from_hex("abee01") == b"\xab\xee\x01"
    assert bytes_from_hex(None) is None


@pytest.mark.utility
@pytest.mark.library
def test_has_duplicates():
    """Tests that has_duplicates will:
    1. return True if a list has duplicate values
    2. return False if a list contains only unique values
    3. return False if a list is empty
    4. raise a ValueError if a non-list datatype is provided to it
    """
    assert has_duplicates([1, 2, 7, 3, 4, 1]) is True
    assert has_duplicates(["a", "b", "e", "a", "oscar"]) is True
    assert has_duplicates([4, 3, 7, 8, 34, 1]) is False
    assert has_duplicates(["a", "b", "e", "f", "oscar"]) is False
    assert has_duplicates([]) is False

    with pytest.raises(ValueError):
        assert has_duplicates(None)
    with pytest.raises(ValueError):
        assert has_duplicates(20)
    with pytest.raises(ValueError):
        assert has_duplicates("foo")
    with pytest.raises(ValueError):
        assert has_duplicates({1, 5, 6, 9, 2})


@pytest.mark.utility
@pytest.mark.library
def test_duplicates():
    """Tests that duplicates will:
    1. return a list of duplicate values contained in a list
    2. return an empty list if a list contains only unique values
    3. return an empty list if a list is empty
    4. raise a ValueError if a non-list datatype is provided to it
    """
    assert duplicates([1, 2, 7, 3, 4, 1]) == [1]
    assert duplicates(["a", "b", "e", "a", "oscar"]) == ["a"]
    assert duplicates([4, 3, 7, 8, 34, 1]) == []
    assert duplicates(["a", "b", "e", "f", "oscar"]) == []
    assert duplicates([]) == []

    with pytest.raises(ValueError):
        assert duplicates(None)
    with pytest.raises(ValueError):
        assert duplicates(20)
    with pytest.raises(ValueError):
        assert duplicates("foo")
