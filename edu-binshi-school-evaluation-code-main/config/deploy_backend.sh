#!/bin/bash
PROJECT_DIR=/data/projects/edu-binshi-school-evaluation
CODE_DIR=$PROJECT_DIR/edu-binshi-school-evaluation-code
RUNTIME_DIR=$PROJECT_DIR/runtime
SERVICE_BACKEND=edu-binshi-school-evaluation-backend
SERVICE_SCHEDULER=edu-binshi-school-evaluation-scheduler
SERVICE_PUBSUB=edu-binshi-school-evaluation-pubsub
SERVICE_PUBSUB=edu-binshi-school-evaluation-pubsub

cd $CODE_DIR

git pull
sudo systemctl stop $SERVICE_BACKEND
sudo systemctl stop $SERVICE_SCHEDULER
sudo systemctl stop $SERVICE_PUBSUB

sudo rm -rf $RUNTIME_DIR
cp -r $CODE_DIR $RUNTIME_DIR
cd $RUNTIME_DIR
source /home/ubuntu/.profile
pyenv activate edu-binshi-school-evaluation-env
poetry install
cp $PROJECT_DIR/conf/app.toml $RUNTIME_DIR
sudo systemctl start $SERVICE_BACKEND
sudo systemctl start $SERVICE_SCHEDULER
sudo systemctl start $SERVICE_PUBSUB


