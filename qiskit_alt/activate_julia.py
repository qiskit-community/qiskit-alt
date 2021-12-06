import logging
import julia

logging_level = logging.INFO
# Choose the following to quiet logging
# logging_level = logging.WARNING

logger = logging.getLogger('qiskit_alt')
logger.setLevel(logging_level)
fh = logging.FileHandler('qiskit_alt.log')
fh.setLevel(logging_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Uncomment this to log to the console
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# ch.setFormatter(formatter)
# logger.addHandler(ch)

import os
toplevel = os.path.dirname(os.path.dirname(__file__))

logger.info("importing qiskit_alt.")

# The user may specify the path to the executable
if os.path.exists(os.path.join(toplevel, "qiskit_alt", "julia_path.py")):
    from .julia_path import julia_path
    logger.info('julia_path.py exists')
    if julia_path == "":
        logger.info('julia_path.julia_path=="".')
    else:
        logger.info('Non-empty julia_path.julia_path=="%s".', julia_path)
else:
    julia_path = ""
    logger.info('julia_path.py does not exist')

# The canonical place to look for a Julia installation is ./julia/bin/julia
local_install_path = os.path.join(toplevel, "julia", "bin", "julia")
if os.path.exists(local_install_path) and julia_path == "":
    julia_path = local_install_path
    logger.info("Using existing executable '%s'.", julia_path)
else:
    logger.info("No installation found at '%s'.", local_install_path)

# If the binary does not exist, the standard search path will be used
from julia.api import LibJulia
if os.path.exists(julia_path):
    api = LibJulia.load(julia=julia_path)
else:
    logger.info("Looking for julia in user's path")
    api = LibJulia.load()

# TODO: support mac and win here
sys_image_path = os.path.join(toplevel, "sys_image", "sys_quantum.so")

sys_image_path_exists = os.path.exists(sys_image_path)

if sys_image_path_exists:
    api.sysimage = sys_image_path
    logger.info("Loading system image %s", sys_image_path)
else:
    logger.info("No custom system image found.")

# Both the path and possibly the sysimage have been set. Now initialize Julia.
logger.info("Initializing julia")
api.init_julia()

# Import these to reexport
from julia import Main
from julia import Base
logger.info("Julia version %s", Main.string(Main.VERSION))

Main.eval("using Revise")

loaded_sys_image_path = Main.eval('unsafe_string(Base.JLOptions().image_file)')
logger.info("Probed system image path %s", loaded_sys_image_path)

# Activate the Julia project

# Maybe useful
# julia_cmd = Base.julia_cmd()

from julia import Pkg
Pkg.activate(toplevel) # Use package data in Project.toml

### Instantiate Julia project, i.e. download packages, etc.

julia_manifest_path = os.path.join(toplevel, "Manifest.toml")

# Assume that if sys_quantum.so exists, then Julia packages are installed.
if sys_image_path_exists or os.path.exists(julia_manifest_path):
    logger.info("Julia quantum packages found.")
else:
    print("Julia packages not installed, installing...")
    logger.info("Julia packages not installed or found.")
    logger.info("Installing registry from github.ibm.com:IBM-Q-Software/QuantumRegistry.git")
    Pkg.Registry
    Pkg.Registry.add(Pkg.RegistrySpec(url = "git@github.ibm.com:IBM-Q-Software/QuantumRegistry.git"))
    logger.info("Installing Julia packages")
    Pkg.resolve()
    Pkg.instantiate()

from os.path import dirname
toplevel = dirname(dirname(__file__))
julia_src_dir = os.path.join(toplevel, "julia_src")

def compile_qiskit_alt():
    """
    Compile a Julia system image with all requirements for qiskit_alt.
    """
    from julia import Pkg
    syspath = os.path.join(toplevel, "sys_image")
    Main.eval('ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")')
    Pkg.activate(syspath)
    Main.cd(syspath)
    Pkg.resolve()
    Pkg.instantiate()
    Main.include("compile_quantum.jl")
