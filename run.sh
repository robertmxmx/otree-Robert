#!/bin/sh

source ./.env

# MINGW formats paths differently
VOLUME_PATH="$([ $(uname | grep MINGW) ] && echo //)$(pwd)/$APP:/app"

print_usage () {
    echo
    echo "Usage: run.sh OPTION"
    echo
    echo "OPTION is any of the following"
    echo "  dev      Run app in development mode"
    echo "  prod     Run app in production mode"
    echo "  tests    Use bots to run tests"
    echo "  lint     Use linting tools to format files"
    echo
    echo "tests arguments"
    echo "  -e       Export bot data to files"
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
        args="$TEST_NAME $TEST_USERS $([ "$2" = "-e" ] && echo --export)"

        docker_build
        docker run -v $VOLUME_PATH $APP otree test $args
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
