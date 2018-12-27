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


//
// Actions
//
//
//
//
const { Types, Creators } = createActions({
  animationBegin:                    null,
  animationEnd:                      null,

  socketError:                       ['error'],
  socketMaxAttemptsReached:          null,
  socketOpen:                        null,
  socketOpenSuccess:                 null,
  socketClose:                       null,
  socketCloseSuccess:                null,

  refreshBegin:                      null,
  refreshEnd:                        null,
  refreshOnNextSocketReceive:        ['flag'],
});


export const AppTypes = Types;
export default Creators;

//
// State
//
//
//
//
export const INITIAL_STATE = Immutable({
  error:                              null,
  socketError:                        null,
  socketMaxAttemptsReached:           null,
  isAnimating:                        null,
  isRefreshing:                       null,
  shouldRefreshOnNextSocketReceive:   null,
  isSocketOpen:                       null,
});

//
// Selectors
//
//
//
//
export const AppSelectors = {
  isAnimating:     (state) => state.app.isAnimating,
  isRefreshing:    (state) => state.app.isRefreshing,
  isSocketOpen:    (state) => state.app.isSocketOpen,
  socketError:     (state) => state.app.socketError,
  socketMaxAttemptsReached: (state) =>
    state.app.socketMaxAttemptsReached,
  shouldRefreshOnNextSocketReceive: (state) =>
    state.app.shouldRefreshOnNextSocketReceive,
};

//
// Reducers
//
//
//
//
export const animationBegin = (state) => {
  return state.merge({ isAnimating: true });
};
export const animationEnd = (state) => {
  return state.merge({ isAnimating: false });
};
export const socketOpen = (state) => {
  return state.merge({});
};
export const socketOpenSuccess = (state) => {
  return state.merge({ isSocketOpen: true, socketError: false });
};
export const socketClose = (state) => {
  return state.merge({});
};
export const socketCloseSuccess = (state) => {
  return state.merge({ isSocketOpen: false });
};
export const socketError = (state, { error }) => {
  return state.merge({ socketError: true });
};
export const socketMaxAttemptsReached = (state) => {
  return state.merge({ socketMaxAttemptsReached: true });
};
export const refreshBegin = (state) => {
  return state.merge({ isRefreshing: true });
};
export const refreshEnd = (state) => {
  return state.merge({ isRefreshing: false });
};
export const refreshOnNextSocketReceive = (state, { flag }) => {
  return state.merge({ shouldRefreshOnNextSocketReceive: flag });
};

//
// Hooks
//
//
//
//
export const reducer = createReducer(INITIAL_STATE, {
  [Types.ANIMATION_BEGIN]: animationBegin,
  [Types.ANIMATION_END]: animationEnd,

  [Types.REFRESH_BEGIN]: refreshBegin,
  [Types.REFRESH_END]: refreshEnd,
  [Types.REFRESH_ON_NEXT_SOCKET_RECEIVE]: refreshOnNextSocketReceive,

  [Types.SOCKET_ERROR]: socketError,
  [Types.SOCKET_MAX_ATTEMPTS_REACHED]: socketMaxAttemptsReached,

  [Types.SOCKET_OPEN]: socketOpen,
  [Types.SOCKET_OPEN_SUCCESS]: socketOpenSuccess,

  [Types.SOCKET_CLOSE]: socketClose,
  [Types.SOCKET_CLOSE_SUCCESS]: socketCloseSuccess,
});
