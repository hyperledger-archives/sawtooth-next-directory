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


import RequesterHome from './containers/requester/RequesterHome';
import RequesterNav from './components/nav/RequesterNav';
import Roles from './containers/requester/Roles';
import Packs from './containers/requester/Packs';


import ApproverHome from './containers/approver/ApproverHome';
import ApproverNav from './components/nav/ApproverNav';
import Individuals from './containers/approver/Individuals';
import Expiring from './containers/approver/Expiring';
import Manage from './containers/approver/Manage';
import People from './containers/approver/People';


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
    main:   (rest) => <Packs {...props} {...rest}/>,
    nav:    () => <RequesterNav {...props}/>,
    exact:  true,
  },
  {
    path:   '/roles/:id',
    main:   (rest) => <Roles {...props} {...rest}/>,
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
    path:   '/approval/people',
    main:   (rest) => <People {...props} {...rest}/>,
    nav:    () => <ApproverNav {...props}/>,
    exact:  true,
  },

];


export default routes;
