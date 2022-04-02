#!/bin/sh

# Some rebuilding is not triggered, even when qiskit_alt source changes
#NOCACHE=--no-cache
NOCACHE=
#RMINTER=--rm=false
RMINTER=

# Install everything except qiskit_alt itself
docker build -t qiskit_alt_base $RMINTER -f Dockerfile0 .. | tee dockerfile0.log

# Install qiskit_alt Python package in development mode
echo docker build $NOCACHE -t qiskit_alt_base1 $RMINTER -f Dockerfile1 ..
docker build $NOCACHE -t qiskit_alt_base1 $RMINTER -f Dockerfile1 .. | tee dockerfile1.log

# Run ensure_init on fresh install. Use juliacall, and some particular options
echo docker build $NOCACHE -t qiskit_alt_2 $RMINTER -f Dockerfile2 ..
docker build $NOCACHE -t qiskit_alt_2 $RMINTER -f Dockerfile2 .. | tee dockerfile2.log

# Same as above, but use pyjulia rather than juliacall
echo docker build $NOCACHE -t qiskit_alt_3 $RMINTER -f Dockerfile3 ..
docker build $NOCACHE -t qiskit_alt_3 $RMINTER -f Dockerfile3 .. | tee dockerfile3.log

# Install conda, and set up for both root and user quser. Create environment qiskit_alt_env
echo docker build $NOCACHE -t qiskit_alt_4 $RMINTER -f Dockerfile4 ..
docker build $NOCACHE -t qiskit_alt_4 $RMINTER -f Dockerfile4 .. | tee dockerfile4.log

# Setup a venv using a python statically linked to libpython and install everything needed except qiskit_alt.
# This is very similar to Dockerfile0, except that used a dynamically linked python.
# We are not using a conda env, but rather a venv. However we use the python executable that was installed
# by conda, because this is statically linked. This is incompatible with pyjulia, which is what we want.
# We need to also try conda. But, learning to use conda in a docker container is difficult.
echo docker build $NOCACHE -t qiskit_alt_5 $RMINTER -f Dockerfile5 ..
docker build $NOCACHE -t qiskit_alt_5 $RMINTER -f Dockerfile5 .. | tee dockerfile5.log

# Install qiskit_alt in dev mode on qiskit_alt_5
echo docker build $NOCACHE -t qiskit_alt_6 $RMINTER -f Dockerfile6 ..
docker build $NOCACHE -t qiskit_alt_6 $RMINTER -f Dockerfile6 .. | tee dockerfile6.log
