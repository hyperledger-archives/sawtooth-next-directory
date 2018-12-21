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


import apisauce from 'apisauce';
import { toast } from 'react-toastify';
import * as storage from '../services/Storage';
import * as AuthActions from '../redux/AuthRedux';


/**
 *
 * Service that includes functions for calling endpoints
 * and configuration for API call behavior
 *
 * @param {string} baseURL Base API URL
 *
 * @example
 *    const api = API.create(...)
 *    api.login(...)
 *
 * If you would like to use this service in sagas, pass it as an
 * argument and then:
 *
 * @example
 *    yield call(api.login, ...)
 *
 * @returns {object}
 *
 */

const create = (baseURL =
(process.env.REACT_APP_HTTP_PROTOCOL || 'http://') +
  (process.env.REACT_APP_SERVER_HOST || 'localhost') + ':' +
  (process.env.REACT_APP_SERVER_PORT || '8000') + '/api/') => {
  //
  // Configuration
  //
  //
  //
  //
  const api = apisauce.create({
    baseURL,
    withCredentials: true,
  });

  //
  // Transforms
  //
  //
  //
  //
  api.addResponseTransform(res => {
    switch (res.problem) {
      case 'TIMEOUT_ERROR':
        toast('Server is not responding. Please try again later.');
        return;
      case 'NETWORK_ERROR':
        toast('Server currently unavailable. Please try again later.');
        return;
      case 'CONNECTION_ERROR':
        toast('Cannot connect to server. Please try again later.');
        return;
      default:
        break;
    }
    switch (res.status) {
      case 200:
        break;
      case 401:
        AuthActions.logout();
        break;
      case 404:
        break;
      default:
        toast(res.data.message);
        break;
    }
  });

  //
  // Definitions
  //
  //
  //
  //
  const me = () => {
    const id = storage.get('user_id');
    return api.get(`users/${id}`);
  };
  const getConfirmedProposals = () => {
    const id = storage.get('user_id');
    return api.get(`users/${id}/proposals/confirmed`);
  };
  const getOpenProposals = (id) => {
    id = id || storage.get('user_id');
    return api.get(`users/${id}/proposals/open`);
  };
  const getRecommended = () => {
    const id = storage.get('user_id');
    return api.get(`users/${id}/roles/recommended`);
  };

  const approveProposals = (id, body) => api.patch(`proposals/${id}`, body);
  const createPack = (payload) => api.post('packs', payload);
  const createRole = (payload) => api.post('roles', payload);
  const login = (creds) => api.post('authorization', creds);
  const getProposal = (id) => api.get(`proposals/${id}`);
  const getRole = (id) => api.get(`roles/${id}`);
  const getRoles = () => api.get('roles');
  const getPack = (id) => api.get(`packs/${id}`);
  const getPacks = () => api.get('packs');
  const getRelationships = (id) => api.get(`users/${id}/relationships`);
  const getRoot = () => api.get('');
  const getUser = (id) => api.get(`users/${id}`);
  const getUsers = () => api.get('users', { limit: 15 });
  const requestPackAccess = (id, body) => api.post(`packs/${id}/members`, body);
  const requestRoleAccess = (id, body) => api.post(`roles/${id}/members`, body);
  const search = (query) => api.post('', { q: query });
  const signup = (creds) => api.post('users', creds);


  return {
    approveProposals,
    createPack,
    createRole,
    login,
    getConfirmedProposals,
    getOpenProposals,
    getProposal,
    getRecommended,
    getRelationships,
    getRole,
    getRoles,
    getPack,
    getPacks,
    getRoot,
    getUser,
    getUsers,
    me,
    requestPackAccess,
    requestRoleAccess,
    search,
    signup,
  };
};


export default {
  create,
};
