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

julia_directory_in_toplevel = os.path.join(toplevel, "julia")
julia_executable_under_toplevel = os.path.join(julia_directory_in_toplevel, "bin", "julia")
if os.path.exists(julia_executable_under_toplevel) and julia_path == "":
    julia_path = julia_executable_under_toplevel
    logger.info("Using executable from julia installation in qiskit_alt toplevel '%s'.", julia_path)
elif os.path.exists(julia_directory_in_toplevel):
    if os.path.isdir(julia_directory_in_toplevel):
        msg = "WARNING: directory ./julia/ found under toplevel, but ./julia/bin/julia not found."
        logger.info(msg)
        print(msg)
    else:
        msg = "WARNING: ./julia found under toplevel, but it is not a directory as expected."
        logger.info(msg)
        print(msg)
else:
    logger.info("No julia installation found at '%s'.", julia_directory_in_toplevel)

# If the binary does not exist, the standard search path will be used
from julia.api import LibJulia
if os.path.exists(julia_path):
    api = LibJulia.load(julia=julia_path)
else:
    logger.info("Searching for julia in user's path")
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

# This does not work here. Has to be called with a magic
# Main.eval("using Revise")

loaded_sys_image_path = Main.eval('unsafe_string(Base.JLOptions().image_file)')
logger.info("Probed system image path %s", loaded_sys_image_path)

# Activate the Julia project

# Maybe useful
julia_cmd = Base.julia_cmd()
logger.info("Probed julia command: %s", julia_cmd)

from julia import Pkg
Pkg.activate(toplevel) # Use package data in Project.toml
logger.info("Probed Project.toml path: %s", Pkg.project().path)

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
    if loaded_sys_image_path == sys_image_path:
        msg = "WARNING: Compiling system image while compiled system image is loaded.\n" \
            + f"Consider deleting  {sys_image_path} and restarting python."
        print(msg)
        logger.info(msg)
    from julia import Pkg
    syspath = os.path.join(toplevel, "sys_image")
    Main.eval('ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")')
    Pkg.activate(syspath)
    logger.info("Compiling: probed Project.toml path: %s", Pkg.project().path)
    Main.cd(syspath)
    try:
        Pkg.resolve()
    except:
        msg = "Pkg.resolve() failed. Updating packages."
        print(msg)
        logger.info(msg)
        Pkg.update()
        Pkg.resolve()
    Pkg.instantiate()
    Main.include("compile_quantum.jl")
