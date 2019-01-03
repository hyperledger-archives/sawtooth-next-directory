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
import { Header, Segment } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import './BrowseCard.css';
import StackedAvatar from './StackedAvatar';
import * as utils from 'services/Utils';


/**
 *
 * @class         BrowseCard
 * @description   BrowseCard component
 *
 *
 */
class BrowseCard extends Component {

  static propTypes = {
    resource: PropTypes.object,
  };


  state = { isPinned: false };


  togglePinned = () => {
    this.setState({
      isPinned: !this.state.isPinned,
    });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { resource } = this.props;

    return (
      <Segment
        as={Link}
        to={`/${resource.roles ? 'packs' : 'roles'}/${resource.id}`}
        className={`gradient ${resource.roles ? 'browse-tile-expanded' : ''}`}>
        <div className='browse-tile-title-container'>
          <Header inverted as='h3'>
            {resource.name}
            { resource.roles &&
              <Header.Subheader>
                {resource.roles && utils.countLabel(
                  resource.roles.length, 'role')
                }
              </Header.Subheader>
            }
          </Header>
          {/* <Icon
            className='browse-tile-pinned-icon'
            disabled={!isPinned}
            onClick={this.togglePinned}
            inverted name='pin' size='small'/> */}
        </div>
        { resource.roles &&
        <div className='browse-tile-description'>
          {resource.description || 'No description available.'}
        </div>
        }
        { !resource.roles &&
          <div className='browse-tile-members'>
            <StackedAvatar
              list={[...resource.owners, ...resource.members]}
              {...this.props}/>
          </div>
        }
      </Segment>
    );
  }

}


export default BrowseCard;
