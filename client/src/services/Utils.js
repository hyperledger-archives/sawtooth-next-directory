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

export const createSlug = (name, parent) => {
  let slug = (parent && parent.name) ? parent.name : name;
  try {
    return slug && slug
      .toLowerCase()
      .replace(/ /g, '-')
      .replace(/[^\w-]+/g, '');
  } catch (error) {
    console.error(error);
    console.error('Invalid resource name: ', name);
    return '';
  }
}


export const createHomeLink = (packs = [], roles = []) => {
  try {
    if (packs && packs.length > 0)
      return `/packs/${createSlug(packs[0].name)}`;
    else if (roles && roles.length > 0 )
      return `/roles/${createSlug(roles[0].name)}`;
    return '/';
  } catch (error) {
    console.error(error);
    console.error('Error creating home link');
    return '/';
  }
}


export const groupBy = (array, key) => {
  return array && array.reduce((prev, curr) => {
    prev[curr[key]] = prev[curr[key]] || [];
    prev[curr[key]].push(curr);
    return prev;
  }, Object.create(null));
}


export const merge = (array1, array2) => {
  return [...new Set([
    ...array1,
    ...array2,
  ]
    .map(object => JSON.stringify(object)))]
    .map(string => JSON.parse(string));
}
