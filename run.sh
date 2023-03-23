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

docker_run () {
    docker build -f otree.Dockerfile -t $APP ./$APP
    docker run --rm -it "$@"
}

case $1 in
    dev)
        RUN_CMD="otree devserver 0.0.0.0:8000"
        docker_run -v $VOLUME_PATH -p "8000:8000" $APP $RUN_CMD
        ;;
    tests)
        RUN_CMD="otree test $TEST_NAME $TEST_USERS"
        docker_run $APP $RUN_CMD
        ;;
    lint)
        IMAGE="pyfound/black:latest_release"
        docker run --rm -v $VOLUME_PATH -w //app $IMAGE black .
        ;;
    prod)
        docker compose up
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
