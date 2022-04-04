#!/usr/bin/sh

source ./venv1/bin/activate && python init_test.py
source ./venv_static/bin/activate && python init_test.py

# Work around poor design
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate qiskit_alt_env && python init_test.py
