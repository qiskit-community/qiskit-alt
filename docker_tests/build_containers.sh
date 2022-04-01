#!/bin/sh

NOCACHE=--no-cache
#NOCACHE=

# Base image before installing qiskit_alt
# docker build -t qiskit_alt_base --rm=false -f Dockerfile0 ..

echo docker build $NOCACHE -t qiskit_alt_base1 --rm=false -f Dockerfile1 ..
docker build $NOCACHE -t qiskit_alt_base1 --rm=false -f Dockerfile1 ..

echo docker build $NOCACHE -t qiskit_alt_2 --rm=false -f Dockerfile2 ..
docker build $NOCACHE -t qiskit_alt_2 --rm=false -f Dockerfile2 ..

docker build $NOCACHE -t qiskit_alt_3 --rm=false -f Dockerfile3 ..
docker build $NOCACHE -t qiskit_alt_4 --rm=false -f Dockerfile4 ..
docker build $NOCACHE -t qiskit_alt_5 --rm=false -f Dockerfile5 ..
