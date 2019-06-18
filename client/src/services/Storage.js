/* Copyright 2019 Contributors to Hyperledger Sawtooth

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


const tokenKey = 'RBAC_AUTH_TOKEN';
const viewKey = 'RBAC_APPROVER_VIEW_ENABLED';
const userIdKey = 'next_id';


export const getToken = () => get(tokenKey);
export const setToken = (value) => set(tokenKey, value);
export const removeToken = () => remove(tokenKey);


export const getViewState = () => get(viewKey);
export const setViewState = (value) => set(viewKey, value);
export const removeViewState = () => remove(viewKey);


export const getUserId = () => get(userIdKey);
export const setUserId = (value) => set(userIdKey, value);
export const removeUserId = () => remove(userIdKey);


export const get = (key) =>
  localStorage.getItem(key);


export const set = (key, value) =>
  localStorage.setItem(key, value);


export const remove = (key) =>
  localStorage.removeItem(key);
