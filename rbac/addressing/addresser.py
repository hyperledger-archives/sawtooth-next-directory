# Copyright 2018 Contributors to Hyperledger Sawtooth
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
import re
import enum
from hashlib import sha512


class SysAdminNamespace(enum.IntEnum):
    SYS_ADMIN_START = 0
    SYS_ADMIN_STOP = 1


class RoleNamespace(enum.IntEnum):
    ROLE_START = 1
    ROLE_STOP = 24


class TaskNamespace(enum.IntEnum):
    TASK_START = 24
    TASK_STOP = 49


class UserNamespace(enum.IntEnum):
    USER_START = 49
    USER_STOP = 149


class ProposalNamespace(enum.IntEnum):
    PROPOSAL_START = 149
    PROPOSAL_STOP = 255


class SysAdminRelationshipNS(enum.IntEnum):
    SYSADMIN_MEMBERS_START = 1
    SYSADMIN_MEMBERS_STOP = 200
    SYSADMIN_OWNERS_START = 200
    SYSADMIN_OWNERS_STOP = 225
    SYSADMIN_ADMINS_START = 225
    SYSADMIN_ADMINS_STOP = 255


class RoleRelationshipNamespace(enum.IntEnum):
    ROLE_ATTRIBUTES_START = 0
    ROLE_ATTRIBUTES_STOP = 1
    ROLE_MEMBER_START = 1
    ROLE_MEMBER_STOP = 125
    ROLE_OWNER_START = 125
    ROLE_OWNER_STOP = 175
    ROLE_TASK_START = 175
    ROLE_TASK_STOP = 225
    ROLE_ADMIN_START = 225
    ROLE_ADMIN_STOP = 255


class TaskRelationshipNamespace(enum.IntEnum):
    TASK_ATTRIBUTES_START = 0
    TASK_ATTRIBUTES_STOP = 1
    TASK_OWNER_START = 1
    TASK_OWNER_STOP = 50
    TASK_ADMIN_START = 50
    TASK_ADMIN_STOP = 100


FAMILY_NAME = "rbac"
FAMILY_VERSION = "1.0"
NS = sha512(FAMILY_NAME.encode()).hexdigest()[:6]
FAMILY_PREFIX = "9f4448"
ADDRESS_LENGTH = 70
ADDRESS_PATTERN = re.compile(r"^[0-9a-f]{70}$")
FAMILY_PATTERN = re.compile(r"^9f4448[0-9a-f]{64}$")


@enum.unique
class AddressSpace(enum.Enum):
    USER = 1
    PROPOSALS = 2

    SYSADMIN_ATTRIBUTES = 3
    SYSADMIN_MEMBERS = 4
    SYSADMIN_OWNERS = 5
    SYSADMIN_ADMINS = 6
    ROLES_ATTRIBUTES = 7
    ROLES_MEMBERS = 8
    ROLES_OWNERS = 9
    ROLES_ADMINS = 10
    ROLES_TASKS = 11

    TASKS_ATTRIBUTES = 12
    TASKS_OWNERS = 13
    TASKS_ADMINS = 14


def _contains(num, start, stop):
    return start <= num < stop


def namespace_ok(address):
    return address[: len(NS)] == NS


def is_address(address):
    """Determines the address is a valid Sawtooth address
       (a 70 character hexadecimal string)

    Args:
        address (str): A 70 character state address.

    Returns: Boolean

    """
    return bool(ADDRESS_PATTERN.match(address))


def is_family_address(address):
    """Determines the address is a valid Sawtooth address
       with the correct family prefix.

    Args:
        address (str): A 70 character state address.

    Returns: Boolean

    """
    return bool(FAMILY_PATTERN.match(address))


def address_is(address):
    """Determines the type of object stored at the address.

    Args:
        address (str): A 70 character state address.

    Returns: AddressSpace enum identifying the part of state.

    """
    if not FAMILY_PATTERN.match(address):
        raise ValueError(
            "Address %s isn't part of the %s namespace", address, FAMILY_NAME
        )

    addr1 = int(address[len(NS) : len(NS) + 2], base=16)

    if _contains(
        addr1, SysAdminNamespace.SYS_ADMIN_START, SysAdminNamespace.SYS_ADMIN_STOP
    ):
        return _sysadmin_address_is(address)
    elif _contains(addr1, RoleNamespace.ROLE_START, RoleNamespace.ROLE_STOP):
        return _role_address_is(address)
    elif _contains(addr1, TaskNamespace.TASK_START, TaskNamespace.TASK_STOP):
        return _task_address_is(address)
    elif _contains(addr1, UserNamespace.USER_START, UserNamespace.USER_STOP):
        return AddressSpace.USER
    elif _contains(
        addr1, ProposalNamespace.PROPOSAL_START, ProposalNamespace.PROPOSAL_STOP
    ):
        return AddressSpace.PROPOSALS
    else:
        raise ValueError("Unable to determine state location of address %s", address)


