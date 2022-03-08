import pytest
import qiskit_alt
project = qiskit_alt.project
project.ensure_init(calljulia="juliacall")


def test_always_passes():
    assert True


def test_interface_lib():
    assert qiskit_alt.project.julia.__name__ == 'juliacall'


def test_Main():
    Main = qiskit_alt.project.julia.Main
    assert Main.sind(90) == 1.0
