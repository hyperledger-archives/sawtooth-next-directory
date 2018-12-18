
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { Message } from 'semantic-ui-react';

require('jest-localstorage-mock');

window.alert = (message) => {};

Enzyme.configure({ adapter: new Adapter() });

window.matchMedia = window.matchMedia || function () {
  return {
    matches: false,
    addListener: function () { },
    removeListener: function () { },
  };
};
