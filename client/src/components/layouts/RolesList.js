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


import React, { Component } from 'react';
import { List, Segment } from 'semantic-ui-react';


import PropTypes from 'prop-types';


import './RolesList.css';


/**
 *
 * @class RolesList
 * Component encapsulating the track pane body
 *
 */
export default class RolesList extends Component {


  render () {
    const { activeRole } = this.props;

    return (
      <div id='next-requester-track-body-container'>

        { activeRole && activeRole.description &&
          <p>{activeRole.description}</p>
        }

        { activeRole && activeRole.roles &&
          <List selection verticalAlign='middle'>
            { activeRole.roles.map((role, index) => (
              <Segment key={index}>
                {role.name}
              </Segment>
            )) }
          </List>
        }

        { activeRole && activeRole.roles &&
          activeRole.roles.length === 0 &&
          <h3>No roles found.</h3>
        }

      </div>
    );
  }

}


RolesList.proptypes = {
  activeRole: PropTypes.arrayOf(PropTypes.shape(
    {
      description: PropTypes.string,
      roles: PropTypes.arrayOf(PropTypes.shape(
        {
          name: PropTypes.string
        }
      ))
    }
  ))
};
