#### Testing installation with docker

You can build the docker image by changing to the `./docker_tests` directory and doing
```shell
docker build -t qiskit_alt -f Dockerfile .. | tee dockerfile.log
```
You can run some installation tests like this
```shell
docker run -it qiskit_alt:latest  /usr/bin/su -l quser -c "cd qiskit_alt; sh ./run_init_tests.sh"
```

#### Working in the docker container

To experiment with the docker container you can do
```shell
docker run -it qiskit_alt /usr/bin/su -l quser -s /usr/bin/fish
```
This example uses the fish shell.
