import julia

import os
toplevel = os.path.dirname(os.path.dirname(__file__))

# The user may specify the path to the executable
if os.path.exists(os.path.join(toplevel, "qiskit_alt", "julia_path.py")):
    from .julia_path import julia_path
else:
    julia_path = ""

# The canonical place to look for a Julia installation is ./julia/bin/julia
local_install_path = os.path.join(toplevel, "julia", "bin", "julia")
if os.path.exists(local_install_path) and julia_path == "":
    julia_path = local_install_path

# If the binary does not exist, the standard search path will be used
from julia.api import LibJulia
if os.path.exists(julia_path):
    api = LibJulia.load(julia=julia_path)
else:
    api = LibJulia.load()

# TODO: support mac and win here
sys_image_path = os.path.join(toplevel, "sys_image", "sys_quantum.so")
if os.path.exists(sys_image_path):
    api.sysimage = sys_image_path

# Both the path and possibly the sysimage have been set. Now initialize Julia
api.init_julia()

# Import these to reexport
from julia import Main
from julia import Base

# Activate the Julia project

from julia import Pkg
Pkg.activate(toplevel) # Use package data in Project.toml

### Instantiate Julia project, i.e. download packages, etc.

julia_manifest_path = os.path.join(toplevel, "Manifest.toml")
is_instantiated = os.path.exists(julia_manifest_path) and Main.eval('any(x -> x.name == "QuantumOps" && x.is_direct_dep, values(Pkg.dependencies()))')

if not is_instantiated:
    print("Julia packages not installed, installing...")
    Main.eval('Pkg.pkg"registry add git@github.ibm.com:IBM-Q-Software/QuantumRegistry.git"')
    Pkg.resolve()
    Pkg.instantiate()

def compile_qiskit_alt():
    from julia import Pkg
    syspath = os.path.join(toplevel, "sys_image")
    Main.eval('ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")')
    Pkg.activate(syspath)
    Main.cd(syspath)
    Pkg.resolve()
    Pkg.instantiate()
    Main.eval('include("compile_quantum.jl")')
