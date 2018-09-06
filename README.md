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

Next, create a `server/config.py` file based off the example at
`server/config.py.example`. Pay special attention to the secret keys at the
bottom of the example file. While other settings have defaults and can be
omitted, these keys have no defaults and _must_ be provided to run the server.
The examples listed are insecure, and should be replaced before deployment.

Once there is a config file in place, you can simply run:

```bash
docker-compose up
```

This will build all components, start them in individual Docker containers,
and download and run the necessary Sawtooth components. Once complete, the
REST API will be available at **http://localhost:8000**.

Later, if the repo is updated, the local components will need to be rebuilt,
which can be accomplished using the `--build` flag:

```bash
docker-compose up --build
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

To start the dev containers, from the root project directory run:

```bash
bin/build -p
docker-compose -f docker-compose-dev.yaml up
```


## Testing

Tests can be run using the `run_docker_test` script, with the desired
docker-compose file as an argument. For example:

```bash
bin/run_docker_test integration_tests/blockchain/docker-compose.yaml
bin/run_docker_test integration_tests/api/docker-compose.yaml
```

# License

Hyperledger Sawtooth NEXT Identity Platform software is licensed under the [Apache License Version 2.0](LICENSE) software license.
