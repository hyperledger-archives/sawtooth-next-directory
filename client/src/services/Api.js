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
import * as storage from '../services/Storage';
import * as AuthActions from '../redux/AuthRedux';


/**
 *
 * Encapsulated service that eases configuration and other
 * API-related tasks.
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
 */
const create = (baseURL = 'http://localhost:8000/api/') => {

  /**
   *
   * Create and configure API object
   *
   *
   */
  const api = apisauce.create({
    baseURL
  });


  const setHeaders = () => {
    api.setHeaders({ 'Authorization': storage.getToken() });
  }


    /**
   *
   * Added condition for unauthorized API call.
   *
   *
   */
  api.addResponseTransform(response => {
    if (response.data.code === 401) {
      AuthActions.logout();
    }
  });


  /**
   *
   * Definitions
   *
   *
   */
  const me = () => {
    setHeaders();
    const id = storage.get('user_id');
    return api.get(`users/${id}`);
  }

  const getRoles = () => {
    setHeaders();
    return api.get('roles');
  }

  const getOpenProposals = () => {
    const id = storage.get('user_id');
    return api.get(`users/${id}/proposals/open`);
  }


  const login = (creds) => api.post('authorization', creds);
  const getProposal = (id) => api.get(`proposals/${id}`);
  const getRequesterBase = () => api.get('me/base');
  const getRole = (id) => api.get(`roles/${id}`);
  const getRoot = () => api.get('');
  const getUser = (id) => api.get(`users/${id}`);
  const requestAccess = (id, body) => api.post(`roles/${id}/members`, body);
  const search = (query) => api.post('', { q: query });
  const signup = (creds) => api.post('users', creds);


  return {
    login,
    getOpenProposals,
    getProposal,
    getRequesterBase,
    getRole,
    getRoles,
    getRoot,
    getUser,
    me,
    requestAccess,
    search,
    signup
  }

}

export default {
  create
}
