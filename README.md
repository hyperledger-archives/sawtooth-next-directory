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
- Some dependencies may need to be installed locally\*
- A _Sawtooth shell_ container is included for testing
- Sawtooth's blockchain REST API will be available at **http://localhost:8080**
- Rethink's database admin panel will be available at **http://localhost:9090**
- The NEXT UI will be available at **http://localhost:4200**

To start the dev containers, from the root project directory run:

```bash
bin/build -p
docker-compose -f docker-compose.yaml -f docker-dev.yaml up
```

A shortcut is available via:
```bash
bin/build -p
bin/start -d
```

#### Deploying Multi-Node Network

The multi-node network consists of four nodes (more can be added) hosting Sawtooth 
Next Directory. The multi-node network utilizes the PoET simulator consensus 
between the validators allowing PoET to run on non-SGX hardware. 

After starting the containers, the Next Directory UI will be available at:
- **http://10.5.0.70:4200** (node 0)
- **http://10.5.0.71:4200** (node 1)
- **http://10.5.0.72:4200** (node 2)
- **http://10.5.0.73:4200** (node 3)


To start the containers in a multi-node configuration run:
```bash
docker-compose -f docker-multi-node.yaml up
```


## Deploying to Any Non-Localhost Server

Pay special attention to the notes about secret keys in .env. 
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

Unit tests can be run using (pytest)[https://docs.pytest.org/en/latest/]:

```bash
pytest
```

Integration tests can be run using the `run_docker_test` script, with the desired
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

#### Cleaning the Docker Image Cache

Docker-compose relies on image caching to improve build and deployment time. Some changes (directory renaming, etc)
can cause the loading of cached images to result in build failures in docker-compose. In addition, not shutting down
containers properly by doing a docker-compose down also leads to this scenario. When it occurs, you will experience
hanging in the legacy UI and stack traces from rbac_server:

     Traceback (most recent call last):
    rbac-server    |   File "/usr/local/lib/python3.5/dist-packages/sanic/app.py", line 556, in handle_request
    rbac-server    |     response = await response
    rbac-server    |   File "/usr/lib/python3.5/asyncio/coroutines.py", line 105, in __next__
    rbac-server    |     return self.gen.send(None)
    rbac-server    |   File "/project/tmobile-rbac/server/api/users.py", line 74, in create_new_user
    rbac-server    |     request.app.config.AES_KEY, txn_key.public_key, private_key.as_bytes()
    rbac-server    |   File "/project/tmobile-rbac/server/api/utils.py", line 172, in encrypt_private_key
    rbac-server    |     cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, init_vector)
    rbac-server    | ValueError: non-hexadecimal number found in fromhex() arg at position 30

To work around this situation, shut down the application, delete all containers and images, and rebuild/deploy:

    docker-compose down

    docker rm -vf $(docker ps -a -q)

    docker rmi -f $(docker images -a -q)

    docker-compose up --build
    


# License

Hyperledger Sawtooth NEXT Identity Platform software is licensed under the 
[Apache License Version 2.0](LICENSE) software license.

# Acknowledgements

### Big Thanks

Cross-browser Testing Platform and Open Source <3 Provided by [Sauce Labs][homepage]

[homepage]: https://saucelabs.com