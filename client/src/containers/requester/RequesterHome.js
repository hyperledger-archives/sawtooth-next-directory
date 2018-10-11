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
import { Container, Image, List } from 'semantic-ui-react';


import PropTypes from 'prop-types';


import './RequesterHome.css';


/**
 * 
 * @class Home
 * Component encapsulating the requester home, which serves as the
 * default landing page after login.
 * 
 */
export default class RequesterHome extends Component {

  render() {
    const { activePack } = this.props;

    return (
      <Container className='next-requester-container'>
        <h1>Requester Home</h1>
        <p>Lorem ipsum dolor sit amet consectitur adipiscing elit.</p>

        { activePack && 
          <h1>Pack ID: {activePack.id}</h1>
        }

        { activePack && activePack.description && 
          <p>{activePack.description}</p>
        }

        { activePack && activePack.roles &&
          <List selection verticalAlign='middle'>
            { activePack.roles.map((role, index) => (
              <List.Item key={index}>
                <Image src=''/>
                <List.Content>
                  <List.Header>{role.id}</List.Header>
                  <span>{role.name}</span>
                  <span>{role.email}</span>
                </List.Content>
              </List.Item>
            )) }
          </List>
        }
      </Container>
    );
  }
  
}


RequesterHome.proptypes = {
  activePack: PropTypes.arrayOf(PropTypes.shape(
    {
      id: PropTypes.string,
      description: PropTypes.string,
      roles: PropTypes.arrayOf(PropTypes.shape(
        {
          id: PropTypes.string,
          name: PropTypes.string,
          email: PropTypes.email
        }  
      ))
    }
  ))
};
