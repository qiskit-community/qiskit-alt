import julia
import logging

from .julia_project import JuliaProject

# The JuliaProject class is generic and should be moved at some point to a
# separate python package.
julia_project = JuliaProject(
    name="qiskit_alt",
    registry_url = "git@github.ibm.com:John-Lapeyre/QuantumRegistry.git",
    logging_level = logging.INFO # or logging.WARN
)

logger = julia_project.logger

# Directory of Julia source files for qiskit_alt loaded via Python
julia_src_dir = julia_project.julia_src_dir

def compile_qiskit_alt():
    julia_project.compile_julia_project()
