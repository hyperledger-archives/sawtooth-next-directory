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


import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { Slide, ToastContainer } from 'react-toastify';


import routes from './routes';
import App from './containers/app/App';
import registerServiceWorker from './registerServiceWorker';
import * as customStore from './customStore';


import './index.css';
import './semantic/semantic.css';
import 'react-toastify/dist/ReactToastify.css';


const store = customStore.create();


ReactDOM.render(
  <div id='next-root'>
    <Provider store={store}>
      <App routes={routes}/>
    </Provider>
    <ToastContainer
      autoClose={2500}
      toastClassName='toast'
      closeButton={false}
      hideProgressBar
      position='bottom-left'
      transition={Slide}/>
  </div>,
  document.getElementById('root')
);

registerServiceWorker();
