#!/bin/sh

source ./.env

function build_run {
    # Builds docker images and runs container with given options/command
    # - First argument is options to 'docker run'
    # - Second argument is command for 'docker run' to execute

    docker build -t $APP --build-arg APP=$APP .
    docker run --rm -it $1 $APP $2
}

# MINGW formats paths differently
if [ $(uname | grep MINGW) ]
then
    VOLUME_PATH="//$(pwd)/$APP:/app"
else
    VOLUME_PATH="./$APP:/app"
fi

case $1 in
    dev)
        build_run "-p 8000:8000 -v $VOLUME_PATH" "otree devserver 0.0.0.0:8000"
        ;;
    tests)
        build_run "-v $VOLUME_PATH" "otree test $TEST_NAME $TEST_USERS"
        ;;
    lint)
        docker run --rm --volume "$VOLUME_PATH" --workdir //app pyfound/black:latest_release black .
        ;;
    prod)
        # Does not require a command as it is already defined in Dockerfile
        build_run "-p 8000:8000 --env-file .prod.env"
        ;;
    *)
        echo
        echo 'Usage: run.sh OPTION'
        echo
        echo 'OPTION should be either "dev", "tests" "lint" or "prod"'
        exit 1
        ;;
esac
