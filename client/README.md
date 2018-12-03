# React Client
The NEXT Directory client is a browser-based React application.

## Getting started
### Docker
After running NEXT with either of the following commands:

`./bin/start` or `docker-compose up`

The client will be available at **[http://localhost:4201](http://localhost:4201)**.

If you need to run the app outside of Docker, the following commands are available:

#### `yarn start`
> Runs the React client in development mode.
> Open **[http://localhost:3000](http://localhost:3000)** to view it in the browser.

#### `yarn build`
> Builds the app for production to the `build` folder.

When running the application using Docker, the development server automatically takes care of hot reloading.

### Tests
Unit tests can be run using the following command:

#### `yarn test`
> Runs the test watcher in an interactive mode.

Lint is run using the following:

#### `yarn lint`
> Runs [ESLint](https://github.com/eslint/eslint) on the `./src` directory.

### CSS

The NEXT Directory client uses [Semantic UI](https://github.com/Semantic-Org/Semantic-UI) for baseline styling. To build Semantic UI after editing its source in `./src/semantic`, you will need to install Gulp > 4.0 by running:

`yarn global add gulp` or `npm i -g gulp`

Then, run the following command:

#### `yarn build:semantic`
> Builds Semantic UI styles, creating compiled assets in `./src/semantic` and `./src/semantic/dist`.

Alternative, you can allow Semantic UI to watch for changes:

#### `yarn watch:semantic`
> Watch for changes to Semantic UI source in `./src/semantic/themes` and `./src/semantic/site`, building to `./src/semantic/dist` and `./src/semantic/*.css|js`

The client will automatically reload after the source is built.

### Documentation

All client code is documented using [JSDoc](https://github.com/jsdoc3/jsdoc) and can be found in `./docs`. JSDoc requires doc-style commenting.

To update the documentation, run:

#### `yarn docs`
> Generate JSDoc documentation

Open `index.html` in `./docs` in your browser to view the complete documentation.