def _sysadmin_address_is(address):
    token = address[-2:]
    num = int(token, base=16)

    if _contains(num, 0, 1):
        return AddressSpace.SYSADMIN_ATTRIBUTES
    elif _contains(
        num,
        SysAdminRelationshipNS.SYSADMIN_MEMBERS_START,
        SysAdminRelationshipNS.SYSADMIN_MEMBERS_STOP,
    ):
        return AddressSpace.SYSADMIN_MEMBERS
    elif _contains(
        num,
        SysAdminRelationshipNS.SYSADMIN_OWNERS_START,
        SysAdminRelationshipNS.SYSADMIN_OWNERS_STOP,
    ):
        return AddressSpace.SYSADMIN_OWNERS
    elif _contains(
        num,
        SysAdminRelationshipNS.SYSADMIN_ADMINS_START,
        SysAdminRelationshipNS.SYSADMIN_ADMINS_STOP,
    ):
        return AddressSpace.SYSADMIN_ADMINS


def _role_address_is(address):
    token = address[-2:]
    num = int(token, base=16)

    if _contains(
        num,
        RoleRelationshipNamespace.ROLE_ATTRIBUTES_START,
        RoleRelationshipNamespace.ROLE_ATTRIBUTES_STOP,
    ):
        return AddressSpace.ROLES_ATTRIBUTES

    elif _contains(
        num,
        RoleRelationshipNamespace.ROLE_MEMBER_START,
        RoleRelationshipNamespace.ROLE_MEMBER_STOP,
    ):
        return AddressSpace.ROLES_MEMBERS
    elif _contains(
        num,
        RoleRelationshipNamespace.ROLE_OWNER_START,
        RoleRelationshipNamespace.ROLE_OWNER_STOP,
    ):
        return AddressSpace.ROLES_OWNERS
    elif _contains(
        num,
        RoleRelationshipNamespace.ROLE_TASK_START,
        RoleRelationshipNamespace.ROLE_TASK_STOP,
    ):
        return AddressSpace.ROLES_TASKS
    elif _contains(
        num,
        RoleRelationshipNamespace.ROLE_ADMIN_START,
        RoleRelationshipNamespace.ROLE_ADMIN_STOP,
    ):
        return AddressSpace.ROLES_ADMINS
    else:
        raise ValueError(
            "Unable to determine state location of address %s"
            " within the Role namespace",
            address,
        )


def _task_address_is(address):
    token = address[-2:]
    num = int(token, base=16)
    if _contains(
        num,
        TaskRelationshipNamespace.TASK_ATTRIBUTES_START,
        TaskRelationshipNamespace.TASK_ATTRIBUTES_STOP,
    ):
        return AddressSpace.TASKS_ATTRIBUTES
    elif _contains(
        num,
        TaskRelationshipNamespace.TASK_OWNER_START,
        TaskRelationshipNamespace.TASK_OWNER_STOP,
    ):
        return AddressSpace.TASKS_OWNERS
    elif _contains(
        num,
        TaskRelationshipNamespace.TASK_ADMIN_START,
        TaskRelationshipNamespace.TASK_ADMIN_STOP,
    ):
        return AddressSpace.TASKS_ADMINS
    else:
        raise ValueError(
            "Unable to determine state location of address %s"
            " within the Task namespace",
            address,
        )


def _compress(object_id, start, limit):
    return "%.2X".lower() % (
        int(sha512(object_id.encode()).hexdigest(), base=16) % limit + start
    )


def _make_role_address(role_id):
    return (
        NS
        + _compress(
            role_id,
            RoleNamespace.ROLE_START,
            RoleNamespace.ROLE_STOP - RoleNamespace.ROLE_START,
        )
        + sha512(role_id.encode()).hexdigest()[:60]
    )


