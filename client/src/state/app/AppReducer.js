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


import { createReducer } from 'reduxsauce';
import { INITIAL_STATE, AppTypes as Types } from './AppActions';


export const animationBegin = (state) =>
  state.merge({ isAnimating: true });


export const animationEnd = (state) =>
  state.merge({ isAnimating: false });


export const socketOpen = (state) =>
  state.merge({});


export const socketOpenSuccess = (state) =>
  state.merge({ isSocketOpen: true, socketError: false });


export const socketClose = (state) =>
  state.merge({});


export const socketCloseSuccess = (state) =>
  state.merge({ isSocketOpen: false });


export const socketError = (state, { error }) =>
  state.merge({ socketError: true });


export const socketMaxAttemptsReached = (state) =>
  state.merge({ socketMaxAttemptsReached: true });


export const refreshBegin = (state) =>
  state.merge({ isRefreshing: true });


export const refreshEnd = (state) =>
  state.merge({ isRefreshing: false });


export const refreshOnNextSocketReceive = (state, { flag }) =>
  state.merge({ shouldRefreshOnNextSocketReceive: flag });


export const AppReducer = createReducer(INITIAL_STATE, {
  [Types.ANIMATION_BEGIN]:                animationBegin,
  [Types.ANIMATION_END]:                  animationEnd,

  [Types.REFRESH_BEGIN]:                  refreshBegin,
  [Types.REFRESH_END]:                    refreshEnd,

  [Types.SOCKET_ERROR]:                   socketError,
  [Types.SOCKET_OPEN]:                    socketOpen,
  [Types.SOCKET_OPEN_SUCCESS]:            socketOpenSuccess,
  [Types.SOCKET_CLOSE]:                   socketClose,
  [Types.SOCKET_CLOSE_SUCCESS]:           socketCloseSuccess,
  [Types.SOCKET_MAX_ATTEMPTS_REACHED]:    socketMaxAttemptsReached,
  [Types.REFRESH_ON_NEXT_SOCKET_RECEIVE]: refreshOnNextSocketReceive,
});
