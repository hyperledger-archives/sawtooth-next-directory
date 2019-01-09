#!/bin/bash

# Start ssh-agent cache and adds decrypted private key
eval "$(ssh-agent -s)"
chmod 600 .travis/id_rsa
ssh-add .travis/id_rsa

# Add a remote called deploy and pushes the master branch to the remote
git remote add deploy ssh://$DEPLOY_USER@$IP/~/$DEPLOY_DIR
git push deploy master

# If the commit message contains the phrase 'RESET_NEXT_STORAGE', this deployment will 
# reset the data on the remote server back to genesis. Volumes might be named differently,
# refer to documentation in ~/docker-persist.yaml for additional information.
if [[ $TRAVIS_COMMIT_MESSAGE = *"RESET_NEXT_STORAGE"* ]] ; then
    RESTART_CONTAINER="sudo docker volume rm sawtooth-next-directory_chain
    sudo docker volume rm sawtooth-next-directory_keys
    sudo docker volume rm sawtooth-next-directory_db
    "
fi

RESTART_CONTAINER+="sudo docker-compose -f docker-compose.yaml -f docker-persist.yaml up -d --build"

# SSH into the remote server and start NEXT Directory Platform 
ssh $DEPLOY_USER@$IP <<EOF
    cd $DEPLOY_DIR
    sudo docker-compose down &
    export PID=$!
    wait $PID
    sudo docker-compose -f docker-compose.yaml -f docker-persist.yaml up -d --build
EOF
