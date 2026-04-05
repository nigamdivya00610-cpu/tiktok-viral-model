import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Simulation Logic ---
def run_viral_simulation(n_nodes, m_edges, spread_prob, decay_rate, initial_seeds):
    # 1. Create a Scale-Free Network (realistic for social media)
    G = nx.barabasi_albert_graph(n_nodes, m_edges)
    
    # Calculate Centrality (used for intervention strategy)
    centrality = nx.degree_centrality(G)
    
    # State mapping: 0 = Passive, 1 = Viewer, 2 = Sharer
    status = np.zeros(n_nodes)
    
    # Intervention: Seed the most central nodes (influencers)
    top_nodes = sorted(centrality, key=centrality.get, reverse=True)
    for i in range(initial_seeds):
        status[top_nodes[i]] = 1
        
    history = []
    
    for t in range(50): # 50 time steps
        new_status = status.copy()
        for node in G.nodes():
            if status[node] == 1: # Current Viewer
                # Growth: Try to spread to neighbors
                for neighbor in G.neighbors(node):
                    if status[neighbor] == 0 and np.random.random() < spread_prob:
                        new_status[neighbor] = 1
                
                # Internal Decay: Move from Viewer to Passive (boredom)
                if np.random.random() < decay_rate:
                    new_status[node] = 2 # Using 2 as 'Stopped watching/Passive'
            
        status = new_status
        history.append({
            "Step": t,
            "Active Viewers": np.sum(status == 1),
            "Reached Total": np.sum(status > 0)
        })
        
    return pd.DataFrame(history), G, centrality

# --- Streamlit UI ---
st.set_page_config(page_title="TikTok Viral Model", layout="wide")
st.title("📈 TikTok Viral Spread Simulator")

with st.sidebar:
    st.header("Simulation Parameters")
    n_nodes = st.slider("Total Users", 100, 1000, 500)
    spread_prob = st.slider("Virality (Spread Prob)", 0.01, 0.20, 0.05)
    decay_rate = st.slider("Decay (Boredom Rate)", 0.01, 0.20, 0.08)
    initial_seeds = st.number_input("Initial Influencer Seeds", 1, 10, 3)

if st.button("Run Viral Simulation"):
    df, G, centrality = run_viral_simulation(n_nodes, 2, spread_prob, decay_rate, initial_seeds)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Viral Growth-Decay Curve")
        st.line_chart(df.set_index("Step"))
        
        peak_val = df["Active Viewers"].max()
        st.metric("Peak Concurrent Viewers", f"{int(peak_val)}")
        
    with col2:
        st.subheader("Network Metrics")
        avg_cent = sum(centrality.values()) / len(centrality)
        st.write(f"**Network Density:** {nx.density(G):.4f}")
        st.write(f"**Avg Centrality:** {avg_cent:.4f}")
        
        st.info("The simulation automatically targets nodes with the highest **Degree Centrality** to model an effective intervention strategy.")

    # Visualization of the Network
    st.subheader("Final Social Graph Snapshot")
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.spring_layout(G, k=0.15)
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='teal', alpha=0.7)
    nx.draw_networkx_edges(G, pos, alpha=0.1)
    st.pyplot(fig)
