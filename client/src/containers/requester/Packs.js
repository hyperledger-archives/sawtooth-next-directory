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
import { Grid } from 'semantic-ui-react';
import PropTypes from 'prop-types';


import Chat from '../../components/chat/Chat';
import TrackHeader from '../../components/layouts/TrackHeader';
import RolesList from '../../components/layouts/RolesList';


import './Packs.css';


/**
 *
 * @class Packs
 * *Your Packs* component
 *
 */
class Packs extends Component {
  render() {
    const { activePack } = this.props;
    const title = activePack && activePack.name;

    return (
      <Grid id="next-requester-grid" celled="internally">

        <Grid.Column
          id="next-requester-grid-track-column"
          width={10}
        >
          <TrackHeader title={title} {...this.props} />
          <RolesList {...this.props} />
        </Grid.Column>
        <Grid.Column
          id="next-requester-grid-converse-column"
          width={6}
        >
          <Chat {...this.props} />
        </Grid.Column>

      </Grid>
    );
  }
}


Packs.propTypes = {
  activePack: PropTypes.arrayOf(PropTypes.shape(
    {
      name: PropTypes.string,
    },
  )),
};

Packs.defaultProps = {
  activePack: '',
};

const mapStateToProps = state => ({});

const mapDispatchToProps = dispatch => ({});

export default connect(mapStateToProps, mapDispatchToProps)(Packs);