def _make_task_address(task_id):
    return (
        NS
        + _compress(
            task_id,
            TaskNamespace.TASK_START,
            TaskNamespace.TASK_STOP - TaskNamespace.TASK_START,
        )
        + sha512(task_id.encode()).hexdigest()[:60]
    )


def make_user_address(user_id):
    return (
        NS
        + _compress(
            user_id,
            UserNamespace.USER_START,
            UserNamespace.USER_STOP - UserNamespace.USER_START,
        )
        + sha512(user_id.encode()).hexdigest()[:62]
    )


def make_proposal_address(object_id, related_id):
    return (
        NS
        + _compress(
            object_id,
            ProposalNamespace.PROPOSAL_START,
            ProposalNamespace.PROPOSAL_STOP - ProposalNamespace.PROPOSAL_START,
        )
        + sha512(object_id.encode()).hexdigest()[:31]
        + sha512(related_id.encode()).hexdigest()[:31]
    )


def _make_sysadmin_address():
    return NS + "0" * 62


def make_sysadmin_attr_address():
    return _make_sysadmin_address() + "00"


def make_sysadmin_members_address(user_id):
    return _make_sysadmin_address() + _compress(
        user_id,
        SysAdminRelationshipNS.SYSADMIN_MEMBERS_START,
        SysAdminRelationshipNS.SYSADMIN_MEMBERS_STOP
        - SysAdminRelationshipNS.SYSADMIN_MEMBERS_START,
    )


def make_sysadmin_owners_address(user_id):
    return _make_sysadmin_address() + _compress(
        user_id,
        SysAdminRelationshipNS.SYSADMIN_OWNERS_START,
        SysAdminRelationshipNS.SYSADMIN_OWNERS_STOP
        - SysAdminRelationshipNS.SYSADMIN_OWNERS_START,
    )


def make_sysadmin_admins_address(user_id):
    return _make_sysadmin_address() + _compress(
        user_id,
        SysAdminRelationshipNS.SYSADMIN_ADMINS_START,
        SysAdminRelationshipNS.SYSADMIN_ADMINS_STOP
        - SysAdminRelationshipNS.SYSADMIN_ADMINS_START,
    )


def make_role_attributes_address(role_id):
    return _make_role_address(role_id) + "00"


def make_role_members_address(role_id, user_id):
    return _make_role_address(role_id) + _compress(
        user_id,
        RoleRelationshipNamespace.ROLE_MEMBER_START,
        RoleRelationshipNamespace.ROLE_MEMBER_STOP
        - RoleRelationshipNamespace.ROLE_MEMBER_START,
    )


def make_role_tasks_address(role_id, task_id):
    return _make_role_address(role_id) + _compress(
        task_id,
        RoleRelationshipNamespace.ROLE_TASK_START,
        RoleRelationshipNamespace.ROLE_TASK_STOP
        - RoleRelationshipNamespace.ROLE_TASK_START,
    )


def make_role_owners_address(role_id, user_id):
    return _make_role_address(role_id) + _compress(
        user_id,
        RoleRelationshipNamespace.ROLE_OWNER_START,
        RoleRelationshipNamespace.ROLE_OWNER_STOP
        - RoleRelationshipNamespace.ROLE_OWNER_START,
    )


def make_role_admins_address(role_id, user_id):
    return _make_role_address(role_id) + _compress(
        user_id,
        RoleRelationshipNamespace.ROLE_ADMIN_START,
        RoleRelationshipNamespace.ROLE_ADMIN_STOP
        - RoleRelationshipNamespace.ROLE_ADMIN_START,
    )


def make_task_attributes_address(task_id):
    return _make_task_address(task_id=task_id) + "00"


def make_task_owners_address(task_id, user_id):
    return _make_task_address(task_id) + _compress(
        user_id,
        TaskRelationshipNamespace.TASK_OWNER_START,
        TaskRelationshipNamespace.TASK_OWNER_STOP
        - TaskRelationshipNamespace.TASK_OWNER_START,
    )


def make_task_admins_address(task_id, user_id):
    return _make_task_address(task_id) + _compress(
        user_id,
        TaskRelationshipNamespace.TASK_ADMIN_START,
        TaskRelationshipNamespace.TASK_ADMIN_STOP
        - TaskRelationshipNamespace.TASK_ADMIN_START,
    )
