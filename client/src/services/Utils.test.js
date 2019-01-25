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


import {
  createSlug,
  groupBy,
  merge,
  arraysEqual } from './Utils';


describe('Utils Service', () => {

  test('create slug', () => {
    expect(createSlug('1234')).toBe('1234');
    expect(createSlug('', { id: '1234' }))
      .toBe('1234');
  });


  test('test groupby', () => {
    groupBy([{ group: '' }], 'group');
  });


  test('test merge', () => {
    const array1 = [
      { name: 'john', role: 'old' },
      { name: 'mary' },
    ];
    const array2 = [
      { name: 'john', role: 'new' },
    ];
    const array3 = [
      { id: '123', members: [1] },
      { id: '456' },
    ];
    const array4 = [
      { id: '123', members: [1, 2, 3] },
    ];
    expect(merge(array1, array2, 'name')).toEqual([
      { name: 'john', role: 'new' },
      { name: 'mary' },
    ]);
    expect(merge(array3, array4)).toEqual([
      { id: '123', members: [1, 2, 3] },
      { id: '456' },
    ]);
  });


  test('test arraysEqual', () => {
    const array1 = ['one'], array2 = ['two'], array3 = ['three', 'four'];
    expect(arraysEqual([], [])).toEqual(true);
    expect(arraysEqual(array1, array2)).toEqual(false);
    expect(arraysEqual(array1, null)).toEqual(false);
    expect(arraysEqual(array1, array3)).toEqual(false);
  });
});
