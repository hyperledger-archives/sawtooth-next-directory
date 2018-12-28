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
import { connect } from 'react-redux';
import { Container, Grid, Header, Placeholder } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import RequesterActions from 'redux/RequesterRedux';


import './Browse.css';
import BrowseCard from './BrowseCard';
import * as theme from 'services/Theme';


/**
 *
 * @class         Browse
 * @description   The browse screen
 *
 */
class Browse extends Component {

  static propTypes = {
    allRoles:           PropTypes.array,
    fetching:           PropTypes.bool,
    getAllRoles:        PropTypes.func,
  };


  themes = ['dark'];


  state = { rolesData: null };


  /**
   * Entry point to perform tasks required to render
   * component. On load, get roles
   */
  componentDidMount () {
    const { getAllRoles } = this.props;
    // TODO: Pagination
    getAllRoles();
    theme.apply(this.themes);
  }


  /**
   * Component teardown
   */
  componentWillUnmount () {
    theme.remove(this.themes);
  }


  /**
   * Called whenever Redux state changes.
   * @param {object} prevProps Props before update
   * @returns {undefined}
   */
  componentDidUpdate (prevProps) {
    const { allRoles } = this.props;
    if (prevProps.allRoles !== allRoles) this.formatData(allRoles);
  }


  /**
   * Format data ?
   * @param {array} value ?
   */
  formatData = (value) => {
    let arr = [[], [], [], []];
    value.forEach((ele, index) => {
      arr[index % 4].push(ele);
    });
    this.setState({ rolesData: arr });
  }

  /**
   * Render layout ?
   * @param {array} layoutData ?
   * @returns {JSX}
   */
  renderLayout (layoutData) {
    const{ rolesData } = this.state;
    let data = layoutData ? layoutData : rolesData;

    return data.map((column, index) => {
      return (<Grid.Column key={index}>
        {this.renderColumns(column)}
      </Grid.Column>);
    });
  }


  /**
   * Render columns
   * @param {array} columnData ?
   * @returns {JSX}
   */
  renderColumns = (columnData) => {
    if(columnData) {
      return columnData.map( (item, index) =>{
        return <BrowseCard key={index} details={item} {...this.props}/> ;
      });
    }
  }


  renderPlaceholder = () => {
    return Array(4).fill(0).map((item, index) => (
      <Grid.Column key={index}>
        <Placeholder inverted>
          <Placeholder.Header image>
            <Placeholder.Line/>
            <Placeholder.Line/>
          </Placeholder.Header>
          <Placeholder.Paragraph>
            <Placeholder.Line length='medium'/>
            <Placeholder.Line length='short'/>
          </Placeholder.Paragraph>
        </Placeholder>
      </Grid.Column>
    ));
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { fetching } = this.props;
    const { rolesData } = this.state;

    return (
      <div id='next-browse-wrapper'>
        <Container fluid id='next-browse-container'>
          <Grid stackable columns={4} id='next-browse-grid'>
            { fetching && this.renderPlaceholder()}
            { rolesData && this.renderLayout()}
          </Grid>
          { rolesData && rolesData.every(item => !item.length) &&
            <Header as='h3' textAlign='center' color='grey'>
              <Header.Content>No roles or packs</Header.Content>
            </Header>
          }
        </Container>
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    allRoles: state.requester.roles,
    fetching: state.requester.fetching,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getAllRoles: () => dispatch(RequesterActions.allRolesRequest()),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Browse);
