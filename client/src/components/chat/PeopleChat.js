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
import { Link } from 'react-router-dom';
import {
  Accordion,
  Button,
  Card,
  Container,
  Grid,
  Header,
  Icon,
  Image } from 'semantic-ui-react';


import './PeopleChat.css';
import * as utils from 'services/Utils';
import glyph from 'images/header-glyph-role.png';
import Avatar from 'components/layouts/Avatar';


/**
 *
 * @class         PeopleChat
 * @description   Component encapsulating the people chat view
 *
 */
export default class PeopleChat extends Component {

  state = { activeIndex: 0, currentRolesMaxCount: 5 };


  /**
   * Called whenever Redux state changes. Load roles not loaded in client.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { activeUser } = this.props;
    if (prevProps.activeUser !== activeUser)
      this.init();
  }


  /**
   * Determine which roles are not currently loaded
   * in the client and dispatch actions to retrieve them.
   */
  init () {
    const {
      activeUser,
      getRoles,
      userFromId,
      roles } = this.props;
    const user = userFromId(activeUser);
    if (!user) return;

    let roleIds = user.memberOf;
    if (roles && roles.length) {
      roleIds = roleIds.filter(
        roleId => !roles.find(role => role.id === roleId)
      );
    }
    getRoles(roleIds);
  }


  /**
   * Get user name from user ID
   * @param {string} userId User ID
   * @returns {string}
   */
  userName = (userId) => {
    const { id, userFromId } = this.props;
    const user = userFromId(userId);
    if (user)
      return userId === id ? `${user.name} (You)` : user.name;
    return null;
  };


  /**
   * Switch between accordion views
   * @param {number} activeIndex Current accordion index
   */
  setFlow = (activeIndex) => {
    this.setState(prevState => ({
      activeIndex: prevState.activeIndex === activeIndex ?
        -1 :
        activeIndex,
    }));
  };


  /**
   * Render user role card
   * @param {string} roleId Role ID
   * @returns {JSX}
   */
  renderUserRole (roleId) {
    const { roleFromId } = this.props;
    const role = roleFromId(roleId);
    return (
      role &&
      <Grid.Column key={roleId}>
        <Card
          fluid
          as={Link}
          to={`/roles/${roleId}`}
          className='minimal small'>
          <Header as='h4'>
            <div>
              <Image size='mini' src={glyph}/>
            </div>
            <div>
              {role.name}
            </div>
          </Header>
          <Card.Content extra>
            { utils.countLabel([
              ...role.members,
              ...role.owners,
            ]
              .length, 'member')
            }
          </Card.Content>
        </Card>
      </Grid.Column>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      activeUser,
      handleOnBehalfOf,
      organization,
      userFromId } = this.props;

    const { activeIndex, currentRolesMaxCount } = this.state;
    const user = userFromId(activeUser);
    if (!user) return null;

    return (
      <div>
        <div id='next-chat-users-selection-container'>
          { activeUser &&
            <div id='next-chat-organization-heading'>
              <Avatar userId={activeUser} size='large' {...this.props}/>
              <Header as='h2' inverted>
                {this.userName(activeUser)}
              </Header>
              { organization &&
                organization.direct_reports.includes(activeUser) &&
                <div>
                  <Button
                    as={Link}
                    to={`people/${activeUser}/pending`}
                    onClick={handleOnBehalfOf}>
                    Pending Approvals
                  </Button>
                </div>
              }
              <Container
                id='next-chat-organization-user-info'
                textAlign='left'>
                <Accordion inverted>
                  { user.memberOf.length > 0 &&
                    <div>
                      <Accordion.Title
                        active={activeIndex === 0}
                        index={0}
                        onClick={() => this.setFlow(0)}>
                        <Icon name='dropdown'/>
                        Current Roles
                      </Accordion.Title>
                      <Accordion.Content active={activeIndex === 0}>
                        <Grid columns={1} stackable>
                          { user.memberOf.slice(0, currentRolesMaxCount).map(
                            roleId => this.renderUserRole(roleId)
                          )}
                        </Grid>
                        { user.memberOf.length > currentRolesMaxCount &&
                          <Container
                            id='next-chat-organization-view-all-button'
                            textAlign='center'>
                            <Button
                              basic
                              animated
                              inverted
                              as={Link}
                              to={'/'}
                              size='mini'>
                              <Button.Content visible>
                                VIEW ALL
                              </Button.Content>
                              <Button.Content hidden>
                                <Icon name='arrow right'/>
                              </Button.Content>
                            </Button>
                          </Container>
                        }
                      </Accordion.Content>
                    </div>
                  }
                </Accordion>
              </Container>
            </div>
          }
        </div>
      </div>
    );
  }

}
