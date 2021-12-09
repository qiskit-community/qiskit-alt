import julia
import logging

from julia_project import JuliaProject

import os
qiskit_alt_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

julia_project = JuliaProject(
    name="qiskit_alt",
    package_path=qiskit_alt_path,
    registry_url = "git@github.ibm.com:John-Lapeyre/QuantumRegistry.git",
    logging_level = logging.INFO, # or logging.WARN,
    console_logging=False
)

julia_project.run()

logger = julia_project.logger

# Directory of Julia source files for qiskit_alt loaded via Python
julia_src_dir = julia_project.julia_src_dir

def compile_qiskit_alt():
    julia_project.compile_julia_project()
