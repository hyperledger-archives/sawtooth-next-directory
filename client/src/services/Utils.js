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


/**
 *
 * Create a URL-friendly string
 *
 * @param {string} name    String used to create slug
 * @param {object} parent
 *        Object containing name field to poll on
 *        availability.
 *
 *        If an object is passed before it is ready
 *        to render, the function will be polled by Redux
 *        until a name field exists and a slug can be created
 *
 * @returns {string}
 *
 */

export const createSlug = (id, parent) => {
  let slug = parent && parent.id ? parent.id : id;
  try {
    return slug;
  } catch (error) {
    console.error('Invalid resource ID.');
    return '';
  }
};


export const createHomeLink = (packs = [], roles = []) => {
  try {
    if (packs && packs.length > 0)
      return `/packs/${createSlug(packs[0])}`;

    else if (roles && roles.length > 0)
      return `/roles/${createSlug(roles[0].id)}`;
    return '/';
  } catch (error) {
    console.error(error);
    console.error('Error creating home link');
    return '/';
  }
};


export const groupBy = (array, key) => {
  return array && array.reduce((prev, curr) => {
    prev[curr[key]] = prev[curr[key]] || [];
    prev[curr[key]].push(curr);
    return prev;
  }, Object.create(null));
};


export const merge = (array1, array2) => {
  return [...new Set([
    ...array1,
    ...array2,
  ]
    .map(object => JSON.stringify(object)))]
    .map(string => JSON.parse(string));
};


export const arraysEqual = (array1, array2) => {
  if (array1 === array2) return true;
  if (array1 == null || array2 == null) return false;
  if (array1.length !== array2.length) return false;

  for (let i = 0; i < array1.length; ++i)
    if (array1[i] !== array2[i]) return false;

  return true;
};


export const noop = () => {};
