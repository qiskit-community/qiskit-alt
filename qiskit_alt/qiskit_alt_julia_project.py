import julia

from .julia_project import JuliaProject

# The JuliaProject class is generic and should be moved at some point to a
# separate python package
julia_project = JuliaProject(
    name="qiskit_alt",
    registry_url = "git@github.ibm.com:IBM-Q-Software/QuantumRegistry.git"
)

logger = julia_project.logger
julia_src_dir = julia_project.julia_src_dir

def compile_qiskit_alt():
    julia_project.compile_julia_project()
