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
import { Container, Grid } from 'semantic-ui-react';
import BrowseCard from '../../components/cards/BrowseCard';

import RequesterActions from '../../redux/RequesterRedux';

import './Browse.css';


/**
 * 
 * @class Browse
 * Browse component
 * 
 */
class Browse extends Component {

  state = { rolesData: null, dataStatus:'Fetching Data...' };


  componentDidMount(){
    const { getAllRoles } = this.props;
    getAllRoles();
  }


  componentWillReceiveProps(nextProps) {
    this.props = nextProps;
    const{ allRoles, isFetching } = this.props;
    
    if(allRoles && allRoles.length !== 0){
      this.formatData(allRoles);
    }

    !isFetching && this.setState({ dataStatus: 'No data found.'});
    
  }


  formatData = (value) => {
    let arr=[[],[],[],[]];

    value.map((ele, index) => {
      arr[index % 4].push(ele)
    });

    this.setState({ rolesData: arr });
    
  }

  renderLayout() {
    const { rolesData } = this.state;

    return rolesData.map((column, index) => {
        return (<Grid.Column key={index}>
          {this.renderColumns(column)}
        </Grid.Column>);
    });

  }


  renderColumns = (columnData) => {
    if(columnData) {
      return columnData.map( (item,index) =>{
        return <BrowseCard key={index} details={item}/> ;
      });
    }
  }


  render () {
    const { rolesData, dataStatus } = this.state;

    return (
      <div id='next-browse-wrapper'>
        <Container id='next-browse-container'>
          {rolesData ?
              <Grid relaxed stackable columns={4} id='next-browse-grid'>
                {this.renderLayout()}
            </Grid> :
            <div className='no-data-container'>{dataStatus}</div>
          }
        </Container>
      </div>
    );
  }
  
}


const mapStateToProps = (state) => {
  return {
    isFetching: state.requester.fetching,
    allRoles: state.requester.roles
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    getAllRoles: () => dispatch(RequesterActions.allrolesRequest()),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Browse);
