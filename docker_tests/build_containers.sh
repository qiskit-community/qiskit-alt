#!/bin/sh

docker build -t qiskit_alt_base --rm=false -f Dockerfile0 ..
docker build -t qiskit_alt_base1 --rm=false -f Dockerfile1 ..
docker build -t qiskit_alt_2 --rm=false -f Dockerfile2 ..
docker build -t qiskit_alt_3 --rm=false -f Dockerfile3 ..
docker build -t qiskit_alt_4 --rm=false -f Dockerfile4 ..
