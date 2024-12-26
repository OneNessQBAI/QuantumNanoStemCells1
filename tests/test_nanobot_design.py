import pytest
import numpy as np
from src.nanobot_design import NanobotDesigner

def test_nanobot_designer_initialization():
    designer = NanobotDesigner()
    assert designer.dimensions == 3
    
    designer_2d = NanobotDesigner(dimensions=2)
    assert designer_2d.dimensions == 2

def test_nanobot_design():
    designer = NanobotDesigner()
    nanobot = designer.design_nanobot(20, "mRNA")
    
    assert isinstance(nanobot, dict)
    assert all(key in nanobot for key in ['size', 'payload', 'efficiency', 'delivery_mechanism'])
    assert nanobot['size'] == 20
    assert nanobot['payload'] == "mRNA"
    assert 0 <= nanobot['efficiency'] <= 1
    assert nanobot['delivery_mechanism'] in ["passive_diffusion", "active_transport", "guided_propulsion"]

def test_delivery_mechanism_optimization():
    designer = NanobotDesigner()
    
    # Test different size ranges
    small_bot = designer.design_nanobot(5, "mRNA")
    medium_bot = designer.design_nanobot(30, "mRNA")
    large_bot = designer.design_nanobot(80, "mRNA")
    
    assert small_bot['delivery_mechanism'] == "passive_diffusion"
    assert medium_bot['delivery_mechanism'] == "active_transport"
    assert large_bot['delivery_mechanism'] == "guided_propulsion"

def test_delivery_simulation():
    designer = NanobotDesigner()
    nanobot = designer.design_nanobot(20, "mRNA")
    target = np.array([1.0, 1.0, 1.0])
    
    result = designer.simulate_delivery(nanobot, target)
    
    assert isinstance(result, dict)
    assert all(key in result for key in ['path', 'steps', 'success_rate'])
    assert len(result['path']) > 0
    assert result['steps'] > 0
    assert 0 <= result['success_rate'] <= 1

def test_efficiency_calculation():
    designer = NanobotDesigner()
    
    # Test size impact
    large_bot = designer.design_nanobot(90, "mRNA")
    small_bot = designer.design_nanobot(10, "mRNA")
    assert small_bot['efficiency'] > large_bot['efficiency']
    
    # Test payload impact
    simple_payload = designer.design_nanobot(20, "small_molecules")
    complex_payload = designer.design_nanobot(20, "plasmids")
    assert simple_payload['efficiency'] > complex_payload['efficiency']

def test_movement_calculation():
    designer = NanobotDesigner()
    nanobot = designer.design_nanobot(20, "mRNA")
    current = np.zeros(3)
    target = np.ones(3)
    
    movement, velocity, effects = designer._calculate_movement_with_effects(current, target, nanobot)
    assert movement.shape == (3,)
    assert isinstance(velocity, float)
    assert all(key in effects for key in ['brownian_motion', 'fluid_resistance', 'cellular_interaction'])
    assert effects['brownian_motion'].shape == (3,)

def test_target_reaching():
    designer = NanobotDesigner()
    current = np.array([0.999999, 1.0, 1.0])
    target = np.array([1.0, 1.0, 1.0])
    
    assert designer._reached_target(current, target)
    assert not designer._reached_target(np.zeros(3), target)

def test_invalid_inputs():
    designer = NanobotDesigner()
    
    with pytest.raises(ValueError):
        designer.design_nanobot(-10, "mRNA")  # Negative size
        
    with pytest.raises(ValueError):
        designer.simulate_delivery(None, np.ones(3))  # Invalid nanobot
