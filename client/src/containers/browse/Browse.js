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

import API from '../../services/Api';
import FixtureAPI from '../../services/FixtureApi';

import './Browse.css';


/**
 * 
 * @class Browse
 * Browse component
 * 
 */
class Browse extends Component {

  state = { rolesData: [] };


  componentDidMount(){
    /**
     * TODO: Move to redux 
     * 
     */
    // let api = API.create();
    let data = FixtureAPI.getRoles();
    this.formatData(data.data);
  }


  formatData = (value) => {
    let arr=[[],[],[],[]];

    value.map((ele, index) => {
      arr[index % 4].push(ele)
    });

    this.setState({ rolesData: arr });
  }


  renderColumns = (columnData) => {
    if(columnData) {
      return columnData.map( (item,index) =>{
        return <BrowseCard key={index} details={item}/> ;
      });
    }
  }


  render () {
    const { rolesData } = this.state;

    return (
      <div id='next-browse-wrapper'>
        <Container id='next-browse-container'>
          <Grid relaxed stackable columns={4} id='next-browse-grid'>
              <Grid.Column>
                {this.renderColumns(rolesData[0])}
              </Grid.Column>
              <Grid.Column>
                {this.renderColumns(rolesData[1])}
              </Grid.Column>
              <Grid.Column>
                {this.renderColumns(rolesData[2])}
              </Grid.Column>
              <Grid.Column>
                {this.renderColumns(rolesData[3])}
              </Grid.Column>
          </Grid>
        </Container>
      </div>
    );
  }
  
}


const mapStateToProps = (state) => {
  return {};
}

const mapDispatchToProps = (dispatch) => {
  return {};
}

export default connect(mapStateToProps, mapDispatchToProps)(Browse);
