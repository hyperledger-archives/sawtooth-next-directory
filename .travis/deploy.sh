#!/bin/bash

# Start ssh-agent cache and adds decrypted private key
eval "$(ssh-agent -s)"
chmod 600 .travis/id_rsa
ssh-add .travis/id_rsa

# Add a remote called deploy and pushes the master branch to the remote
git remote add deploy ssh://$DEPLOY_USER@$IP/~/$DEPLOY_DIR
git push deploy master

# SSH into the remote server and start NEXT Directory Platform
ssh $DEPLOY_USER@$IP <<EOF
    cd $DEPLOY_DIR
    sudo docker-compose down &
    export PID=$!
    wait $PID
    sudo docker-compose -f docker-compose.yaml -f docker-persist.yaml up -d --build
EOF
