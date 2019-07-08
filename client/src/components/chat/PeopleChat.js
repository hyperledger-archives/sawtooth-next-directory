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
  Image,
  Label } from 'semantic-ui-react';


import './PeopleChat.css';
import * as utils from 'services/Utils';
import glyph from 'images/glyph-role.png';
import Avatar from 'components/layouts/Avatar';
import Organization from 'containers/approver/people/Organization';


/**
 *
 * @class         PeopleChat
 * @description   Component encapsulating the people chat view
 *
 */
class PeopleChat extends Component {

  state = { accordionIndex: 0, currentRolesMaxCount: 5 };


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
    const { currentRolesMaxCount } = this.state;
    const user = userFromId(activeUser);
    if (!user) return;

    let roleIds = user.memberOf;
    if (roles && roles.length) {
      roleIds = roleIds && roleIds.filter(
        roleId => !roles.find(role => role.id === roleId)
      );
    }
    roleIds && getRoles(roleIds.slice(0, currentRolesMaxCount));
  }


  /**
   * Get user name from user ID
   * @param {string} userId User ID
   * @returns {string}
   */
  userName = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    if (user) return utils.toTitleCase(user.name);
    return null;
  };


  /**
   * Get user email from user ID
   * @param {string} userId User ID
   * @returns {string}
   */
  userEmail = (userId) => {
    const { userFromId } = this.props;
    const user = userFromId(userId);
    if (user) return user.email;
    return null;
  };


  /**
   * Switch between accordion views
   * @param {number} accordionIndex Current accordion index
   */
  setFlow = (accordionIndex) => {
    this.setState(prevState => ({
      accordionIndex: prevState.accordionIndex === accordionIndex ?
        -1 :
        accordionIndex,
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
            {utils.countLabel(role.members.length, 'member')}
          </Card.Content>
        </Card>
      </Grid.Column>
    );
  }


  /**
   * Construct organization accordion panel
   * @returns {object}
   */
  organizationPanel = () => {
    const {
      activeIndex,
      activeUser,
      fetchingOrganization,
      setFlow } = this.props;
    if (activeIndex === 1) return null;

    return {
      key: 'organization-panel',
      title: {
        content: (
          <span>
            <strong>
              Organization
            </strong>
          </span>
        ),
      },
      content: {
        content: (
          <div className='next-people-organization-panel'>
            <Organization
              compact
              activeUser={activeUser}
              handleUserSelect={() => {}}
              {...this.props}/>
            { !fetchingOrganization &&
              <Container
                className='next-chat-organization-view-all-button'
                textAlign='center'>
                <Button
                  basic
                  animated
                  onClick={() => setFlow(1)}
                  size='mini'>
                  <Button.Content visible>
                  VIEW FULL CHART
                  </Button.Content>
                  <Button.Content hidden>
                    <Icon name='arrow right'/>
                  </Button.Content>
                </Button>
              </Container>
            }
          </div>
        ),
      },
    };
  }


  /**
   * Construct roles accordion panel
   * @param {object} user User
   * @returns {object}
   */
  rolesPanel = (user) => {
    const { setFlow } = this.props;
    const { currentRolesMaxCount } = this.state;
    return {
      key: 'roles-panel',
      title: {
        content: (
          <span>
            <strong>
              Current Roles
            </strong>
          </span>
        ),
      },
      content: {
        content: (
          <div>
            <Grid columns={1} stackable>
              { user.memberOf &&
                user.memberOf.length > 0 &&
                user.memberOf.slice(0, currentRolesMaxCount).map(
                  roleId => this.renderUserRole(roleId)
                )}
              { user.memberOf && user.memberOf.length === 0 &&
              <div className='next-people-organization-no-items'>
                <span>
                  No roles
                </span>
              </div>
              }
            </Grid>
            { user.memberOf &&
              user.memberOf.length > currentRolesMaxCount &&
              <Container
                className='next-chat-organization-view-all-button'
                textAlign='center'>
                <Button
                  basic
                  animated
                  onClick={() => setFlow(2)}
                  size='mini'>
                  <Button.Content visible>
                  VIEW ALL ROLES
                  </Button.Content>
                  <Button.Content hidden>
                    <Icon name='arrow right'/>
                  </Button.Content>
                </Button>
              </Container>
            }
          </div>
        ),
      },
    };
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      activeUser,
      directReports,
      handleOnBehalfOf,
      isAdministrator,
      id,
      organization,
      userFromId } = this.props;

    const user = userFromId(activeUser);
    if (!user) return null;

    return (
      <div>
        <div id='next-chat-users-selection-container'>
          { activeUser &&
            <div id='next-chat-organization-heading'>
              <Container>
                <Avatar userId={activeUser} size='large' {...this.props}/>
                <Header as='h2'>
                  {this.userName(activeUser)}
                  <Header.Subheader>
                    {this.userEmail(activeUser)}
                  </Header.Subheader>
                </Header>
                { organization && directReports && id &&
                  (organization.managers.includes(id) ||
                  directReports.includes(activeUser)) &&
                  <div>
                    <Label color='green' horizontal>
                      Direct Report
                    </Label>
                    <div id='next-people-chat-pending-approvals-button'>
                      <Button
                        as={Link}
                        size='large'
                        to={`people/${activeUser}/pending`}
                        onClick={handleOnBehalfOf}>
                        Pending Approvals
                      </Button>
                    </div>
                  </div>
                }
                { process.env.REACT_APP_ENABLE_NEXT_BASE_USE === '1' &&
                  isAdministrator &&
                  <div>
                    <div id='next-people-chat-pending-approvals-button'>
                      <Button
                        as={Link}
                        size='large'
                        to={`people/${activeUser}/edit`}>
                        Edit
                      </Button>
                    </div>
                  </div>
                }
              </Container>
              <Container
                id='next-chat-organization-user-info'
                textAlign='left'>
                <Accordion
                  defaultActiveIndex={[0, 1]}
                  panels={[
                    this.organizationPanel(),
                    this.rolesPanel(user),
                  ]}
                  exclusive={false}/>
              </Container>
            </div>
          }
        </div>
      </div>
    );
  }

}


export default PeopleChat;
