# I used fedora:34 rather than fedora:35 as the base image because of
# https://bugzilla.redhat.com/show_bug.cgi?id=1988199.
# Comment 26 there points to an upstream RHEL bug, but I am not
# certain it is the same bug as I was experiencing [garrison].
FROM fedora:34

### Install all needed packages from distribution and remove the package download cache.
RUN dnf install -y git @development-tools gcc-c++ python3 python3-devel passwd fish emacs wget && \
      dnf clean dbcache

# Is the followig necessary ?
RUN python3 -m pip install -U pip

### Create a user 'quser' and add to sudoers

RUN useradd --create-home --shell /bin/bash quser && echo "quser:quser" | chpasswd && \
    usermod -aG wheel quser && mkdir /home/quser/qiskit_alt && chown -R quser /home/quser && chgrp -R quser /home/quser

### Change quser

WORKDIR /home/quser/qiskit_alt
USER quser

### Create a virtual envirnoment venv1, install jill.py, and install julia via jill.py

RUN python3 -m venv ./venv1 && source ./venv1/bin/activate && pip install --upgrade pip jill && \
    jill install --confirm
# Note 'printf "y\n" | jill install' works at the cli, but not here :(

### Install all python packges needed for qiskit_alt in venv1, but not qiskit_alt.

COPY --chown=quser requirements.txt .
RUN source ./venv1/bin/activate && pip install ipython && \
    pip install --requirement requirements.txt

### Do system-wide install of miniconda

SHELL ["/bin/bash", "--login", "-c"]

USER root
WORKDIR /root
# Install miniconda
ENV CONDA_DIR /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

RUN conda init bash && conda init fish && conda config --set auto_activate_base false

### Setup conda for user quser

USER quser
WORKDIR /home/quser/qiskit_alt

ENV CONDA_DIR /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

RUN printf "y\n" |  conda create -n qiskit_alt_env python=3.9
RUN conda init bash && conda init fish && conda config --set auto_activate_base false

## Use conda-installed python to create a venv virtual environment.  This venv is
## unrelated to conda. But, we do it because the conda-installed python is statically
## linked to libpython. This allows us to test both statically and dynamically linked
## python.

RUN /opt/conda/bin/python -m venv ./venv_static && \
    source ./venv_static/bin/activate && pip install --upgrade pip ipython && \
    pip install --requirement requirements.txt

## Create a conda environment called qiskit_alt_env

RUN conda activate qiskit_alt_env && pip install ipython && pip install --requirement requirements.txt

### Copy all and only files required for pip install of qiskit_alt in dev mode

COPY --chown=quser requirements.txt setup.cfg  pyproject.toml README.md ./
COPY --chown=quser src ./src/

### Install qiskit_alt into the three virtual environments we have created.

RUN source ./venv1/bin/activate && pip install -e .
RUN source ./venv_static/bin/activate && pip install -e .
RUN conda activate qiskit_alt_env && pip install -e .

### Copy files used to test initializing qiskit_alt. That is downloading Julia packages, etc.

COPY --chown=quser init_test.py run_init_tests.sh ./

### Start container as root user by default.
### This is less necessary now the we put quser in sudoers group.

USER root
WORKDIR /root
