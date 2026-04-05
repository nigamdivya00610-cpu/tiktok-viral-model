import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd

st.title("TikTok Growth-Decay Network Model")

# Sidebar Inputs
st.sidebar.header("Model Parameters")
r = st.sidebar.slider("Virality Rate (r)", 0.1, 1.0, 0.4)
delta = st.sidebar.slider("Decay Rate (δ)", 0.05, 0.5, 0.2)
n_users = st.sidebar.slider("Network Size", 100, 1000, 500)

def simulate_viral_logic(n, r, delta):
    # 1. Create Scale-Free Network (Network Structure)
    G = nx.barabasi_albert_graph(n, 3)
    centrality = nx.degree_centrality(G)
    
    # 2. Initial State: Start with top 3 influencers
    seeds = sorted(centrality, key=centrality.get, reverse=True)[:3]
    active_viewers = np.zeros(n)
    active_viewers[seeds] = 1.0
    
    results = []
    
    # 3. Time-Stepping (Euler Method for dV/dt)
    for t in range(50):
        current_total = np.sum(active_viewers)
        
        # Calculate Network-Weighted Growth
        # High centrality sharers push the video to more 'Passive' nodes
        new_viewers = active_viewers.copy()
        
        for i in G.nodes():
            if active_viewers[i] > 0.1: # If node is an active sharer
                neighbors = list(G.neighbors(i))
                for neighbor in neighbors:
                    # Growth Formula: Rate adjusted by node importance
                    growth = r * centrality[i] * (1 - current_total/n)
                    # Decay Formula: Natural loss of interest
                    decay = delta * active_viewers[i]
                    
                    new_viewers[neighbor] += growth
                    new_viewers[i] -= decay
        
        # Clip values between 0 and 1 (probability/intensity)
        active_viewers = np.clip(new_viewers, 0, 1)
        
        results.append({
            "Time": t,
            "Viral Intensity": np.sum(active_viewers),
            "Growth Rate": r * (1 - np.sum(active_viewers)/n)
        })
        
    return pd.DataFrame(results)

# Execution
data = simulate_viral_logic(n_users, r, delta)

# Visualization
st.subheader("The Viral Curve: $dV/dt = Growth - Decay$")
st.line_chart(data.set_index("Time")[["Viral Intensity"]])

st.write(f"**Peak Reach:** {data['Viral Intensity'].max():.2f} users")
st.latex(r"\frac{dV}{dt} = rV(1 - \frac{V}{K}) - \delta V")
