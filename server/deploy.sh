#!/bin/bash

# Required env variables:
#   SERVICE_NAME
#   DEPLOY_PATH
#   SOURCE_DIR
#   APP_OWNER
if [ $# -eq 0 ]
    then
        echo "Missing environment configuration argument"
    else
        service $SERVICE_NAME stop
        rm -rf $DEPLOY_PATH
        mkdir $DEPLOY_PATH
        cp -r $SOURCE_DIR/src/* $DEPLOY_PATH
        cp $1 $DEPLOY_PATH/.current.env

        cd $SOURCE_DIR
        pip install -r requirements.txt
        cd $DEPLOY_PATH
        python manage.py migrate
        python manage.py seed
        chown -R $APP_OWNER .
        service $SERVICE_NAME start
fi


