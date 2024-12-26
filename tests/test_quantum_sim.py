import pytest
import numpy as np
import cirq
from src.quantum_sim import QuantumCellSimulator

def test_quantum_simulator_initialization():
    simulator = QuantumCellSimulator()
    assert len(simulator.qubits) == 4
    assert simulator.qubits[0].row == 0
    assert simulator.qubits[0].col == 0

def test_reprogramming_circuit_creation():
    simulator = QuantumCellSimulator()
    target_cell_type = np.array([0.5, 0.3, 0.4, 0.6])
    circuit = simulator.create_reprogramming_circuit(target_cell_type)
    
    # Check if circuit is created with correct number of moments
    assert len(circuit) > 0
    
    # Verify measurement operation is included
    has_measurement = False
    for moment in circuit:
        for op in moment:
            if isinstance(op.gate, cirq.MeasurementGate):
                has_measurement = True
                break
        if has_measurement:
            break
    assert has_measurement

def test_reprogramming_simulation():
    simulator = QuantumCellSimulator()
    target_cell_type = np.array([0.5, 0.3, 0.4, 0.6])
    results = simulator.simulate_reprogramming(target_cell_type)
    
    # Check if results are in correct format
    assert isinstance(results, dict)
    assert len(results) > 0
    
    # Verify probabilities sum to total number of repetitions
    total_counts = sum(results.values())
    assert total_counts == 100  # Default repetitions

def test_transformation_optimization():
    simulator = QuantumCellSimulator()
    initial_state = np.array([0, 0, 0, 0])
    target_state = np.array([1, 1, 1, 1])
    
    circuit = simulator.optimize_transformation(initial_state, target_state)
    assert len(circuit) > 0

def test_invalid_target_cell_type():
    simulator = QuantumCellSimulator()
    with pytest.raises(ValueError):
        # Test with invalid array length
        invalid_target = np.array([0.5, 0.3, 0.4])
        simulator.simulate_reprogramming(invalid_target)

def test_optimization_steps():
    simulator = QuantumCellSimulator()
    initial_state = np.array([0, 0, 0, 0])
    target_state = np.array([1, 1, 1, 1])
    
    # Test with different step counts
    circuit_short = simulator.optimize_transformation(initial_state, target_state, steps=5)
    circuit_long = simulator.optimize_transformation(initial_state, target_state, steps=10)
    
    assert len(circuit_long) > len(circuit_short)
