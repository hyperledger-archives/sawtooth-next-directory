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
import { Link, withRouter } from 'react-router-dom';
import { Image, Label, List, Transition } from 'semantic-ui-react';


import PropTypes from 'prop-types';


import './NavList.css';
import * as utils from '../../services/Utils';


/**
 *
 * @class         NavList
 * @description   Component encapsulating a reusable, selectable list suitable
 *                for displaying options in navigation components
 *
 */
class NavList extends Component {

  static propTypes = {
    labels:           PropTypes.array,
    location:         PropTypes.object,
    list:             PropTypes.array,
    listTitle:        PropTypes.string,
    route:            PropTypes.string,
    titleIsLink:      PropTypes.bool,
  };


  /**
   * Determine if nav item is active
   * @param {object} item Nav item
   * @returns {boolean}
   */
  isItemActive = (item) => {
    const { location } = this.props;

    const slug = utils.createSlug(item.slug, item);
    return location.pathname.includes(`/${slug}`);
  };


  /**
   * Create relative URL for nav list item
   * @param {object} item Nav item
   * @returns {string}
   */
  createNavLink = (item) => {
    const { route } = this.props;
    const root = route ||
      (item.roles && item.roles.length > 0 ? '/packs' : '/roles');
    return item.slug ?
      `${root}/${item.slug}` :
      `${root}/${utils.createSlug(item.id, item)}`;
  };


  /**
   * Generate a sub-list of nav links
   *
   * Each list item is ported into a <Link> router element whose
   * attributes are mapped on <List>.
   *
   * Due to some sidebar sub-list items being dynamic and others static,
   * (i.e., *Cloud Onboarding Pack* vs. *Individuals*), to support both in
   * one component, lists are passed in as an array with an optional
   * slug property, which becomes the ID of the route. In cases where
   * no slug is provided, one is generated.
   *
   * @param {array} list List of nav links to display
   * @returns {JSX}
   */
  renderList (list) {
    const { labels } = this.props;

    return (
      list.map((item, index) => (
        item &&
        <List.Item active={this.isItemActive(item)}
          key={index}
          as={Link}
          to={this.createNavLink(item)}>

          <Image floated='left' src=''/>

          <List.Content className='pull-left next-nav-list-content'>
            <List.Header>{item.name}</List.Header>
          </List.Content>

          { labels && labels[index] &&
            <List.Content floated='right' className='next-nav-list-label'>
              <Label circular size='mini' basic>
                {labels[index]}
              </Label>
            </List.Content>
          }
        </List.Item>
      ))
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { list, listTitle, route, titleIsLink } = this.props;

    return (
      <div className='next-nav-list-container'>
        { titleIsLink ?
          <h4><Link to={route}>{listTitle}</Link></h4> :
          <h4>{listTitle}</h4>
        }

        { list && list.length !== 0 ?
          <Transition.Group
            as={List}
            duration={500}
            inverted
            link
            selection>
            { this.renderList(list) }
          </Transition.Group> :
          !titleIsLink &&
          <span className='next-nav-list-empty'>
            No items
          </span>
        }

      </div>
    );
  }

}


export default withRouter(NavList);
