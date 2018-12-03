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
/*


Browse
Browse component */


import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Container, Grid } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import BrowseCard from '../../components/cards/BrowseCard';
import RequesterActions from '../../redux/RequesterRedux';


import './Browse.css';


class Browse extends Component {

  static propTypes = {
    allRoles:           PropTypes.array,
    getAllRoles:        PropTypes.func,
  };


  componentDidMount(){
    const { getAllRoles } = this.props;
    getAllRoles();
  }


  componentDidUpdate (prevProps) {
    const { allRoles } = this.props;

    if(allRoles && allRoles.length !== 0) this.formatData(allRoles);

  }


  formatData = (value) => {
    let arr=[[], [], [], []];

    value.forEach((ele, index) => {
      arr[index % 4].push(ele)
    });

    this.rolesData = arr;

  }

  renderLayout() {
    return this.rolesData.map((column, index) => {
      return (<Grid.Column key={index}>
        {this.renderColumns(column)}
      </Grid.Column>);
    });

  }


  renderColumns = (columnData) => {
    if(columnData) {
      return columnData.map( (item, index) =>{
        return <BrowseCard key={index} details={item}/> ;
      });
    }

  }


  render () {
    return (
      <div id='next-browse-wrapper'>
        <Container id='next-browse-container'>
          {this.rolesData &&
              <Grid relaxed stackable columns={4} id='next-browse-grid'>
                {this.renderLayout()}
              </Grid>
          }
        </Container>
      </div>
    );
  }

}


const mapStateToProps = (state) => {
  return {
    allRoles: state.requester.roles,
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    getAllRoles: () => dispatch(RequesterActions.allrolesRequest()),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Browse);
