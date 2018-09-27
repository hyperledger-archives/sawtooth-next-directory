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


import { createReducer, createActions } from 'reduxsauce';
import Immutable from 'seamless-immutable';


/**
 * 
 * Actions
 * 
 * @property getPackRequest
 * @property getPackSuccess
 * 
 */
const { Types, Creators } = createActions({
  getPackRequest:       ['id'],
  getPackSuccess:       ['activePack']
});


export const HomeTypes = Types;
export default Creators;


/**
 * 
 * State
 * 
 * @property isAuthenticated
 * @property fetching
 * @property error
 * 
 */
export const INITIAL_STATE = Immutable({
  activePack:       null,
  fetching:         null,
  error:            null
});


/**
 * 
 * Selectors
 * 
 * 
 */
export const HomeSelectors = {
  activePack: (state) => {
    return state.home.activePack;
  }
};


export const request = (state) => state.merge({ fetching: true });
export const success = (state, { activePack }) => {
  return state.merge({ fetching: false, activePack });
}


/**
 * 
 * Reducers
 * 
 * 
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.GET_PACK_REQUEST]: request,
  [Types.GET_PACK_SUCCESS]: success
});
