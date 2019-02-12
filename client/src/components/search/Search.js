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
import { Input, Search as SearchInput } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './Search.css';
import * as utils from 'services/Utils';


/**
 *
 * @class         Search
 * @description   Component encapsulating app search functionality
 *
 *
 */
class Search extends Component {

  static propTypes = {
    fetchingSearchResults:  PropTypes.bool,
    resetSearchStart:       PropTypes.func,
    search:                 PropTypes.func,
    searchInput:            PropTypes.string,
    searchLimit:            PropTypes.number,
    setSearchInput:         PropTypes.func,
    types:                  PropTypes.array,
  };


  /**
   * Handle form change event
   * @param {object} event Event passed by Semantic UI
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  handleChange = (event, { name, value }) => {
    const {
      resetSearchStart,
      searchLimit,
      search,
      setSearchInput,
      types } = this.props;

    setSearchInput(value);
    resetSearchStart();

    if (utils.isWhitespace(value)) return;

    const query = {
      query: {
        search_input: value,
        search_object_types: types,
        page_size: searchLimit,
        page: 1,
      },
    };

    search('browse', query);
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { fetchingSearchResults, searchInput } = this.props;
    return (
      <div>
        <SearchInput
          fluid
          input={() => <Input
            fluid
            loading={fetchingSearchResults}
            size='large'
            icon='search'
            placeholder='Search...'
            name='searchInput'
            value={searchInput}
            onChange={this.handleChange}/>}
          className='next-search-input'
          category
          loading={false}/>
      </div>
    );
  }

}


export default Search;
