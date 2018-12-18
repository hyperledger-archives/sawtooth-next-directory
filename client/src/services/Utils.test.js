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


import { createSlug, groupBy, merge } from './Utils';


describe('Utils Service', () => {

  test('create slug', () => {
    expect(createSlug('create Slug string')).toBe('create-slug-string');
    expect(createSlug('', { name: 'create slug string' }))
      .toBe('create-slug-string');
  });

  test('test groupby', () => {
    groupBy([{ group: '' }], 'group');
  });

  test('test merge', () => {
    const array1 = ['firstname'], array2 = ['lastname'];
    expect(merge(array1, array2)).toEqual([...array1, ...array2]);

  });

});
