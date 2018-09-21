#! /usr/bin/env python3

# Copyright 2018 The Sawtooth NEXT Directory Authors
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

# http://docs.python-requests.org/en/master/

import requests
import json

HEADERS = {"Content-Type": "application/json"}


def insert_test_data():
    """Inserts test users, managers, roles for demo and experimentation.

      Builds out an example user, manager, role structure by making rest calls against the NEXT api.
    """

    print("Inserting test data...")

    response_create_current_manager = create_user('currentManager')
    print('Created current manager:', response_create_current_manager)

    id_current_manager = response_create_current_manager['data']['user']['id']

    response_create_other_manager = create_user('otherManager')
    id_other_manager = response_create_other_manager['data']['user']['id']

    print('Created other manager:', response_create_other_manager)

    additional_managers = 5
    print('Adding an additional {} managers...'.format(additional_managers))
    for i in range(additional_managers):
        create_user('manager' + str(i))

    response_create_staff = create_user('staff', id_current_manager)
    id_staff = response_create_staff['data']['user']['id']

    print('Created staff:', response_create_staff)

    auth_current_manager = response_create_current_manager['data']['authorization']

    response_create_role_admins = create_role(auth=auth_current_manager,
                                              name="Sharepoint Admins",
                                              owners=[id_current_manager],
                                              admins=[id_current_manager],
                                              members=[id_staff])

    print('Created role:', response_create_role_admins['data']['name'])

    response_create_role_auditors = create_role(auth=auth_current_manager,
                                                name="Infosec Auditors",
                                                owners=[id_current_manager],
                                                admins=[id_current_manager],
                                                members=[id_staff])

    print('Created role:', response_create_role_auditors['data']['name'])

    payload_propose_manager = {"id": id_other_manager}

    response_propose_manager = json.loads(requests.put('http://localhost:8000/api/users/' + id_staff + '/manager/',
                                                       data=json.dumps(payload_propose_manager),
                                                       headers={"Content-Type": "application/json",
                                                                "Authorization": auth_current_manager}).text)

    print('Created proposal id: {} - Switch {}\'s manager from {} to {}'.format(
        response_propose_manager['proposal_id'],
        'staff',
        'currentManager',
        'otherManager'))


def create_user(identifier, manager=''):
    """Creates a user in the system having the given identifier as name, password, username and *optional* manager

       Returns the response payload of the user creation rest call as a json object.
    """
    payload_current_manager = {'name': identifier, 'password': identifier, 'username': identifier,
                               'email': identifier + '@mail.com', 'manager': manager, 'metadata': ''}

    response_create_user = requests.post('http://localhost:8000/api/users/', json=payload_current_manager)
    return json.loads(response_create_user.text)


def create_role(auth, name, owners, admins, members):
    """Creates a role in the system.

       Args:
           auth: The bearer token to be used in the Authorization header
           name: The name of the role
           owners: Owners of the role (add/remove members)
           admins: Administrators of the role (modify the role itself)
           members: Members of the role (inherit the privileges assigned to the role)


       Returns the response payload of the role creation rest call as a json object.
    """

    payload_create_role = {
        "name": name,
        "owners": owners,
        "administrators": admins,
        "members": members,
        "metadata": ""
    }

    response_create_role_envelope = requests.post('http://localhost:8000/api/roles/', json=payload_create_role,
                                                  headers={"Content-Type": "application/json",
                                                           "Authorization": auth})

    if response_create_role_envelope.status_code != 200:
        raise RuntimeError('Failed to create role. Response: ' + response_create_role_envelope.text)

    response_create_role_payload = json.loads(response_create_role_envelope.text)
    return response_create_role_payload


if __name__ == "__main__":
    insert_test_data()
