### Working on Julia packages within qiskit_alt

You can start by using qiskit_alt to set up the Julia project for you.

If you are just using qiskit_alt, you can give the command `pip install qiskit_alt`.
You might try this just to explore a bit.
But, since you want to develop qiskit-alt it is better to install it in development mode.

```shell
> git clone https://github.com/Qiskit-Extensions/qiskit-alt
> cd qiskit-alt
```

(Really, a better idea is to go to github and fork qiskit-alt, then pull the repostory to
your machine as instructed)

You typically want to work in a virtual environment that is specific to your development
clone of `qiskit_alt`. So for example in linux (maybe macos too) and
using the standard bash shell, you do (inside the qiskit-alt directory)

```shell
> python -m venv ./venv
> source ./venv/bin/activate  # Activate this environment
```
Just use the command 'deactivate' alone to deactivate the environment later.

Alternatively, you may want to use `conda`; i.e. instead of `venv`. Use only one or the other
at a time.
First install conda. Then do something like
```shell
> conda create -n qiskit_alt_env python=3.9
> conda activate qiskit_alt_env
```
I used python 3.9 here because conda installed 3.10 the first time I tried this. Qiskit
is (probably still?) pegged at python 3.9 because it depends on pyscf which also has this
restriction.

Now use this shell with the active virtual environment to run your command line interface or Jupyter notebook, or whatever you are going to use.
I use `ipython` as a cli. It has a few good advantages over `python`. With the virtual
environment active, we do
```shell
> pip install --upgrade pip ipython # upgrade pip to silence complaints
```
Now you can install qiskit-alt in development mode like this
```shell
> pip install -e .
```

Do the first initialization of qiskit-alt.
```python
> ipython
In [1]: import qiskit_alt
In [2]: qiskit_alt.project.ensure_init()
```
