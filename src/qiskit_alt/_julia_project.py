import logging
import os
from julia_project import JuliaProject

qiskit_alt_path = os.path.dirname(os.path.abspath(__file__))

# def _after_init_func():
#     importlib.import_module('.hellomod', 'qiskit_alt')

def new_project(calljulia="pyjulia"):
    """Return a new `JuliaProject`.

    Use this if you want to use both `pyjulia` (`julia` module) and `juliacall`
    in a single session. For example, if are already using `pyjulia`, you can
    do `new_proj = new_project(calljulia="juliacall")` and then
    `new_proj.ensure_init()`.
    """
    return JuliaProject(
        name="qiskit_alt",
        package_path = qiskit_alt_path,
        version_spec = "^1.6", # Must be at least 1.6
        env_prefix = 'MYJULIAMOD_', # env variables prefixed with this may control JuliaProject
        registries = {"QuantumRegistry" : "https://github.com/Qiskit-Extensions/QuantumRegistry"},
        logging_level = logging.INFO, # or logging.WARN,
        console_logging=False,
        calljulia = calljulia
        )


project = new_project()
