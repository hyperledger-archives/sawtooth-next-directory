# T-Mobile RBAC Blockchain Components

This repo contains multiple components which together with a
_Hyperledger Sawtooth_ validator, will comprise the "blockchain" components
of the T-Mobile _Role Based Access Control_ project. The components in this
repo include:

- a **server** which provides a REST API for querying blockchain data
- a **transaction processor** which handles RBAC-specific transaction logic
- a **ledger sync** which writes blockchain state changes to a local database


##Usage

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


##Development

Docker containers are also available for developers, and are marked with a
`-dev` tag in their filename. There are a few differences between how these
containers work compared to the defaults:

- they do not need to be rebuilt when local files change
- most dependencies will have to be installed locally
- _Sawtooth REST API_ and _Sawtooth shell_ containers are included for testing
- Rethink's database admin panel is available at **http://localhost:9090**

To start the dev containers, from the root project directory run:

```bash
bin/build -p
docker-compose -f docker-compose-dev.yaml up
```

In addition to locally installing Sawtooth dependencies like the
`sawtooth_sdk`, it is likely some `pip3` dependencies will need to be
installed to run this command.


##Testing

Tests can be run using the `run_docker_test` script, with the desired
docker-compose file as an argument. For example:

```bash
bin/run_docker_test integration_tests/blockchain_integration_tests.yaml
```
