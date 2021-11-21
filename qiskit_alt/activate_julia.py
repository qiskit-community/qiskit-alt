import julia

from julia.api import LibJulia
# julia_path = "/home/lapeyre/.local/julias/julia-1.5/bin/julia"
# julia_path = "/home/lapeyre/.local/julias/julia-1.6/bin/julia"
# julia_path = "/home/lapeyre/.local/julias/julia-1.8.0-DEV.979/bin/julia"
julia_path = "/home/lapeyre/.local/julias/julia-1.7.0-beta4/bin/julia"

api = LibJulia.load(julia=julia_path)
api.init_julia()

from julia import Main
from julia import Base

from julia import Pkg
Pkg.activate(".") # Use package data in Project.toml
