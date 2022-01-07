from setuptools import setup, find_packages

version = {}
with open("./qiskit_alt/_version.py") as fp:
    exec(fp.read(), version)

setup(
    name='qiskit_alt',
    version=version['__version__'],
    description='Alternative to parts of qiskit, written in Julia',
    url= 'https://github.ibm.com:John-Lapeyre/qiskit_alt.git',
    author='John Lapeyre',
    packages=find_packages(),
    install_requires=[
        'pyscf>=2.0.1',
        'julia>=0.5.7',
        'qiskit-terra>=0.19.0',
        'qiskit-nature>=0.2.2',
        'julia_project @ git+https://github.com/jlapeyre/julia_project.git'
    ],
    include_package_data=True
)
