/* Copyright 2019 Contributors to Hyperledger Sawtooth

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------- */


import React from 'react';


import ApproverHome from 'containers/approver/ApproverHome';
import ApproverNav from 'components/nav/ApproverNav';
import RequesterHome from 'containers/requester/RequesterHome';
import RequesterNav from 'components/nav/RequesterNav';


import Role from 'containers/requester/role/Role';
import Pack from 'containers/requester/pack/Pack';


import Approved from 'containers/approver/proposals/Approved';
import Delegated from 'containers/approver/proposals/Delegated';
import Expired from 'containers/approver/proposals/Expired';
import Expiring from 'containers/approver/proposals/Expiring';
import Individual from 'containers/approver/proposals/Individual';
import PeopleApproval from 'containers/approver/proposals/PeopleApproval';
import Rejected from 'containers/approver/proposals/Rejected';


import Manage from 'containers/approver/manage/Manage';
import People from 'containers/approver/people/People';
import EditUser from 'containers/approver/people/EditUser';


import CreateRole from 'containers/approver/manage/roles/CreateRole';
import ManageRoles from 'containers/approver/manage/roles/ManageRoles';
import CreatePack from 'containers/approver/manage/packs/CreatePack';
import ManagePacks from 'containers/approver/manage/packs/ManagePacks';
import CreateDelegation
  from 'containers/approver/manage/delegations/CreateDelegation';
import ManageDelegations
  from 'containers/approver/manage/delegations/ManageDelegations';


const routes = (props) => [
  {
    path:   '/',
    main:   (rest) => <RequesterHome {...props} {...rest}/>,
    nav:    () => <RequesterNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/packs/:id',
    main:   (rest) => <Pack {...props} {...rest}/>,
    nav:    () => <RequesterNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/roles/:id',
    main:   (rest) => <Role {...props} {...rest}/>,
    nav:    () => <RequesterNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval',
    main:   (rest) => <ApproverHome {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/pending/individual',
    main:   (rest) => <Individual {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/pending/about-to-expire',
    main:   (rest) => <Expiring {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/manage',
    main:   (rest) => <Manage {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/manage/roles',
    main:   (rest) => <ManageRoles {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/manage/packs',
    main:   (rest) => <ManagePacks {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/manage/delegations',
    main:   (rest) => <ManageDelegations {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/manage/roles/create',
    main:   (rest) => <CreateRole {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/manage/packs/create',
    main:   (rest) => <CreatePack {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/manage/delegations/create',
    main:   (rest) => <CreateDelegation {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/people',
    main:   (rest) => <People {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/people/:id/edit',
    main:   (rest) => <EditUser {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/people/:id/pending',
    main:   (rest) => <PeopleApproval {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/approved',
    main:   (rest) => <Approved {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/rejected',
    main:   (rest) => <Rejected {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/delegated',
    main:   (rest) => <Delegated {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/expired',
    main:   (rest) => <Expired {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
];


export default routes;
