from typing import List, Literal

from classiq.qmod.qmod_parameter import QParam
from classiq.qmod.qmod_struct import QStruct
from classiq.qmod.qmod_variable import Input, Output, QArray, QBit
from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.quantum_function import ExternalQFunc


@QStruct
class PauliTerm:
    pauli: List[int]
    coefficient: float


@QStruct
class MoleculeProblem:
    mapping: int
    z2_symmetries: bool
    molecule: "Molecule"
    freeze_core: bool
    remove_orbitals: List[int]


@QStruct
class Molecule:
    atoms: List["ChemistryAtom"]
    spin: int
    charge: int


@QStruct
class ChemistryAtom:
    element: int
    position: "Position"


@QStruct
class Position:
    x: float
    y: float
    z: float


@QStruct
class FockHamiltonianProblem:
    mapping: int
    z2_symmetries: bool
    terms: List["LadderTerm"]
    num_particles: List[int]


@QStruct
class LadderTerm:
    coefficient: float
    ops: List["LadderOp"]


@QStruct
class LadderOp:
    op: int
    index: int


@QStruct
class CombinatorialOptimizationSolution:
    probability: float
    cost: float
    solution: List[int]
    count: int


@QStruct
class GaussianModel:
    num_qubits: int
    normal_max_value: float
    default_probabilities: List[float]
    rhos: List[float]
    loss: List[int]
    min_loss: int


@QStruct
class LogNormalModel:
    num_qubits: int
    mu: float
    sigma: float


@QStruct
class FinanceFunction:
    f: int
    threshold: float
    larger: bool
    polynomial_degree: int
    use_chebyshev_polynomial_approximation: bool
    tail_probability: float


@QStruct
class QsvmResult:
    test_score: float
    predicted_labels: List[float]


@QStruct
class QSVMFeatureMapPauli:
    feature_dimension: int
    reps: int
    entanglement: int
    alpha: float
    paulis: List[List[int]]


