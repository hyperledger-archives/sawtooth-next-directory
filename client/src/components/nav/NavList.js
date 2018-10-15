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
import { Link } from 'react-router-dom'
import { Image, List } from 'semantic-ui-react';


import PropTypes from 'prop-types';


import './NavList.css';


/**
 * 
 * @class NavList
 * Component encapsulating a reusable, selectable list suitable
 * for displaying options in navigation components
 * 
 */
export default class NavList extends Component {

  /**
   * 
   * Generate a sub-list of nav links
   * 
   * Each list item is ported into a <Link> router element whose
   * attributes are mapped on <List>.
   * 
   * Due to some sidebar sub-list items being dynamic and others static,
   * (i.e., *Cloud Onboarding Pack* vs. *Individuals*), to support both in
   * one component, lists are passed in as an array with an optional
   * slug property, which becomes the ID of the route.
   * 
   * In cases where no slug is provided, one is generated.
   * 
   */
  renderList (list) {
    const { dynamic, route } = this.props;

    return (
      list.map((item, index) => (
        <List.Item
          key={index}
          as={Link}
          to={dynamic ?
            `${route}/${item.slug}` :
            `${route}/${this.createSlug(item)}`}>

          <Image src=''/>
          
          <List.Content>
            { dynamic ?
              <List.Header>{item.name}</List.Header> :
              <List.Header>{item}</List.Header>
            }
          </List.Content>
        </List.Item>
      ))
    )
  }


  // TODO: Move to utils
  createSlug (name) {
    return name
      .toLowerCase()
      .replace(/ /g, '-')
      .replace(/[^\w-]+/g, '');
  }


  render () {
    const { list, listTitle } = this.props;

    return (
      <div className='next-nav-list-container'>
        <h3>{listTitle}</h3>
        
        { list &&
          <List inverted link selection>
            { this.renderList(list) }
          </List>
        }

        { !list &&
          <span className='next-nav-list-label'>
            No items
          </span>
        }
      </div>
    );
  }
  
}


NavList.prototypes = {
  route: PropTypes.string,
  listTitle: PropTypes.string,
  list: PropTypes.arrayOf(PropTypes.number),
  dynamic: PropTypes.bool
};
