import julia

from julia.api import LibJulia
julia_path = ""
# julia_path = "/home/lapeyre/.local/julias/julia-1.6/bin/julia"
# julia_path = "/home/lapeyre/.local/julias/julia-1.8.0-DEV.979/bin/julia"
julia_path = "/home/lapeyre/.local/julias/julia-1.7.0-beta4/bin/julia"

import os
toplevel = os.path.dirname(os.path.dirname(__file__))

# TODO: support mac and win here
sys_image_path = toplevel + "/sys_quantum.so"
if os.path.exists(sys_image_path):
    from julia import Julia
    jl = Julia(sysimage= sys_image_path)

# If the binary does not exist, the standard search path will be used
if os.path.exists(julia_path):
    api = LibJulia.load(julia=julia_path)
    api.init_julia()

from julia import Main
from julia import Base

from julia import Pkg
Pkg.activate(toplevel) # Use package data in Project.toml
