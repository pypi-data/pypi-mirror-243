# struqture-qutip-interface

An interface that can transform struqture spin objects to qutip objects for simulation purposes.

This project is in the alpha stage, documentation is minimal at the moment and breaking changes may occur.

## Example

```Python
from struqture_qutip_interface import SpinQutipInterface, SpinOpenSystemQutipInterface
import qutip as qt
from struqture_py.spins import (
    SpinLindbladOpenSystem,
    SpinLindbladNoiseSystem,
    SpinHamiltonianSystem,
    PauliProduct,
    DecoherenceProduct
)

number_spins = 2
# Creating a Spin Hamiltonian in struqture
hamiltonian = SpinHamiltonianSystem(number_spins)
for i in range(number_spins):
    hamiltonian.set(PauliProduct().z(i), 1.0)

for i in range(number_spins-1):
    hamiltonian.set(PauliProduct().x(i).x(i+1), 0.5)

# Creating noise terms in struqture
noise = SpinLindbladNoiseSystem(number_spins)

for i in range(number_spins):
    noise.set((DecoherenceProduct().z(i), DecoherenceProduct().z(i)), 0.001)

# Combining noise terms and Hamiltonian to an open system
noisy_system = SpinLindbladOpenSystem.group(hamiltonian, noise)

# Transforming the open system to a qutip superoperator
(coherent_part, noisy_part) = SpinOpenSystemQutipInterface.open_system_to_qutip(noisy_system)
liouFull = coherent_part  + noisy_part

# Setting up separate operators that can be measured
qi = SpinQutipInterface()
op_Z0 = PauliProduct().set_pauli(0, "Z")
op_Z1 = PauliProduct().set_pauli(1, "Z")
op_Z0Z1 = PauliProduct().set_pauli(0, "Z").set_pauli(1, "Z")

endianess = 'little' #'big'
qt_Z0 = qi.pauli_product_to_qutip(op_Z0, number_spins, endianess=endianess)
qt_Z1 = qi.pauli_product_to_qutip(op_Z1, number_spins, endianess=endianess)
qt_Z0Z1 = qi.pauli_product_to_qutip(op_Z0Z1, number_spins, endianess=endianess)

# Setting up an initial density matrix
init_spin = []
for i in range(number_spins):
    init_spin.append(qt.basis(2, 1)) # initially all spins excited
init_spin_tensor = qt.tensor(list(reversed(init_spin)))
psi0 = init_spin_tensor * init_spin_tensor.dag()

# master-equation solver
time_axis = np.linspace(0, 10, 100)
result = qt.mesolve(liouFull,
                    psi0,
                    time_axis,
                    [], # c_op_list is left empty, since noise is already in liouFull
                    [qt_Z0, qt_Z1, qt_Z0Z1] # operators to be measured
                    ).expect
time_evolution_Z0 = np.real(result[0])
time_evolution_Z1 = np.real(result[1])
time_evolution_Z0Z1 = np.real(result[2])
```
