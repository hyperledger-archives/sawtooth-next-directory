const assert = require('assert');
const webdriver = require('selenium-webdriver');
const gecko = require('geckodriver');


const appTitle = 'NEXT Directory';


let browser;
let serverUri;


/**
 * 
 * Configure Browser
 * 
 * 
 */
if (!process.env.CI) {
  serverUri = 'http://localhost:3000';

  browser = new webdriver.Builder()
    .usingServer()
    .withCapabilities({ browserName: 'chrome' })
    .build();
} else {
  serverUri = 'https://next.app.ci';

  // Sauce Labs
  // TODO: Encrypt and/or move to environment variables
  let username = 'pgobin';
  let accessKey = '2887ebb8-f09b-428f-9b3f-5c01132e0e27';
  

  browser  = new webdriver.Builder()
    .usingServer()
    .withCapabilities({
      browserName: 'chrome',
      username: username,
      accessKey: accessKey,
      'tunnel-identifier': process.env.TRAVIS_JOB_NUMBER,
      build: process.env.TRAVIS_BUILD_NUMBER
      })
    .usingServer('http://' + username + ':' + accessKey + '@ondemand.saucelabs.com:80/wd/hub')
    .build();
}


function logTitle() {
  return new Promise((resolve, reject) => {
    browser.getTitle().then(function(title) {
      resolve(title);
    });
  });
}


/**
 * 
 * Home Page
 * 
 */
describe('Home Page', function() {

  it('Should load the home page and get title', function() {
    return new Promise((resolve, reject) => {
      browser
        .get(serverUri)
        .then(logTitle)
        .then(title => {
          assert.strictEqual(title, appTitle);
          resolve();
        })
        .catch(err => reject(err));
    });
  });

  after(function() {
    browser.quit();
  });

});
