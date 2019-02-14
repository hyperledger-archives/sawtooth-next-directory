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
import Search from 'components/search/Search';
import './RoleSelectGridNav.css';


/**
 *
 * @class         RoleSelectGridNav
 * @description   Component encapsulating the template for pack
 *                role selection navigation header
 *
 *
 */
class RoleSelectGridNav extends Component {

  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      fetchingSearchResults,
      searchInput,
      searchLimit,
      searchTypes,
      setSearchInput,
      setSearchStart } = this.props;
    return (
      <div id='next-role-select-grid-nav'>
        <div id='next-role-select-grid-search'>
          <Search
            fetchingSearchResults={fetchingSearchResults}
            searchInput={searchInput}
            searchLimit={searchLimit}
            searchTypes={searchTypes}
            setSearchInput={setSearchInput}
            setSearchStart={setSearchStart}
            type='browse'
            {...this.props}/>
        </div>
      </div>
    );
  }

}


export default RoleSelectGridNav;
