/* Copyright 2018 Contributors to Hyperledger Sawtooth

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
/*


Routes
Routes are destructured from the declarative syntax due to for
increased flexibility. State is sent top-down via propsto the main
and nav components. */


import React from 'react';


import ApproverNav from './components/nav/ApproverNav';
import RequesterHome from './containers/requester/RequesterHome';
import RequesterNav from './components/nav/RequesterNav';
import Role from './containers/requester/Role';
import Pack from './containers/requester/Pack';


import Approved from './containers/approver/Approved';
import ApproverHome from './containers/approver/ApproverHome';
import CreatePack from './containers/approver/manage/CreatePack';
import CreateRole from './containers/approver/manage/CreateRole';
import Expiring from './containers/approver/Expiring';
import Individuals from './containers/approver/Individuals';
import Manage from './containers/approver/manage/Manage';
import ManagePacks from './containers/approver/manage/ManagePacks';
import ManageRoles from './containers/approver/manage/ManageRoles';
import People from './containers/approver/people/People';
import Delegated from './containers/approver/Delegated';
import Expired from './containers/approver/Expired';
import PeopleApproval from './containers/approver/people/PeopleApproval';


const routes = (props) => [
  //
  // Requester
  //
  //
  //
  //
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

  //
  // Approver
  //
  //
  //
  //

  {
    path:   '/approval',
    main:   (rest) => <ApproverHome {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/approval/pending/individual',
    main:   (rest) => <Individuals {...props} {...rest}/>,
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
    path:   '/approval/people',
    main:   (rest) => <People {...props} {...rest}/>,
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
