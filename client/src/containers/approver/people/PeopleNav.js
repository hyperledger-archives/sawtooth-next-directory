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
import { Button, Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import Search from 'components/search/Search';
import './PeopleNav.css';


/**
 *
 * @class         PeopleNav
 * @description   Component encapsulating the template for the People
 *                screen navigation header
 *
 *
 */
class PeopleNav extends Component {

  static propTypes = {
    activeIndex:        PropTypes.number,
    setFlow:            PropTypes.func,
  };


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      activeIndex,
      fetchingSearchResults,
      searchInput,
      searchLimit,
      searchTypes,
      setFlow,
      setSearchInput,
      setSearchStart } = this.props;

    return (
      <div
        id='next-people-nav'
        className={activeIndex > 0 ? 'next-people-nav-less-padding' : ''}>
        { activeIndex > 0 &&
          <Button
            icon
            className='next-people-nav-back-button'
            labelPosition='left'
            onClick={() => setFlow(0)}>
            People
            <Icon name='left arrow'/>
          </Button>
        }
        { activeIndex === 0 &&
        <Search
          fetchingSearchResults={fetchingSearchResults}
          searchInput={searchInput}
          searchLimit={searchLimit}
          searchTypes={searchTypes}
          setSearchInput={setSearchInput}
          setSearchStart={setSearchStart}
          type='people'
          {...this.props}/>
        }
      </div>
    );
  }

}


export default PeopleNav;
