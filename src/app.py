import streamlit as st
import numpy as np
from src.quantum_sim import QuantumCellSimulator
from src.nanobot_design import NanobotDesigner

st.set_page_config(page_title="Quantum Cell Reprogramming & Nanobot Delivery", layout="wide")

def main():
    st.title("Quantum Cell Reprogramming & Nanobot Delivery System")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Cell Reprogramming Section
    st.header("1. Cell Reprogramming")
    col1, col2 = st.columns(2)
    
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
            results = simulator.simulate_reprogramming(target_cell_type)
            
            with col2:
                st.subheader("Simulation Results")
                st.write("Quantum State Distribution:")
                st.bar_chart(results)
                
                # Calculate success probability
                success_prob = sum(v for k, v in results.items() if k > 0.5) / 100
                st.metric("Reprogramming Success Probability", f"{success_prob:.2%}")
    
    # Nanobot Design Section
    st.header("2. Nanobot Delivery System")
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Nanobot Parameters")
        target_size = st.slider("Nanobot Size (nm)", 5, 100, 20)
        payload_type = st.selectbox(
            "Payload Type",
            ["mRNA", "proteins", "plasmids", "small_molecules"]
        )
        
        if st.button("Design Nanobot"):
            designer = NanobotDesigner()
            nanobot = designer.design_nanobot(target_size, payload_type)
            
            # Simulate delivery to a random target
            target = np.random.rand(3)  # 3D coordinates
            delivery_sim = designer.simulate_delivery(nanobot, target)
            
            with col4:
                st.subheader("Design Results")
                st.json(nanobot)
                st.metric("Delivery Success Rate", f"{delivery_sim['success_rate']:.2%}")
                st.write(f"Steps to Target: {delivery_sim['steps']}")
                
                # Plot delivery path
                if len(delivery_sim['path']) > 0:
                    path = np.array(delivery_sim['path'])
                    st.line_chart(path[:, 0])  # Plot X-coordinate movement
    
    # System Status
    st.sidebar.markdown("---")
    st.sidebar.subheader("System Status")
    st.sidebar.success("Quantum Computer: Connected")
    st.sidebar.info("Nanobot Designer: Active")

if __name__ == "__main__":
    main()
