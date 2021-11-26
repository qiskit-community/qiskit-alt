import julia

from julia.api import LibJulia

import os
toplevel = os.path.dirname(os.path.dirname(__file__))

if os.path.exists(toplevel + "/qiskit_alt/julia_path.py"):
    from .julia_path import julia_path
else:
    julia_path = ""

local_install_path = toplevel + "/julia/bin/julia"
if os.path.exists(local_install_path) and not julia_path == "":
    julia_path = local_install_path

# TODO: support mac and win here
sys_image_path = toplevel + "/sys_image/sys_quantum.so"
if os.path.exists(sys_image_path):
    from julia import Julia
    jl = Julia(sysimage= sys_image_path)

# If the binary does not exist, the standard search path will be used
if os.path.exists(julia_path):
    api = LibJulia.load(julia=julia_path)
    api.init_julia()
elif not julia_path == "":
    print("Unable to find Julia executable ", julia_path, ".")
    print("Trying system search path.")

from julia import Main
from julia import Base

from julia import Pkg
Pkg.activate(toplevel) # Use package data in Project.toml

julia_manifest_path = toplevel + "/Manifest.toml"
is_instantiated = os.path.exists(julia_manifest_path) and Main.eval('any(x -> x.name == "QuantumOps" && x.is_direct_dep, values(Pkg.dependencies()))')

if not is_instantiated:
    print("Julia packages not found, installing...")
    Main.eval('Pkg.pkg"registry add git@github.com:jlapeyre/QuantumRegistry.git"')
    Pkg.resolve()
    Pkg.instantiate()

def compile_qiskit_alt():
    from julia import Pkg
    syspath = toplevel + "/sys_image"
    Main.eval('ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")')
    Pkg.activate(syspath)
    Main.cd(syspath)
    Main.eval('include("compile_quantum.jl")')
