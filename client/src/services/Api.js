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


  /**
   *
   * Definitions
   *
   *
   */
  const me = () => {
    const userId = storage.get('user_id');

    api.setHeaders({ 'Authorization': storage.getToken() });
    return api.get(`users/${userId}`);
  }

  const login = (creds) => api.post('authorization', creds);
  const getPack = (id) => api.get(`roles/${id}`);
  const getProposal = (id) => api.get(`proposals/${id}`);
  const getRequesterBase = () => api.get('me/base');
  const getRoles = () => api.get('roles');
  const getRoot = () => api.get('');
  const requestAccess = (id, body) => api.post(`roles/${id}/members`, body);
  const search = (query) => api.post('', { q: query });
  const signup = (creds) => api.post('users', creds);


  return {
    login,
    getPack,
    getProposal,
    getRequesterBase,
    getRoles,
    getRoot,
    me,
    requestAccess,
    search,
    signup
  }

}

export default {
  create
}
