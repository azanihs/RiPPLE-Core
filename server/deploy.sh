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
        today=`date '+%Y_%m_%d__%H_%M_%S'`
        mv $DEPLOY_PATH/rippledb $OLD_DATA/$today-rippledb
        rm -rf $DEPLOY_PATH
        mkdir $DEPLOY_PATH
        cp -r $SOURCE_DIR/src/* $DEPLOY_PATH
        cp $1 $DEPLOY_PATH/.env.current

        cd $SOURCE_DIR
        pip3 install -r requirements.txt
        cd $DEPLOY_PATH
        python3 manage.py migrate
        #python3 manage.py seed --dataset=/home/uqnjosep/RiPPLE-Core/migration/exportJSON --host $SERVER_HOST
        chown -R $APP_OWNER .
        service $SERVICE_NAME start
fi


