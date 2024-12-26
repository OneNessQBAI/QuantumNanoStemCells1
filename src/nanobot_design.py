import numpy as np
from scipy.spatial import distance

class NanobotDesigner:
    def __init__(self, dimensions=3):
        self.dimensions = dimensions
        
    def design_nanobot(self, target_size, payload_type):
        """Design nanobot with specific parameters and environmental considerations."""
        if target_size <= 0:
            raise ValueError("Target size must be positive")
            
        efficiency = self._calculate_efficiency(target_size, payload_type)
        delivery_mechanism = self._optimize_delivery_mechanism(target_size)
        
        return {
            'size': target_size,
            'payload': payload_type,
            'efficiency': efficiency['overall_efficiency'],
            'efficiency_factors': efficiency['factors'],
            'delivery_mechanism': delivery_mechanism,
            'design_specs': self._generate_design_specs(target_size, payload_type)
        }
        
    def simulate_delivery(self, nanobot, target_coordinates):
        """Simulate nanobot delivery to target cells with detailed trajectory."""
        if nanobot is None:
            raise ValueError("Invalid nanobot configuration")
            
        current_pos = np.zeros(self.dimensions)
        path = [current_pos.copy()]
        velocities = []
        environmental_effects = []
        max_steps = 1000  # Prevent infinite loops
        step_count = 0
        
        while not self._reached_target(current_pos, target_coordinates) and step_count < max_steps:
            # Calculate movement with environmental factors
            movement, velocity, effects = self._calculate_movement_with_effects(
                current_pos, target_coordinates, nanobot
            )
            current_pos += movement
            path.append(current_pos.copy())
            velocities.append(velocity)
            environmental_effects.append(effects)
            step_count += 1
            
        success_rate = self._calculate_success_rate(path, target_coordinates)
        trajectory_analysis = self._analyze_trajectory(path, velocities, environmental_effects)
        
        return {
            'path': path,
            'steps': len(path),
            'success_rate': success_rate,
            'trajectory_analysis': trajectory_analysis,
            'path_3d': np.array(path),  # For 3D visualization
            'velocities': velocities,
            'environmental_effects': environmental_effects,
            'target_reached': step_count < max_steps
        }
    
    def _calculate_efficiency(self, size, payload):
        """Calculate delivery efficiency with detailed environmental factors."""
        base_efficiency = 0.9
        
        # Size factor - smaller is generally better but with optimal range
        size_factor = np.exp(-(size - 30)**2 / 800)  # Peak efficiency around 30nm
        
        # Payload complexity weights with detailed factors
        payload_weights = {
            'small_molecules': {'weight': 0.1, 'stability': 0.95, 'diffusion': 0.9},
            'mRNA': {'weight': 0.3, 'stability': 0.7, 'diffusion': 0.8},
            'proteins': {'weight': 0.5, 'stability': 0.8, 'diffusion': 0.7},
            'plasmids': {'weight': 0.7, 'stability': 0.6, 'diffusion': 0.5}
        }
        
        payload_data = payload_weights.get(payload, payload_weights['mRNA'])
        
        # Environmental factors
        environmental_factors = {
            'ph_sensitivity': 0.95,
            'temperature_stability': 0.9,
            'cellular_barriers': 0.85,
            'degradation_resistance': 0.88
        }
        
        # Calculate overall efficiency
        payload_efficiency = (1.0 - payload_data['weight']) * payload_data['stability'] * payload_data['diffusion']
        env_efficiency = np.mean(list(environmental_factors.values()))
        overall_efficiency = base_efficiency * size_factor * payload_efficiency * env_efficiency
        
        return {
            'overall_efficiency': overall_efficiency,
            'factors': {
                'base_efficiency': base_efficiency,
                'size_factor': float(size_factor),  # Convert from numpy to native Python float
                'payload_factors': payload_data,
                'environmental_factors': environmental_factors
            }
        }
    
    def _optimize_delivery_mechanism(self, size):
        """Optimize the delivery mechanism based on nanobot size."""
        if size < 10:
            return "passive_diffusion"
        elif size < 50:
            return "active_transport"
        else:
            return "guided_propulsion"
    
    def _reached_target(self, current, target, threshold=1e-3):
        """Check if nanobot has reached the target."""
        return np.linalg.norm(current - target) < threshold
    
    def _calculate_movement_with_effects(self, current, target, nanobot):
        """Calculate movement with environmental effects."""
        direction = target - current
        direction_norm = np.linalg.norm(direction)
        if direction_norm > 0:
            direction = direction / direction_norm
        
        # Base velocity depends on delivery mechanism
        mechanism_velocity = {
            'passive_diffusion': 0.05,
            'active_transport': 0.1,
            'guided_propulsion': 0.15
        }
        base_velocity = mechanism_velocity[nanobot['delivery_mechanism']] * nanobot['efficiency']
        
        # Environmental effects
        brownian_motion = np.random.normal(0, 0.01, self.dimensions)
        fluid_resistance = -0.05 * base_velocity
        cellular_interaction = 0.02 * np.sin(np.sum(current))  # Simplified cellular interaction
        
        # Combined effects
        velocity = base_velocity + fluid_resistance
        movement = direction * velocity + brownian_motion + cellular_interaction * direction
        
        effects = {
            'brownian_motion': brownian_motion,
            'fluid_resistance': fluid_resistance,
            'cellular_interaction': cellular_interaction
        }
        
        return movement, velocity, effects
    
    def _analyze_trajectory(self, path, velocities, effects):
        """Analyze the delivery trajectory."""
        path_array = np.array(path)
        
        if len(path_array) < 2:
            return {
                'total_distance': 0.0,
                'average_velocity': 0.0,
                'velocity_variance': 0.0,
                'path_linearity': 1.0,
                'environmental_impact': self._analyze_environmental_impact(effects)
            }
        
        distances = np.linalg.norm(path_array[1:] - path_array[:-1], axis=1)
        
        return {
            'total_distance': float(np.sum(distances)),
            'average_velocity': float(np.mean(velocities)),
            'velocity_variance': float(np.var(velocities)),
            'path_linearity': float(self._calculate_path_linearity(path_array)),
            'environmental_impact': self._analyze_environmental_impact(effects)
        }
    
    def _calculate_path_linearity(self, path_array):
        """Calculate how linear the path is (1.0 = perfectly linear)."""
        if len(path_array) < 2:
            return 1.0
        
        direct_distance = np.linalg.norm(path_array[-1] - path_array[0])
        actual_distance = np.sum(np.linalg.norm(path_array[1:] - path_array[:-1], axis=1))
        
        return direct_distance / actual_distance if actual_distance > 0 else 1.0
    
    def _analyze_environmental_impact(self, effects):
        """Analyze the impact of environmental effects."""
        return {
            'brownian_intensity': float(np.mean([np.linalg.norm(e['brownian_motion']) for e in effects])),
            'resistance_impact': float(np.mean([e['fluid_resistance'] for e in effects])),
            'cellular_interaction_strength': float(np.mean([e['cellular_interaction'] for e in effects]))
        }
    
    def _calculate_success_rate(self, path, target):
        """Calculate success rate of delivery based on path."""
        final_distance = np.linalg.norm(path[-1] - target)
        path_efficiency = 1.0 / len(path)  # Shorter paths are more efficient
        max_expected_distance = np.linalg.norm(target)  # Maximum expected distance
        
        # Normalize distance to [0, 1] range
        normalized_distance = min(final_distance / max_expected_distance, 1.0)
        distance_score = 1.0 - normalized_distance
        
        return float(0.7 * distance_score + 0.3 * path_efficiency)
    
    def _generate_design_specs(self, size, payload_type):
        """Generate detailed design specifications."""
        return {
            'surface_chemistry': self._determine_surface_chemistry(payload_type),
            'coating_requirements': self._determine_coating(size, payload_type),
            'stability_parameters': self._calculate_stability_parameters(size, payload_type),
            'manufacturing_protocol': self._generate_manufacturing_protocol(size, payload_type)
        }
    
    def _determine_surface_chemistry(self, payload_type):
        """Determine optimal surface chemistry based on payload."""
        surface_properties = {
            'small_molecules': {'charge': 'neutral', 'hydrophobicity': 'moderate'},
            'mRNA': {'charge': 'positive', 'hydrophobicity': 'low'},
            'proteins': {'charge': 'variable', 'hydrophobicity': 'moderate'},
            'plasmids': {'charge': 'positive', 'hydrophobicity': 'low'}
        }
        return surface_properties.get(payload_type, surface_properties['mRNA'])
    
    def _determine_coating(self, size, payload_type):
        """Determine appropriate coating specifications."""
        base_coating = {
            'material': 'PEG',
            'thickness_nm': size * 0.1,
            'degradation_rate': '0.1nm/hour'
        }
        return base_coating
    
    def _calculate_stability_parameters(self, size, payload_type):
        """Calculate stability parameters."""
        return {
            'temperature_range': {'min': 4, 'max': 40},
            'ph_range': {'min': 6.5, 'max': 7.5},
            'shelf_life_days': 30,
            'zeta_potential': -30  # mV
        }
    
    def _generate_manufacturing_protocol(self, size, payload_type):
        """Generate basic manufacturing protocol steps."""
        return [
            'Prepare biocompatible polymer solution',
            'Add payload under controlled conditions',
            'Perform nanoprecipitation',
            'Apply surface coating',
            'Purify using tangential flow filtration',
            'Perform quality control'
        ]
