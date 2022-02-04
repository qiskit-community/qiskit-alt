import julia
import logging

from julia_project import JuliaProject

import os
qiskit_alt_path = os.path.dirname(os.path.abspath(__file__))
#qiskit_alt_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

julia_project = JuliaProject(
    name="qiskit_alt",
    package_path=qiskit_alt_path,
    preferred_julia_versions = ['1.7', '1.6', 'latest'],
    registry_url = "git@github.com:Qiskit-Extensions/QuantumRegistry.git",
    env_prefix = 'QISKIT_ALT_',
    logging_level = logging.INFO, # or logging.WARN,
    console_logging=False
)

julia_project.run()

logger = julia_project.logger

# Directory of Julia source files for qiskit_alt loaded via Python
julia_src_dir = julia_project.julia_src_dir

def compile_qiskit_alt():
    """
    Compile a system image for `qiskit_alt` in the subdirectory `./sys_image/`. This
    system image will be loaded the next time you import `qiskit_alt`.
    """
    julia_project.compile_julia_project()


def update_qiskit_alt():
    """
    Remove possible stale Manifest.toml files and compiled system image.
    Update Julia packages and rebuild Manifest.toml file.
    Before compiling, it's probably a good idea to call this method, then restart Python.
    """
    julia_project.update()