@ExternalQFunc
def qaoa_mixer_layer(
    num_qubits: QParam[int],
    b: QParam[float],
    target: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def qaoa_cost_layer(
    num_qubits: QParam[int],
    g: QParam[float],
    hamiltonian: QParam[List["PauliTerm"]],
    is_st: QParam[bool],
    target: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def qaoa_layer(
    num_qubits: QParam[int],
    g: QParam[float],
    b: QParam[float],
    hamiltonian: QParam[List["PauliTerm"]],
    is_st: QParam[bool],
    target: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def qaoa_init(
    num_qubits: QParam[int],
    target: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def qaoa_penalty(
    num_qubits: QParam[int],
    params_list: QParam[List[float]],
    hamiltonian: QParam[List["PauliTerm"]],
    is_st: QParam[bool],
    target: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def full_hea(
    num_qubits: QParam[int],
    is_parametrized: QParam[List[int]],
    angle_params: QParam[List[float]],
    connectivity_map: QParam[List[List[int]]],
    reps: QParam[int],
    operands_1qubit: QCallable[QParam[float], QBit],
    operands_2qubit: QCallable[QParam[float], QBit, QBit],
    x: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def H(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def X(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def Y(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def Z(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def I(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def S(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def T(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def SDG(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def TDG(
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def PHASE(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def RX(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def RY(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def RZ(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def RXX(
    theta: QParam[float],
    target: QArray[QBit, Literal[2]],
) -> None:
    pass


@ExternalQFunc
def RYY(
    theta: QParam[float],
    target: QArray[QBit, Literal[2]],
) -> None:
    pass


@ExternalQFunc
def RZZ(
    theta: QParam[float],
    target: QArray[QBit, Literal[2]],
) -> None:
    pass


@ExternalQFunc
def CH(
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def CX(
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def CY(
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def CZ(
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def CRX(
    theta: QParam[float],
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def CRY(
    theta: QParam[float],
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def CRZ(
    theta: QParam[float],
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def CPHASE(
    theta: QParam[float],
    target: QBit,
    control: QBit,
) -> None:
    pass


@ExternalQFunc
def SWAP(
    qbit0: QBit,
    qbit1: QBit,
) -> None:
    pass


@ExternalQFunc
def IDENTITY(
    target: QArray[QBit],
) -> None:
    pass


@ExternalQFunc
def prepare_state(
    probabilities: QParam[List[float]],
    bound: QParam[float],
    out: Output[QArray[QBit, Literal["log(len(probabilities), 2)"]]],
) -> None:
    pass


@ExternalQFunc
def prepare_amplitudes(
    amplitudes: QParam[List[float]],
    bound: QParam[float],
    out: Output[QArray[QBit, Literal["log(len(amplitudes), 2)"]]],
) -> None:
    pass


@ExternalQFunc
def unitary(
    elements: QParam[List[List[float]]],
    target: QArray[QBit, Literal["log(len(elements[0]), 2)"]],
) -> None:
    pass


@ExternalQFunc
def add(
    left: Input[QArray[QBit]],
    right: Input[QArray[QBit]],
    result: Output[QArray[QBit, Literal["Max(len(left), len(right)) + 1"]]],
) -> None:
    pass


@ExternalQFunc
def U(
    theta: QParam[float],
    phi: QParam[float],
    lam: QParam[float],
    gam: QParam[float],
    target: QBit,
) -> None:
    pass


@ExternalQFunc
def CCX(
    target: QBit,
    control: QArray[QBit, Literal[2]],
) -> None:
    pass


@ExternalQFunc
def allocate(
    num_qubits: QParam[int],
    out: Output[QArray[QBit, Literal["num_qubits"]]],
) -> None:
    pass


@ExternalQFunc
def free(
    in_: Input[QArray[QBit]],
) -> None:
    pass


@ExternalQFunc
def single_pauli_exponent(
    pauli_string: QParam[List[int]],
    coefficient: QParam[float],
    qbv: QArray[QBit, Literal["len(pauli_string)"]],
) -> None:
    pass


@ExternalQFunc
def suzuki_trotter(
    pauli_operator: QParam[List["PauliTerm"]],
    evolution_coefficient: QParam[float],
    order: QParam[int],
    repetitions: QParam[int],
    qbv: QArray[QBit, Literal["len(get_field(pauli_operator[0], 'pauli'))"]],
) -> None:
    pass


@ExternalQFunc
def qdrift(
    pauli_operator: QParam[List["PauliTerm"]],
    evolution_coefficient: QParam[float],
    num_qdrift: QParam[int],
    qbv: QArray[QBit, Literal["len(get_field(pauli_operator[0], 'pauli'))"]],
) -> None:
    pass


@ExternalQFunc
def exponentiation_with_depth_constraint(
    pauli_operator: QParam[List["PauliTerm"]],
    evolution_coefficient: QParam[float],
    max_depth: QParam[int],
    qbv: QArray[QBit, Literal["len(get_field(pauli_operator[0], 'pauli'))"]],
) -> None:
    pass


@ExternalQFunc
def qft_step(
    num_qbits: QParam[int],
    qbv: QArray[QBit, Literal["num_qbits"]],
) -> None:
    pass


@ExternalQFunc
def qft(
    num_qbits: QParam[int],
    qbv: QArray[QBit, Literal["num_qbits"]],
) -> None:
    pass


@ExternalQFunc
def qpe(
    reg_size: QParam[int],
    qpe_reg_size: QParam[int],
    qfunc: QCallable[QArray[QBit, Literal["reg_size"]]],
    x: QArray[QBit, Literal["reg_size"]],
    q: QArray[QBit, Literal["qpe_reg_size"]],
) -> None:
    pass


@ExternalQFunc
def single_pauli(
    reg_size: QParam[int],
    slope: QParam[float],
    offset: QParam[float],
    q1_qfunc: QCallable[QParam[float], QBit],
    x: QArray[QBit, Literal["reg_size"]],
    q: QBit,
) -> None:
    pass


@ExternalQFunc
def linear_pauli_rotations(
    reg_size: QParam[int],
    num_state_qubits: QParam[int],
    bases: QParam[List[int]],
    slopes: QParam[List[float]],
    offsets: QParam[List[float]],
    x: QArray[QBit, Literal["reg_size"]],
    q: QArray[QBit, Literal["num_state_qubits"]],
) -> None:
    pass


@ExternalQFunc
def amplitude_estimation(
    num_phase_qubits: QParam[int],
    num_unitary_qubits: QParam[int],
    sp_op: QCallable[QParam[int], QArray[QBit, Literal["num_unitary_qubits"]]],
    oracle_op: QCallable[QParam[int], QArray[QBit, Literal["num_unitary_qubits"]]],
    phase_port: Output[QArray[QBit, Literal["num_phase_qubits"]]],
    unitary_port: Output[QArray[QBit, Literal["num_unitary_qubits"]]],
) -> None:
    pass


@ExternalQFunc
def simple_oracle(
    predicate: QCallable[QArray[QBit, Literal["len(target)"]], QBit],
    target: QArray[QBit],
) -> None:
    pass


@ExternalQFunc
def grover_diffuser(
    num_qubits: QParam[int],
    p: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def grover_operator(
    num_qubits: QParam[int],
    sp_op: QCallable[QParam[int], QArray[QBit, Literal["num_qubits"]]],
    oracle_op: QCallable[QParam[int], QArray[QBit, Literal["num_qubits"]]],
    p: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def uniform_superposition(
    num_qubits: QParam[int],
    q: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def apply_to_all(
    num_qubits: QParam[int],
    gate_operand: QCallable[QBit],
    q: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def grover_search(
    num_qubits: QParam[int],
    reps: QParam[int],
    oracle_op: QCallable[QParam[int], QArray[QBit, Literal["num_qubits"]]],
    gsq: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def prepare_int(
    val: QParam[int],
    out: Output[QArray[QBit]],
) -> None:
    pass


@ExternalQFunc
def repeat(
    count: QParam[int],
    iteration: QCallable[QParam[int]],
) -> None:
    pass


@ExternalQFunc
def invert(
    operand: QCallable[QArray[QBit, Literal["len(target)"]]],
    target: QArray[QBit],
) -> None:
    pass


@ExternalQFunc
def control(
    operand: QCallable[QArray[QBit, Literal["len(target)"]]],
    ctrl: QArray[QBit],
    target: QArray[QBit],
) -> None:
    pass


@ExternalQFunc
def if_(
    condition: QParam[bool],
    then: QCallable,
    else_: QCallable,
) -> None:
    pass


@ExternalQFunc
def switch(
    selector: QParam[int],
    cases: QCallable,
) -> None:
    pass


@ExternalQFunc
def join(
    in1: Input[QArray[QBit]],
    in2: Input[QArray[QBit]],
    out: Output[QArray[QBit, Literal["len(in1)+len(in2)"]]],
) -> None:
    pass


@ExternalQFunc
def split(
    out1_size: QParam[int],
    out2_size: QParam[int],
    in_: Input[QArray[QBit, Literal["out1_size+out2_size"]]],
    out1: Output[QArray[QBit, Literal["out1_size"]]],
    out2: Output[QArray[QBit, Literal["out2_size"]]],
) -> None:
    pass


@ExternalQFunc
def permute(
    functions: QCallable,
) -> None:
    pass


@ExternalQFunc
def power(
    power: QParam[int],
    operand: QCallable[QArray[QBit, Literal["len(qbv)"]]],
    qbv: QArray[QBit],
) -> None:
    pass


@ExternalQFunc
def molecule_ucc(
    molecule_problem: QParam["MoleculeProblem"],
    excitations: QParam[List[int]],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@ExternalQFunc
def molecule_hva(
    molecule_problem: QParam["MoleculeProblem"],
    reps: QParam[int],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@ExternalQFunc
def molecule_hartree_fock(
    molecule_problem: QParam["MoleculeProblem"],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@ExternalQFunc
def fock_hamiltonian_ucc(
    fock_hamiltonian_problem: QParam["FockHamiltonianProblem"],
    excitations: QParam[List[int]],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@ExternalQFunc
def fock_hamiltonian_hva(
    fock_hamiltonian_problem: QParam["FockHamiltonianProblem"],
    reps: QParam[int],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@ExternalQFunc
def fock_hamiltonian_hartree_fock(
    fock_hamiltonian_problem: QParam["FockHamiltonianProblem"],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@ExternalQFunc
def log_normal_finance(
    finance_model: QParam["LogNormalModel"],
    finance_function: QParam["FinanceFunction"],
    func_port: QArray[QBit, Literal["get_field(finance_model, 'num_qubits')"]],
    obj_port: QBit,
) -> None:
    pass


@ExternalQFunc
def gaussian_finance(
    finance_model: QParam["GaussianModel"],
    finance_function: QParam["FinanceFunction"],
    func_port: QArray[
        QBit,
        Literal[
            "get_field(finance_model, 'num_qubits') + len(get_field(finance_model, 'rhos')) + floor(log(sum(get_field(finance_model, 'loss')), 2)) + 1"
        ],
    ],
    obj_port: QBit,
) -> None:
    pass


@ExternalQFunc
def pauli_feature_map(
    feature_map: QParam["QSVMFeatureMapPauli"],
    qbv: QArray[QBit, Literal["get_field(feature_map, 'feature_dimension')"]],
) -> None:
    pass


@ExternalQFunc
def bloch_sphere_feature_map(
    feature_dimension: QParam[int],
    qbv: QArray[QBit, Literal["ceiling(feature_dimension/2)"]],
) -> None:
    pass


__all__ = [
    "PauliTerm",
    "MoleculeProblem",
    "Molecule",
    "ChemistryAtom",
    "Position",
    "FockHamiltonianProblem",
    "LadderTerm",
    "LadderOp",
    "CombinatorialOptimizationSolution",
    "GaussianModel",
    "LogNormalModel",
    "FinanceFunction",
    "QsvmResult",
    "QSVMFeatureMapPauli",
    "qaoa_mixer_layer",
    "qaoa_cost_layer",
    "qaoa_layer",
    "qaoa_init",
    "qaoa_penalty",
    "full_hea",
    "H",
    "X",
    "Y",
    "Z",
    "I",
    "S",
    "T",
    "SDG",
    "TDG",
    "PHASE",
    "RX",
    "RY",
    "RZ",
    "RXX",
    "RYY",
    "RZZ",
    "CH",
    "CX",
    "CY",
    "CZ",
    "CRX",
    "CRY",
    "CRZ",
    "CPHASE",
    "SWAP",
    "IDENTITY",
    "prepare_state",
    "prepare_amplitudes",
    "unitary",
    "add",
    "U",
    "CCX",
    "allocate",
    "free",
    "single_pauli_exponent",
    "suzuki_trotter",
    "qdrift",
    "exponentiation_with_depth_constraint",
    "qft_step",
    "qft",
    "qpe",
    "single_pauli",
    "linear_pauli_rotations",
    "amplitude_estimation",
    "simple_oracle",
    "grover_diffuser",
    "grover_operator",
    "uniform_superposition",
    "apply_to_all",
    "grover_search",
    "prepare_int",
    "repeat",
    "invert",
    "control",
    "if_",
    "switch",
    "join",
    "split",
    "permute",
    "power",
    "molecule_ucc",
    "molecule_hva",
    "molecule_hartree_fock",
    "fock_hamiltonian_ucc",
    "fock_hamiltonian_hva",
    "fock_hamiltonian_hartree_fock",
    "log_normal_finance",
    "gaussian_finance",
    "pauli_feature_map",
    "bloch_sphere_feature_map",
]
