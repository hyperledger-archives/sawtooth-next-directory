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
 * @property animationBegin  Initiating action
 *
 */
const { Types, Creators } = createActions({
  animationBegin:      null,
  animationEnd:        null,
});


export const AppTypes = Types;
export default Creators;


/**
 *
 * State
 *
 * @property isAnimating
 *
 *
 */
export const INITIAL_STATE = Immutable({
  isAnimating:         null,
});


/**
 *
 * Selectors
 *
 *
 */
export const AppSelectors = {
  isAnimating: (state) => state.app.isAnimating,
};


/**
 *
 * Reducers - General
 *
 *
 */
export const start = (state) => {
  return state.merge({ isAnimating: true });
};
export const end = (state) => {
  return state.merge({ isAnimating: false });
};


/**
 *
 * Hooks
 *
 *
 */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.ANIMATION_BEGIN]: start,
  [Types.ANIMATION_END]: end,
});
