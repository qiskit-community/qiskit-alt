# I used fedora:34 rather than fedora:35 as the base image because of
# https://bugzilla.redhat.com/show_bug.cgi?id=1988199.
# Comment 26 there points to an upstream RHEL bug, but I am not
# certain it is the same bug as I was experiencing [garrison].
FROM fedora:34

RUN dnf install -y git @development-tools gcc-c++ python3 python3-devel passwd fish emacs wget && \
      dnf clean dbcache
# Is the followig necessary ?
RUN python3 -m pip install -U pip
RUN useradd --create-home --shell /bin/bash quser && echo "quser:quser" | chpasswd

WORKDIR /home/quser/qiskit_alt
RUN chown -R quser . && chgrp -R quser .
USER quser
RUN python3 -m venv ./venv1 && source ./venv1/bin/activate && pip install --upgrade pip jill
# Note 'printf "y\n" | jill install' works at the cli, but not here :(

COPY --chown=quser requirements.txt .
RUN source ./venv1/bin/activate && jill install --confirm && pip install ipython && \
    pip install --requirement requirements.txt

SHELL ["/bin/bash", "--login", "-c"]

USER root
WORKDIR /root
# Install miniconda
ENV CONDA_DIR /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

RUN conda init bash && conda init fish && conda config --set auto_activate_base false

USER quser
WORKDIR /home/quser/qiskit_alt

# This is needed a second time
ENV CONDA_DIR /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Again, see if we can combine these
RUN printf "y\n" |  conda create -n qiskit_alt_env python=3.9
RUN conda init bash && conda init fish && conda config --set auto_activate_base false

RUN /opt/conda/bin/python -m venv ./venv_static && \
    source ./venv_static/bin/activate && pip install --upgrade pip ipython && \
    pip install --requirement requirements.txt

RUN conda activate qiskit_alt_env && pip install ipython && pip install --requirement requirements.txt

# Copy only files required for pip install
COPY --chown=quser requirements.txt setup.cfg  pyproject.toml README.md ./
COPY --chown=quser src ./src/

USER quser
RUN source ./venv1/bin/activate && pip install -e .
RUN source ./venv_static/bin/activate && pip install -e .
RUN conda activate qiskit_alt_env && pip install -e .

COPY --chown=quser init_test.py run_init_tests.sh ./


USER root
WORKDIR /root
