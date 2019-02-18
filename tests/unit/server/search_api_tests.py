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
# ------------------------------------------------------------------------------
import pytest

from rbac.server.api.search import (
    get_total_pages,
    search_paginate,
    validate_search_payload,
)

PAGINATION_TEST_CASES = [
    (20, 1, (0, 20)),
    (5, 3, (10, 15)),
    (0, 1, (0, 50)),
    (30, 0, (0, 30)),
    (-20, -5, (0, 50)),
]
TOTALS_TEST_CASES = [
    ([], 50, 0),
    ([45, 3, 2], 50, 1),
    ([700, 720, 613], 50, 15),
    ([0, 55, 2], 50, 2),
]


@pytest.mark.parametrize("page_size,page_num,expected_result", PAGINATION_TEST_CASES)
def test_search_paginate(page_size, page_num, expected_result):
    """Test search_paginate with various input cases."""
    result = search_paginate(page_size, page_num)
    assert result == expected_result


def test_paginate_no_inputs():
    """Test search_paginate with no parameters submitted. (Default pagination)."""
    result = search_paginate()
    assert result == (0, 50)


@pytest.mark.parametrize("size_list,page_size,expected_result", TOTALS_TEST_CASES)
def test_get_total_pages(size_list, page_size, expected_result):
    """Test total pages function to get the max number of pages from all query result sizes."""
    result = get_total_pages(size_list, page_size)
    assert result == expected_result


def test_get_total_no_inputs():
    """Test get_total_pages with no parameters submitted. (Default 0)."""
    result = search_paginate()
    assert result == (0, 50)


def test_validate_search():
    """Test validate_search_payload works with a good payload."""
    payload = {"search_input": "The input", "search_object_types": []}
    result = validate_search_payload(payload)
    assert result == {}


def test_validate_search_no_query():
    """Test validation of an empty value for search query."""
    result = validate_search_payload(None)
    assert result["errors"] == "No query parameter received."


def test_validate_search_no_input():
    """Test validation of an empty value for search_input."""
    payload = {"search_object_types": []}
    result = validate_search_payload(payload)
    assert result["errors"] == "No search_input string for search received."


def tests_validate_search_no_types():
    """Test validation of an empty value for search_object types."""
    payload = {"search_input": "The input"}
    result = validate_search_payload(payload)
    assert result["errors"] == "No search_object_types for search received."
