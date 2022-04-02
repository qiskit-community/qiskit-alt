#!/usr/bin/sh

source ./venv1/bin/activate && python init_test.py
conda activate qiskit_alt_env && python init_test.py
source ./venv_static/bin/activate && python init_test.py
