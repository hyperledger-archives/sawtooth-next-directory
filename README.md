![logo](logo.png)

# Hyperledger Sawtooth NEXT Identity Platform

[![Build Status](https://travis-ci.org/hyperledger/sawtooth-next-directory.svg?branch=master)](https://travis-ci.org/hyperledger/sawtooth-next-directory)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://github.com/hyperledger/sawtooth-next-directory/blob/master/LICENSE)

This repo contains multiple components which together with a
_Hyperledger Sawtooth_ validator, will comprise the "blockchain" components
of the NEXT Identity Platform project. The components include:

- a **server** which provides a REST API for querying blockchain data
- a **transaction processor** which handles RBAC-specific transaction logic
- a **ledger sync** which writes blockchain state changes to a local database


## Usage

The easiest way to run these components is with
[Docker](https://www.docker.com/what-docker). To start these components,
first install Docker for your platform and clone this repo.


To build and deploy the app, run:

```bash
docker-compose up
```

A shortcut is available via:
```bash
bin/start
```

This will build all components, start them in individual Docker containers,
and download and run the necessary Sawtooth components. Once complete, the
REST API will be available at **http://localhost:8000**.

Later, if the repo is updated, the local components will need to be rebuilt,
which can be accomplished using the `--build` flag:

```bash
docker-compose up --build
```

A shortcut is available via:
```bash
bin/start -b
```

Once all the docker containers are running without error, see ui/readme.md
for configuring / running the UI server.

## Development

#### System Dependencies 

The server code is written in python3. Confirm your version using command:

    python -V

If Python is missing or an earlier version, install python3 and pip3. 

PyYaml is required for running tests. Install it using pip3:

    pip3 install pyyaml


#### Deploying to Localhost

Docker containers are also available for developers, and are marked with a
`-dev` tag in their filename. There are a few differences between how these
containers work compared to the defaults:

- They do not need to be rebuilt when local files change
- Protobuf files will need to be built locally
- Some dependencies may need to be installed locally\*
- A _Sawtooth shell_ container is included for testing
- Sawtooth's blockchain REST API will be available at **http://localhost:8080**
- Rethink's database admin panel will be available at **http://localhost:9090**
- The NEXT UI will be available at **http://localhost:4200**

To start the dev containers, from the root project directory run:

```bash
bin/build -p
docker-compose -f docker-compose-dev.yaml -f docker-dev.yaml up
```

A shortcut is available via:
```bash
bin/build -p
bin/start -d
```

## Deploying to Any Non-Localhost Server

Pay special attention to the notes about secret keys in config.py.example. 
Due to their private/sensitive nature, the values of these keys should be 
provided to the application using 
  - a configuration file that is not stored/managed by git 
  - cli arguments 
  - some other means that prevents them from being publicly available
  
They are the most sensitive components for the security of your application.
Manage them wisely and responsibly.

When no such keys are provided, random keys are generated on application
bootstrap to simplify development. This avoids publication of the keys in
git and allows the application to start up in their absence. Work is 
underway to cause startup to fail fast and explosively when keys are missing.
Once that work is complete, the random key generation can be removed as well.
In other words: It must be made obvious to a user when startup fails due to 
missing keys.


## Testing

#### Populating Test Data

To quickly populate the application with test users, roles, etc., run script 
bin/populate_test_data.py once the application is up and running. It will spin up
a rest client and create the objects through the application's rest api.

#### Running Automated Tests

Tests can be run using the `run_docker_test` script, with the desired
docker-compose file as an argument. For example:

```bash
bin/build -p
bin/run_docker_test tests/docker-compose.yaml
```

A shortcut is available via:
```bash
bin/build -p
bin/build -i
```

# License

Hyperledger Sawtooth NEXT Identity Platform software is licensed under the 
[Apache License Version 2.0](LICENSE) software license.

# Acknowledgements

### Big Thanks

Cross-browser Testing Platform and Open Source <3 Provided by [Sauce Labs][homepage]

[homepage]: https://saucelabs.com