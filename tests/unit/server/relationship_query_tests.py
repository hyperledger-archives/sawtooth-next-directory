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
""" Unit Tests for rbac/server/db/roles_query.py"""
import pytest

from rbac.server.db.relationships_query import fetch_relationship_query

ROLE_RELATIONSHIP_CASES = [
    (
        "admins",
        "158fa3c5-5d73-4dbf-9426-84e8b090efd6",
        "r.table(role_admins).filter({{role_id: 158fa3c5-5d73-4dbf-9426-84e8b090efd6}})"
        ".get_field(related_id).coerce_to(array)",
    ),
    (
        "owners",
        "158fa3c5-5d73-4dbf-9426-84e8b090efd6",
        "r.table(role_owners).filter({{role_id: 158fa3c5-5d73-4dbf-9426-84e8b090efd6}})"
        ".get_field(related_id).coerce_to(array)",
    ),
    (
        "members",
        "158fa3c5-5d73-4dbf-9426-84e8b090efd6",
        "r.table(role_members).filter({{role_id: 158fa3c5-5d73-4dbf-9426-84e8b090efd6}})"
        ".get_field(related_id).coerce_to(array)",
    ),
]


@pytest.mark.parametrize(
    "relationship, role_id, expected_result", ROLE_RELATIONSHIP_CASES
)
def test_fetch_relationship_query(relationship, role_id, expected_result):
    """" Tests valid cases when using fetch_relationship_query()
    Args:
        relationship:
            str: String dictating the role relationship to fetch: admins,
            owners, or members.
        role_id:
            str: UUID4 formatted id of the role.
        expected_result:
            str: RethinkDB query to fetch the role relationship
    """
    result = fetch_relationship_query(relationship, role_id)
    assert result == expected_result


def test_invalid_relationship_query():
    """ Tests invalid case when using fetch_relationship_query()"""
    payload = {
        "relationship": "superheroes",
        "role_id": "158fa3c5-5d73-4dbf-9426-84e8b090efd6",
    }
    with pytest.raises(ValueError):
        fetch_relationship_query(
            relationship=payload["relationship"], role_id=payload["role_id"]
        )
