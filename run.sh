#!/bin/sh

source ./.env

# MINGW formats paths differently
if [ $(uname | grep MINGW) ]
then
    VOLUME_PATH="//$(pwd)/$APP:/app"
else
    VOLUME_PATH="./$APP:/app"
fi

print_usage () {
    echo
    echo 'Usage: run.sh OPTION'
    echo
    echo 'OPTION should be either "dev", "tests" "lint" or "prod"'
}

docker_build () {
    docker build -f otree.Dockerfile -t $APP ./$APP
}

case $1 in
    dev)
        docker_build
        docker run -it --rm -v $VOLUME_PATH -p "8000:8000" \
            --env-file ./.dev.env $APP otree devserver 0.0.0.0:8000
        ;;
    tests)
        docker_build
        docker run $APP otree test $TEST_NAME $TEST_USERS
        ;;
    lint)
        docker run --rm -v $VOLUME_PATH -w //app \
            pyfound/black:latest_release black .
        ;;
    prod)
        docker compose up
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
