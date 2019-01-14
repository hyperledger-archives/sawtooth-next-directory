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
import { Link } from 'react-router-dom';
import { Breadcrumb, Header, Image, Grid } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './TrackHeader.css';


/**
 *
 * @class         TrackHeader
 * @description   Component encapsulating the track pane header
 *
 *
 */
class TrackHeader extends Component {

  static propTypes = {
    breadcrumb:         PropTypes.array,
    button:             PropTypes.func,
    glyph:              PropTypes.string,
    inverted:           PropTypes.bool,
    subtitle:           PropTypes.string,
    title:              PropTypes.string,
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const {
      breadcrumb,
      button,
      glyph,
      inverted,
      subtitle,
      title } = this.props;

    return (
      <Grid>
        <Grid.Column id='track-header-outer-grid'>
          <div id='next-track-header-container'>
            <div id='next-track-header'>
              { title &&
                <Header as='h1' inverted={inverted}>
                  { glyph &&
                    <Image size='large' src={glyph}/>
                  }
                  <Header.Content>
                    {title}
                    <Header.Subheader id='next-track-header-subheader'>
                      {subtitle}
                    </Header.Subheader>
                  </Header.Content>
                </Header>
              }
              {button && button()}
              { breadcrumb && breadcrumb.length > 1 &&
                <Breadcrumb>
                  <Breadcrumb.Section
                    link
                    as={Link}
                    to={breadcrumb[0].slug}>
                    {breadcrumb[0].name}
                  </Breadcrumb.Section>
                  <Breadcrumb.Divider icon='right chevron'/>
                  <Breadcrumb.Section
                    link
                    as={Link}
                    to={breadcrumb[1].slug}>
                    {breadcrumb[1].name}
                  </Breadcrumb.Section>
                  { title && title !== breadcrumb[1].name &&
                    <div>
                      <Breadcrumb.Divider icon='right arrow'/>
                      <Breadcrumb.Section active>
                        {title}
                      </Breadcrumb.Section>
                    </div>
                  }
                </Breadcrumb>
              }

            </div>
          </div>
        </Grid.Column>
      </Grid>
    );
  }

}


export default TrackHeader;
