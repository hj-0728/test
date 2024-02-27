#!/bin/bash
PROJECT_DIR=/data/projects/edu-binshi-school-evaluation
CODE_DIR=$PROJECT_DIR/edu-binshi-school-evaluation-code
RUNTIME_DIR=$PROJECT_DIR/frontend-web
ARCHIVE_DIR=$PROJECT_DIR/archive/frontend-web
cd $CODE_DIR
git pull

cd $CODE_DIR/frontend_web
pnpm install

npm run build:staging


NOW=`date +%Y-%m-%d.%H.%M.%S`
cp $RUNTIME_DIR $ARCHIVE_DIR/$NOW -r
sudo rm $RUNTIME_DIR -rf
mv $CODE_DIR/frontend_web/dist $RUNTIME_DIR 


