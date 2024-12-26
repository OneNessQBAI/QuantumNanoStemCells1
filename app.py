import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.quantum_sim import QuantumCellSimulator
from src.nanobot_design import NanobotDesigner

st.set_page_config(page_title="Quantum Cell Reprogramming & Nanobot Delivery", layout="wide")

def plot_3d_trajectory(path_3d):
    """Create 3D trajectory plot using plotly."""
    path = np.array(path_3d)
    fig = go.Figure(data=[go.Scatter3d(
        x=path[:, 0],
        y=path[:, 1],
        z=path[:, 2],
        mode='lines+markers',
        marker=dict(
            size=2,
            color=np.arange(len(path)),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Step')
        ),
        line=dict(color='darkblue', width=2)
    )])
    
    fig.update_layout(
        title='Nanobot Delivery Trajectory',
        scene=dict(
            xaxis_title='X Position',
            yaxis_title='Y Position',
            zaxis_title='Z Position'
        ),
        width=700,
        height=700
    )
    return fig

def plot_quantum_states(states):
    """Create quantum state visualization."""
    if not states:
        return None
        
    # Get the last few states for visualization
    recent_states = states[-5:]
    labels = [f"Step {s['step']}: {s['operation']}" for s in recent_states]
    values = [np.abs(s['state_vector'])**2 for s in recent_states]
    
    fig = go.Figure()
    for i, (label, value) in enumerate(zip(labels, values)):
        fig.add_trace(go.Bar(
            name=label,
            y=value,
            x=[f"|{i}⟩" for i in range(len(value))],
            visible=True if i == len(values)-1 else "legendonly"
        ))
    
    fig.update_layout(
        title='Quantum State Evolution',
        xaxis_title='Basis State',
        yaxis_title='Probability',
        barmode='group',
        width=700,
        height=500
    )
    return fig

def main():
    st.title("Quantum Cell Reprogramming & Nanobot Delivery System")
    
    # Add links to websites
    st.sidebar.markdown("""
    ### Links
    - [OpenQuantum](https://www.openquantum.ca)
    - [OnenessCan](https://www.onenesscan.com)
    """)
    
    # Cell Reprogramming Section
    st.header("1. Cell Reprogramming")
    col1, col2 = st.columns(2)
    
    simulation_results = None
    with col1:
        st.subheader("Input Parameters")
        target_cell_type = np.array([
            st.slider("Pluripotency Factor", 0.0, 1.0, 0.5),
            st.slider("Differentiation Factor", 0.0, 1.0, 0.3),
            st.slider("Growth Factor", 0.0, 1.0, 0.4),
            st.slider("Survival Factor", 0.0, 1.0, 0.6)
        ])
        
        if st.button("Run Quantum Simulation"):
            simulator = QuantumCellSimulator()
            simulation_results = simulator.simulate_reprogramming(target_cell_type)
            
            with col2:
                st.subheader("Simulation Results")
                st.write("Quantum State Distribution:")
                st.bar_chart(simulation_results['final_results'])
                
                # Calculate success probability
                st.metric("Reprogramming Success Probability", 
                         f"{simulation_results['success_metric']:.2%}")
                
                # Display quantum circuit
                st.subheader("Quantum Circuit")
                st.code(simulation_results['circuit_diagram'])
                
                # Plot quantum states
                st.subheader("Quantum State Evolution")
                state_fig = plot_quantum_states(simulation_results['intermediate_states'])
                if state_fig:
                    st.plotly_chart(state_fig)
    
    # Nanobot Design Section
    st.header("2. Nanobot Delivery System")
    col3, col4 = st.columns(2)
    
    nanobot_config = None
    delivery_sim = None
    with col3:
        st.subheader("Nanobot Parameters")
        target_size = st.slider("Nanobot Size (nm)", 5, 100, 20)
        payload_type = st.selectbox(
            "Payload Type",
            ["mRNA", "proteins", "plasmids", "small_molecules"]
        )
        
        if st.button("Design Nanobot"):
            designer = NanobotDesigner()
            nanobot_config = designer.design_nanobot(target_size, payload_type)
            
            # Simulate delivery to a random target
            target = np.random.rand(3)  # 3D coordinates
            delivery_sim = designer.simulate_delivery(nanobot_config, target)
            
            with col4:
                st.subheader("Design Results")
                
                # Basic metrics
                st.metric("Overall Efficiency", f"{nanobot_config['efficiency']:.2%}")
                st.metric("Delivery Success Rate", f"{delivery_sim['success_rate']:.2%}")
                
                # Detailed efficiency factors
                st.subheader("Efficiency Breakdown")
                factors = nanobot_config['efficiency_factors']
                st.json({
                    'Base Efficiency': factors['base_efficiency'],
                    'Size Factor': factors['size_factor'],
                    'Payload Properties': factors['payload_factors'],
                    'Environmental Impact': factors['environmental_factors']
                })
                
                # Trajectory Analysis
                st.subheader("Delivery Analysis")
                analysis = delivery_sim['trajectory_analysis']
                st.write(f"Total Distance: {analysis['total_distance']:.2f} units")
                st.write(f"Average Velocity: {analysis['average_velocity']:.2f} units/step")
                st.write(f"Path Linearity: {analysis['path_linearity']:.2%}")
                
                # 3D Trajectory Visualization
                st.subheader("3D Delivery Path")
                fig_3d = plot_3d_trajectory(delivery_sim['path_3d'])
                st.plotly_chart(fig_3d)
                
                # Design Specifications
                st.subheader("Design Specifications")
                st.json(nanobot_config['design_specs'])
    
    # Download Section
    st.header("3. Download Results & Protocol")
    if nanobot_config and delivery_sim:
        # Create detailed CSV with simulation data
        data = {
            'Parameter': [],
            'Value': []
        }
        
        # Add nanobot configuration
        for key, value in nanobot_config.items():
            if key not in ['efficiency_factors', 'design_specs']:
                data['Parameter'].append(f"Nanobot {key}")
                data['Value'].append(str(value))
        
        # Add efficiency factors
        for key, value in nanobot_config['efficiency_factors'].items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    data['Parameter'].append(f"Efficiency - {key} - {subkey}")
                    data['Value'].append(str(subvalue))
            else:
                data['Parameter'].append(f"Efficiency - {key}")
                data['Value'].append(str(value))
        
        # Add trajectory analysis
        for key, value in delivery_sim['trajectory_analysis'].items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    data['Parameter'].append(f"Trajectory - {key} - {subkey}")
                    data['Value'].append(str(subvalue))
            else:
                data['Parameter'].append(f"Trajectory - {key}")
                data['Value'].append(str(value))
        
        if simulation_results:
            data['Parameter'].append('Quantum Reprogramming Success')
            data['Value'].append(f"{simulation_results['success_metric']:.2%}")
        
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Simulation Data (CSV)",
            data=csv,
            file_name="quantum_nanobot_simulation.csv",
            mime="text/csv"
        )
        
        # Generate and offer lab protocol
        protocol = generate_lab_protocol(nanobot_config, simulation_results)
        st.download_button(
            label="Download Lab Protocol (TXT)",
            data=protocol,
            file_name="lab_protocol.txt",
            mime="text/plain"
        )
    
    # System Status
    st.sidebar.markdown("---")
    st.sidebar.subheader("System Status")
    st.sidebar.success("Quantum Computer: Connected")
    st.sidebar.info("Nanobot Designer: Active")
    
    # Contact Information
    st.sidebar.markdown("---")
    st.sidebar.subheader("Contact")
    st.sidebar.markdown("""
    - Email: [jerry@openquantum.ca](mailto:jerry@openquantum.ca)
    - Support: [info@openquantum.ca](mailto:info@openquantum.ca)
    """)

