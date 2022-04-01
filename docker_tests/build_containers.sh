#!/bin/sh

# Some rebuilding is not triggered, even when qiskit_alt source changes
NOCACHE=--no-cache
#NOCACHE=

# Base image before installing qiskit_alt
# docker build -t qiskit_alt_base --rm=false -f Dockerfile0 .. | tee dockerfile0.log

echo docker build $NOCACHE -t qiskit_alt_base1 --rm=false -f Dockerfile1 ..
docker build $NOCACHE -t qiskit_alt_base1 --rm=false -f Dockerfile1 .. | tee dockerfile1.log

echo docker build $NOCACHE -t qiskit_alt_2 --rm=false -f Dockerfile2 ..
docker build $NOCACHE -t qiskit_alt_2 --rm=false -f Dockerfile2 .. | tee dockerfile2.log

echo docker build $NOCACHE -t qiskit_alt_3 --rm=false -f Dockerfile3 ..
docker build $NOCACHE -t qiskit_alt_3 --rm=false -f Dockerfile3 .. | tee dockerfile3.log

echo docker build $NOCACHE -t qiskit_alt_4 --rm=false -f Dockerfile4 ..
docker build $NOCACHE -t qiskit_alt_4 --rm=false -f Dockerfile4 .. | tee dockerfile4.log

echo docker build $NOCACHE -t qiskit_alt_5 --rm=false -f Dockerfile5 ..
docker build $NOCACHE -t qiskit_alt_5 --rm=false -f Dockerfile5 .. | tee dockerfile5.log
