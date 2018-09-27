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
import { Container, Grid, Menu, Search, Segment } from 'semantic-ui-react';
import './Browse.css';


/**
 * 
 * @class Browse
 * Browse component
 * 
 */
class Browse extends Component {

  render () {
    return (
      <div>
        <Container id='next-browse-container'>
          <Menu>
            <Menu.Item>Recommended</Menu.Item>
            <Menu.Item>All Groups</Menu.Item>
            <Menu.Item>All Roles</Menu.Item>
          </Menu>
          <Search loading={false} className='next-browse-search'/>
          <Grid stackable columns={3} id='next-browse-grid'>
            <Grid.Row stretched>
              <Grid.Column>
                <Segment></Segment>
              </Grid.Column>
              <Grid.Column>
                <Segment></Segment>
                <Segment></Segment>
              </Grid.Column>
              <Grid.Column>
                <Segment></Segment>
                <Segment></Segment>
                <Segment></Segment>
              </Grid.Column>
            </Grid.Row>
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
