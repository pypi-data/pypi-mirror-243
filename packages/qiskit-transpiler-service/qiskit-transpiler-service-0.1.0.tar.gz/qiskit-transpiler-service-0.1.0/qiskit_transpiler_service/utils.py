import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import LinearFunction
from qiskit.quantum_info import Clifford
from qiskit.synthesis.linear.linear_matrix_utils import random_invertible_binary_matrix


def get_metrics(qc: QuantumCircuit):
    """Returns a dict with metrics from a QuantumCircuit"""
    qcd = qc.decompose(reps=3)
    return {
        "n_gates": qcd.size(),
        "n_layers": qcd.depth(),
        "n_cnots": qcd.num_nonlocal_gates(),
        "n_layers_cnots": qcd.depth(lambda x: x[0].name == "cx"),
    }


def random_permutation(n_qubits):
    """Generate a random permutation of n_qubits qubits."""
    return np.random.permutation(n_qubits)


def create_random_linear_function(n_qubits: int, seed: int = 123):
    rand_lin = lambda seed: LinearFunction(
        random_invertible_binary_matrix(n_qubits, seed=seed)
    )

    return LinearFunction(rand_lin(seed))


def random_clifford_from_linear_function(n_qubits: int, seed: int = 123):
    """Generate a random clifford from a random linear function of n_qubits qubits."""

    random_linear = lambda seed: LinearFunction(
        random_invertible_binary_matrix(n_qubits, seed=seed)
    )
    random_clifford = Clifford(random_linear(seed))
    return random_clifford
