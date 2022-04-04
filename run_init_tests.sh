#!/usr/bin/sh

# Must deactivate to avoid complaint about mixed virtual environments
echo "source ./venv1/bin/activate && python init_test.py"
source ./venv1/bin/activate && python init_test.py
echo
deactivate

echo "source ./venv1/bin/activate && python init_test.py"
source ./venv_static/bin/activate && python init_test.py
echo
deactivate

# Work around poor design
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
echo "conda activate qiskit_alt_env && python init_test.py"
conda activate qiskit_alt_env && python init_test.py
