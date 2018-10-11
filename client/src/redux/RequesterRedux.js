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
 * @property request  Initiating action
 * @property success  Action called on execution success
 * @property failure  Action called on execution failure
 * 
 */
const { Types, Creators } = createActions({
  baseRequest:       null,
  baseSuccess:       ['base'],
  baseFailure:       ['error'],

  packRequest:       ['id'],
  packSuccess:       ['activePack'],
  packFailure:       ['error']
});


export const RequesterTypes = Types;
export default Creators;


/**
 * 
 * State
 * 
 * @property recommended
 * @property requests
 * @property fetching
 * @property activePack
 * @property error
 * 
 * @todo Consider normalizing recommended, requests, and packs
 * into one roles entity, queried by selector
 * 
 */
export const INITIAL_STATE = Immutable({
  recommended:      null,
  requests:         null,
  fetching:         null,
  activePack:       null,
  error:            null
});


/**
 * 
 * Selectors
 * 
 * 
 */
export const RequesterSelectors = {
  activePack:   (state) => state.requester.activePack,
  recommended:  (state) => state.requester.recommended,
  requests:     (state) => state.requester.requests,

  idFromSlug: (collection, slug) => {
    if (!collection) return null;

    const pack = collection.find((item) => item.slug === slug);
    return pack && pack.id;
  }
};


/**
 * 
 * Reducers - General
 * 
 * 
 */
export const request = (state) => state.merge({ fetching: true });
export const failure = (state, { error }) => {
  return state.merge({ fetching: false, error });
}


/**
 * 
 * Reducers - Success
 * 
 * 
 */
export const packSuccess = (state, { activePack }) => {
  return state.merge({ fetching: false, activePack });
}

export const baseSuccess = (state, { base }) => {
  return state.merge({
    fetching: false,
    recommended: base.recommended,
    requests: base.requests
  });
}


export const reducer = createReducer(INITIAL_STATE, {
  [Types.BASE_REQUEST]: request,
  [Types.BASE_SUCCESS]: baseSuccess,
  [Types.BASE_FAILURE]: failure,

  [Types.PACK_REQUEST]: request,
  [Types.PACK_SUCCESS]: packSuccess,
  [Types.PACK_FAILURE]: failure
});
