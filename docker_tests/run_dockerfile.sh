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
elif [[ $1 == "fish" ]]
then
    docker run -it qiskit_alt /usr/bin/su -l quser -s /usr/bin/fish
elif [[ $1 == "bash" ]]
then
    docker run -it qiskit_alt /usr/bin/su -l quser -s /usr/bin/bash
elif [[ $1 == "rootfish" ]]
then
    docker run -it qiskit_alt /usr/bin/fish
else
    echo Expecting argument "build" or "run", got $1
    echo "'run_dockerfile.sh build' to build image"
    echo "'run_dockerfile.sh run' to run tests in container"
    echo "'run_dockerfile.sh' to build, then run."
    echo "'run_dockerfile.sh fish' for an interactive fish shell"
    echo "'run_dockerfile.sh bash' for an interactive bash shell"
fi
