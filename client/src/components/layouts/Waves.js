/* Copyright 2018 Contributors to Hyperledger Sawtooth

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------- */


import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'
import PropTypes from 'prop-types';
import './Waves.css';


/**
 *
 * @class         Waves
 * @description   Component encapsulating the track pane waves
 *
 *
 */
class Waves extends Component {

  static propTypes = {
    location:              PropTypes.object,
    isAnimating:           PropTypes.bool,
    stopAnimation:         PropTypes.func,
  };


  state = { transition: null };


  componentDidMount () {
    const { location } = this.props;

    const waves = location && !location.pathname.startsWith('/approval');
    const transition = waves ? 'next-waves-animate-up' :
      'next-waves-animate-down';
    this.setState({ transition })
  }


  componentDidUpdate (prevProps) {
    const { isAnimating, location, stopAnimation } = this.props;

    if (this.props.location !== prevProps.location) {
      const waves = location && !location.pathname.startsWith('/approval');

      isAnimating && stopAnimation();
      const transition = isAnimating ?
        (waves ? 'next-waves-animate-up' : 'next-waves-animate-down') :
        (waves ? 'next-waves' : 'next-static');

      this.setState({ transition })
    }
  }


  render () {
    const { transition } = this.state;

    return (
      <div id='next-wave-container'>
        <div id='next-wave'>
          <svg
            xmlns='http://www.w3.org/2000/svg'
            preserveAspectRatio='xMidYMid'
            className={transition}>
            <rect
              x='0'
              y='0'
              width='100%'
              height='100%'
              fill='url(#next-pattern)'/>
            <pattern
              x='0'
              y='0'
              patternUnits='userSpaceOnUse'
              id='next-pattern'
              width='1000'
              height='43'>
              <path
                fill='#fff'
                d={`M -1000 37 C -750 37 -750 2 -500 2 C -250
                    2 -250 37 2 37 C 250 37 250 2 500 2 C 750
                    2 750 37 1000 37`}
                stroke='#f1038e'
                strokeWidth='0'>
                <animateTransform
                  attributeName='transform'
                  type='translate'
                  keyTimes='0;1'
                  repeatCount='indefinite'
                  values='0 0;1000 0'
                  dur='30s'/>
              </path>
            </pattern>
          </svg>
        </div>
        <div id='next-wave-alt'>
          <svg
            className={transition}
            xmlns='http://www.w3.org/2000/svg'
            preserveAspectRatio='xMidYMid'>
            <rect
              x='0'
              y='0'
              width='100%'
              height='100%'
              fill='url(#next-pattern-alt)'/>
            <pattern
              x='0'
              y='0'
              patternUnits='userSpaceOnUse'
              id='next-pattern-alt'
              width='1000'
              height='130'>
              <path
                fill='#ffffff9e'
                d={`M -1000 37 C -750 37 -750 2 -500 2 C -250
                    2 -250 37 2 37 C 250 37 250 2 500 2 C 750
                    2 750 37 1000 37`}
                stroke='#ca0de8'
                strokeWidth='0.4'>
                <animateTransform
                  attributeName='transform'
                  type='translate'
                  keyTimes='0;1'
                  repeatCount='indefinite'
                  values='1000 0;0 0'
                  begin='-7s'
                  dur='30s'/>
              </path>
            </pattern>
          </svg>
        </div>
      </div>
    );
  }

}


export default withRouter(Waves);
