import subprocess

def python_commands(commands):
    try:
        result = subprocess.run(
            ['python', '-c', commands], check=True, capture_output=True, encoding='utf8'
        )
    except subprocess.CalledProcessError as err:
        return err
    return result


def basic_inits():
    all_coms = []
    for _compile in ("False", "True"):
        for calljulia in ("pyjulia", "juliacall"):
            for depot in ("False", "True"):
                args = f"compile={_compile}, calljulia='{calljulia}', depot={depot}"
                coms = f"import qiskit_alt; qiskit_alt.project.ensure_init({args})"
                all_coms.append(coms)
                if calljulia == "pyjulia":
                    other_calljulia = "juliacall"
                else:
                    other_calljulia = "pyjulia"
                args = f"compile={_compile}, calljulia='{other_calljulia}', depot={depot}"
                coms = f"import qiskit_alt; qiskit_alt.project.ensure_init({args}); qiskit_alt.project.clean_all()"
                all_coms.append(coms)
    return all_coms

# def basic_inits():
#     all_coms = ["import sys", "import os", "import sdsdff", "import sdsdff", "import shutil"]
#     return all_coms


def run_tests(all_commands=None, verbose=False):
    num_passed = 0
    if all_commands is None:
        all_commands = basic_inits()
    for commands in all_commands:
        print(f"running '{commands}'")
        result = python_commands(commands)
        if isinstance(result, subprocess.CalledProcessError):
            print(f"**** Commands '{commands}' failed with error code {result}")
            print(result.stderr)
        else:
            num_passed += 1
            if verbose:
                print(result)
    msg = f"{num_passed} of {len(all_commands)} installation tests passed"
    if num_passed < len(all_commands):
        print("**** " + msg)
    else:
        print(msg)


if __name__ == '__main__':
    run_tests()