def generate_lab_protocol(nanobot_config, quantum_results=None):
    """Generate detailed lab protocol based on simulation results."""
    protocol = []
    
    protocol.append("Laboratory Protocol for Quantum-Guided Nanobot Cell Reprogramming")
    protocol.append("\n1. Equipment Required:")
    protocol.append("- Transmission Electron Microscope (TEM)")
    protocol.append("- Dynamic Light Scattering (DLS) analyzer")
    protocol.append("- Zeta potential analyzer")
    protocol.append("- Cell culture facility with biosafety cabinet")
    protocol.append("- CO2 incubator")
    protocol.append("- Fluorescence microscope")
    protocol.append("- Microfluidic device fabrication equipment")
    protocol.append("- Real-time PCR system")
    protocol.append("- Flow cytometer")
    
    protocol.append("\n2. Materials Required:")
    protocol.append("- Cell culture medium (DMEM/F12)")
    protocol.append("- Growth factors and cytokines")
    protocol.append(f"- {nanobot_config['payload']} synthesis kit")
    protocol.append("- Biocompatible polymer for nanobot fabrication")
    protocol.append("- Quantum dots for tracking")
    protocol.append("- Cell viability assay kit")
    
    protocol.append("\n3. Nanobot Fabrication:")
    protocol.append(f"- Target size: {nanobot_config['size']} nm")
    protocol.append(f"- Delivery mechanism: {nanobot_config['delivery_mechanism']}")
    protocol.append(f"- Surface chemistry: {nanobot_config['design_specs']['surface_chemistry']}")
    protocol.append("\nCoating specifications:")
    for key, value in nanobot_config['design_specs']['coating_requirements'].items():
        protocol.append(f"- {key}: {value}")
    
    protocol.append("\n4. Cell Preparation:")
    protocol.append("- Isolate target cells using FACS")
    protocol.append("- Culture in stem cell maintenance medium")
    protocol.append("- Verify cell viability (>90% required)")
    protocol.append("- Perform baseline gene expression analysis")
    
    protocol.append("\n5. Reprogramming Process:")
    if quantum_results:
        protocol.append(f"- Expected success rate: {quantum_results['success_metric']:.2%}")
    protocol.append("- Monitor transformation using live cell imaging")
    protocol.append("- Collect time-lapse microscopy data")
    protocol.append("- Perform periodic cell viability checks")
    
    protocol.append("\n6. Quality Control:")
    protocol.append("- Verify reprogramming using RT-PCR")
    protocol.append("- Perform immunostaining for pluripotency markers")
    protocol.append("- Conduct functional assays")
    protocol.append("- Analyze gene expression profiles")
    protocol.append("- Perform epigenetic characterization")
    
    protocol.append("\n7. Safety Considerations:")
    protocol.append("- Use appropriate PPE at all times")
    protocol.append("- Handle biological materials in certified biosafety cabinet")
    protocol.append("- Follow institutional biosafety guidelines")
    protocol.append("- Properly dispose of biological waste")
    
    return "\n".join(protocol)

if __name__ == "__main__":
    main()
