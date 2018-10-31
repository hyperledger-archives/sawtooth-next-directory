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
import { Icon } from 'semantic-ui-react';

import PropTypes from 'prop-types';

import './toast.css';


/**
 * 
 * @class Toast
 * Component encapsulating the toast to display error message
 * 
 */
export default class Toast extends Component {

  constructor(props) {
    super(props);

    this.hideToast = this.hideToast.bind(this);
    this.timeout = '';
  }

  componentWillReceiveProps(newProps) {
    this.props = newProps;
    const { open, timeout } = this.props;

    if (open) {
      /**
       * auto close functionality
       *  
       */
      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => { this.hideToast() }, timeout || 30000);
    }
  }

  hideToast() {
    const { close } = this.props;

    if (close) {
      close();
    } else {
      document.querySelector('.next-toast-container').classList.add('hide-toast');
    }
  }

  render() {
    const { title, message, open } = this.props;

    return (
      <div className={'next-toast-container' + (open ? '' : ' hide-toast')}>
        <div className='toast-icon-wrapper'>
          <div className='toast-title'>
            {title ? title : 'Error'}
          </div>
          <Icon onClick={() => this.hideToast()} name='close' />
        </div>
        <p>
          {message || ' '}
        </p>
      </div>
    );
  }
}

Toast.prototypes = {
  title: PropTypes.string,
  close: PropTypes.func.isRequired,
  open: PropTypes.bool,
  message: PropTypes.string,
  timeout: PropTypes.number
};
