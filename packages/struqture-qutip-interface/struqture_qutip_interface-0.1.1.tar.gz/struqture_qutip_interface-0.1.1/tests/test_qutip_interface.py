# Copyright © 2021-2023 HQS Quantum Simulations GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing permissions and
# limitations under the License.

"""Test SpinHamiltonianSystem and SpinSystem"""
from struqture_py.spins import (
    SpinHamiltonianSystem,
    PauliProduct,
    SpinLindbladOpenSystem,
    SpinLindbladNoiseSystem,
)
from struqture_qutip_interface import SpinQutipInterface, SpinOpenSystemQutipInterface
from qoqo_calculator_pyo3 import CalculatorComplex
import qutip as qt
import numpy as np
import pytest
import sys


testdata = [
    (action, qt_matrix)
    for action, qt_matrix in zip(
        ["I", "X", "Y", "Z"], [qt.qeye(2), qt.sigmax(), qt.sigmay(), qt.sigmaz()]
    )
]


@pytest.mark.parametrize("action, qt_matrix", testdata)
def test_pauli_product_to_qutip_1spin(action, qt_matrix):
    qi = SpinQutipInterface()
    op = PauliProduct().set_pauli(0, action)
    assert qi.pauli_product_to_qutip(op, 1) == qt_matrix


testdata = [
    (action, qt_matrix)
    for action, qt_matrix in zip(
        ["I", "X", "Y", "Z"], [qt.qeye(2), qt.sigmax(), qt.sigmay(), qt.sigmaz()]
    )
]


@pytest.mark.parametrize("action,qt_matrix", testdata)
@pytest.mark.parametrize("endianess", ["little", "big"])
def test_pauli_product_to_qutip_2spin(action, qt_matrix, endianess):
    qi = SpinQutipInterface()
    op = PauliProduct().set_pauli(0, action)
    if endianess == "little":
        exact = np.kron([[1, 0], [0, 1]], qt_matrix.data.toarray())
    else:
        exact = np.kron(qt_matrix.data.toarray(), [[1, 0], [0, 1]])
    assert qi.pauli_product_to_qutip(op, 2, endianess=endianess) == qt.Qobj(
        exact, dims=[[2, 2], [2, 2]]
    )


testdata = [
    (action, qt_matrix)
    for action, qt_matrix in zip(
        ["I", "X", "Y", "Z"], [qt.qeye(2), qt.sigmax(), qt.sigmay(), qt.sigmaz()]
    )
]


@pytest.mark.parametrize("action,qt_matrix", testdata)
@pytest.mark.parametrize("endianess", ["little", "big"])
def test_pauli_product_to_qutip_2actions(action, qt_matrix, endianess):
    qi = SpinQutipInterface()
    op = PauliProduct().set_pauli(0, action).set_pauli(1, action)
    exact = np.kron(qt_matrix.data.toarray(), qt_matrix.data.toarray())
    assert qi.pauli_product_to_qutip(op, 2, endianess=endianess) == qt.Qobj(
        exact, dims=[[2, 2], [2, 2]]
    )


def test_qobj():
    qi = SpinQutipInterface()
    to_matrix = {0: qt.qeye(2), 1: qt.sigmax(), 2: qt.sigmay(), 3: qt.sigmaz()}
    exact = np.sum(
        [
            (i + 1) * np.kron(to_matrix[i].data.toarray(), to_matrix[i].data.toarray())
            for i in [0, 1, 2, 3]
        ],
        0,
    )
    sps = SpinHamiltonianSystem(2)
    for i, action in enumerate(["I", "X", "Y", "Z"]):
        pp = PauliProduct().set_pauli(0, action).set_pauli(1, action)
        sps.set(repr(pp), CalculatorComplex(i + 1))
    assert qi.qobj(sps) == qt.Qobj(exact, dims=[[2, 2], [2, 2]])


@pytest.mark.parametrize("endianess", ["little", "big"])
def test_qobj_endianess(endianess):
    qi = SpinQutipInterface()
    to_matrix = {0: qt.qeye(2), 1: qt.sigmax(), 2: qt.sigmay(), 3: qt.sigmaz()}
    if endianess == "little":
        exact = np.sum(
            [(i + 1) * np.kron(np.eye(2), to_matrix[i].data.toarray()) for i in [0, 1, 2, 3]],
            0,
        )
    else:
        exact = np.sum(
            [(i + 1) * np.kron(to_matrix[i].data.toarray(), np.eye(2)) for i in [0, 1, 2, 3]],
            0,
        )
    sps = SpinHamiltonianSystem(2)
    for i, action in enumerate(["I", "X", "Y", "Z"]):
        pp = PauliProduct().set_pauli(0, action)
        sps.set(repr(pp), CalculatorComplex(i + 1))
    assert qi.qobj(sps, endianess=endianess) == qt.Qobj(exact, dims=[[2, 2], [2, 2]])


