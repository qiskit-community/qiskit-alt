#!/bin/bash

BUILD="docker build -t qiskit_alt -f Dockerfile .."

if [[ $1 == "build" ]]
then
    echo $BUILD
    $BUILD
elif [[ $1 == "run" ]]
then
    echo 'docker run -it qiskit_alt:latest  /usr/bin/su -l quser -c "cd qiskit_alt; sh ./run_init_tests.sh"'
    docker run -it qiskit_alt:latest  /usr/bin/su -l quser -c "cd qiskit_alt; sh ./run_init_tests.sh"
elif [[ $1 == "" ]]
then
    $BUILD
    echo 'docker run -it qiskit_alt:latest  /usr/bin/su -l quser -c "cd qiskit_alt; sh ./run_init_tests.sh"'
    docker run -it qiskit_alt:latest  /usr/bin/su -l quser -c "cd qiskit_alt; sh ./run_init_tests.sh"
else
    echo Excpecting argument "build" or "run", got $1
    echo "'run_dockerfile.sh build' to build image"
    echo "'run_dockerfile.sh run' to run tests in container"
    echo "'run_dockerfile.sh' to build, then run."
fi