@pytest.mark.parametrize("endianess", ["little", "big"])
def test_open_system_interface_open_system(endianess):
    qi = SpinOpenSystemQutipInterface()

    hamiltonian = SpinHamiltonianSystem()
    hamiltonian.add_operator_product("0X", CalculatorComplex(2))
    hamiltonian.add_operator_product("0Z", CalculatorComplex(4))
    noise = SpinLindbladNoiseSystem()
    noise.set(("0Z", "1iY"), 3.0)
    open_system = SpinLindbladOpenSystem.group(hamiltonian, noise)
    qt_system_2 = qi.open_system_to_qutip(open_system=open_system, endianess=endianess)

    hamiltonian = SpinHamiltonianSystem()
    hamiltonian.add_operator_product("0X", CalculatorComplex(2))
    hamiltonian.add_operator_product("0Z", CalculatorComplex(4))
    noise = SpinLindbladNoiseSystem()
    open_system = SpinLindbladOpenSystem.group(hamiltonian, noise)
    qt_system_3 = qi.open_system_to_qutip(open_system=open_system, endianess=endianess)
    hamiltonian = SpinHamiltonianSystem()
    noise = SpinLindbladNoiseSystem()
    noise.set(("0Z", "1iY"), 3.0)
    open_system = SpinLindbladOpenSystem.group(hamiltonian, noise)
    qt_system_4 = qi.open_system_to_qutip(open_system=open_system, endianess=endianess)

    open_system = SpinLindbladOpenSystem()
    qt_system_5 = qi.open_system_to_qutip(open_system=open_system, endianess=endianess)

    if endianess == "little":
        qt_coherent_pre = 2 * qt.tensor(qt.qeye(2), qt.sigmax()) + 4 * qt.tensor(
            qt.qeye(2), qt.sigmaz()
        )
        (An, Am) = (
            qt.tensor(qt.qeye(2), qt.sigmaz()),
            qt.tensor(qt.sigmay() * 1j, qt.qeye(2)),
        )
    if endianess == "big":
        qt_coherent_pre = 2 * qt.tensor(qt.sigmax(), qt.qeye(2)) + 4 * qt.tensor(
            qt.sigmaz(), qt.qeye(2)
        )
        (An, Am) = (
            qt.tensor(qt.sigmaz(), qt.qeye(2)),
            qt.tensor(qt.qeye(2), qt.sigmay() * 1j),
        )

    qt_coherent = -1j * (qt.spre(qt_coherent_pre) - qt.spost(qt_coherent_pre))
    qt_noisy = complex(3) * (
        qt.sprepost(An, Am.dag()) - 0.5 * qt.spre(Am.dag() * An) - 0.5 * qt.spost(Am.dag() * An)
    )

    assert qt_system_3[1] == 0
    assert qt_system_4[0] == 0
    assert qt_system_5 == (0, 0)
    assert qt_system_2[0] == qt_coherent
    assert qt_system_2[1] == qt_noisy


@pytest.mark.parametrize("endianess", ["little", "big"])
def test_open_system_interface_noise_operator(endianess):
    qi = SpinOpenSystemQutipInterface()

    open_system = SpinLindbladNoiseSystem()
    open_system.set(("0Z", "1iY"), 3.0)
    qt_system_4 = qi.open_system_to_qutip(open_system=open_system, endianess=endianess)

    open_system = SpinLindbladNoiseSystem()
    qt_system_5 = qi.open_system_to_qutip(open_system=open_system, endianess=endianess)

    if endianess == "little":
        (An, Am) = (
            qt.tensor(qt.qeye(2), qt.sigmaz()),
            qt.tensor(qt.sigmay() * 1j, qt.qeye(2)),
        )
    if endianess == "big":
        (An, Am) = (
            qt.tensor(qt.sigmaz(), qt.qeye(2)),
            qt.tensor(qt.qeye(2), qt.sigmay() * 1j),
        )

    qt_noisy = complex(3) * (
        qt.sprepost(An, Am.dag()) - 0.5 * qt.spre(Am.dag() * An) - 0.5 * qt.spost(Am.dag() * An)
    )

    assert qt_system_5 == (0, 0)
    assert qt_system_4[0] == 0
    assert qt_system_4[1] == qt_noisy


if __name__ == "__main__":
    pytest.main(sys.argv)
