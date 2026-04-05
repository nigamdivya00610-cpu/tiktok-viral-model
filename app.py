import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

st.title("📈 TikTok Viral Spread: Growth-Decay & Network Model")
st.markdown("""
This model simulates a TikTok video's journey. It uses a **Scale-Free Network** (representing influencers and followers) 
and a **Growth-Decay** differential logic to track how users move between being Passive, Viewers, and Sharers.
""")

# --- Sidebar Inputs ---
st.sidebar.header("🕹️ Simulation Controls")
N = st.sidebar.slider("Total Users (N)", 100, 1000, 500)
m = st.sidebar.slider("Network Connectivity (m)", 1, 5, 2)
alpha = st.sidebar.slider("Growth Rate (Virality)", 0.1, 1.0, 0.6)
beta = st.sidebar.slider("Decay Rate (Boredom)", 0.01, 0.5, 0.1)
steps = st.sidebar.slider("Time Steps", 50, 200, 100)

intervention = st.sidebar.selectbox("Intervention Strategy", ["None", "Seed Influencers", "Shadowban Hubs"])

# --- Simulation Logic ---
def run_simulation():
    # 1. Network Structure (Barabási-Albert)
    G = nx.barabasi_albert_graph(N, m)
    centrality = nx.degree_centrality(G)
    
    # Initialize States: 0=Passive, 1=Viewer, 2=Sharer
    status = np.zeros(N)
    
    # Intervention Strategy Logic
    sorted_nodes = sorted(centrality, key=centrality.get, reverse=True)
    if intervention == "Seed Influencers":
        for i in sorted_nodes[:5]: status[i] = 2 # Top 5 become active sharers
    elif intervention == "Shadowban Hubs":
        for i in sorted_nodes[:5]: centrality[i] = 0 # Top 5 lose all reach
    else:
        status[np.random.randint(0, N, 5)] = 2 # Random initial seeds

    v_hist, s_hist, p_hist = [], [], []

    # 2. Growth-Decay Loop
    for _ in range(steps):
        new_status = status.copy()
        for i in G.nodes():
            if status[i] == 2: # Sharer
                # Growth: Infect neighbors based on centrality and alpha
                for neighbor in G.neighbors(i):
                    if status[neighbor] == 0:
                        if np.random.rand() < (alpha * (1 + centrality[i])):
                            new_status[neighbor] = 1
                # Decay: Sharer becomes Passive/Bored
                if np.random.rand() < beta:
                    new_status[i] = 0
            
            elif status[i] == 1: # Viewer
                # Transition: Viewer becomes Sharer
                if np.random.rand() < (alpha * 0.5):
                    new_status[i] = 2
                # Decay: Viewer becomes Passive
                if np.random.rand() < beta:
                    new_status[i] = 0
        
        status = new_status
        v_hist.append(np.sum(status == 1))
        s_hist.append(np.sum(status == 2))
        p_hist.append(np.sum(status == 0))

    return v_hist, s_hist, p_hist, G

v_data, s_data, p_data, G_final = run_simulation()

# --- Metrics ---
peak_views = max(v_data)
peak_time = v_data.index(peak_views)

col1, col2, col3 = st.columns(3)
col1.metric("🔥 Peak Viewers", int(peak_views))
col2.metric("⏱️ Peak Time", peak_time)
col3.metric("🕸️ Network Density", f"{nx.density(G_final):.4f}")

# --- Output Graphs ---
st.header("📊 Visualization of Spread")
g1, g2 = st.columns(2)

with g1:
    st.subheader("1. Viewer Growth Curve")
    fig1, ax1 = plt.subplots()
    ax1.plot(v_data, color='red', label="Viewers")
    ax1.set_ylabel("Count")
    ax1.legend()
    st.pyplot(fig1)

with g2:
    st.subheader("2. Sharer Activity (Virality)")
    fig2, ax2 = plt.subplots()
    ax2.plot(s_data, color='blue', label="Sharers")
    ax2.set_ylabel("Count")
    ax2.legend()
    st.pyplot(fig2)

st.subheader("3. Final Combined Graph (Total Dynamics)")
fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(v_data, label="Viewers (V)", color='red', alpha=0.8)
ax3.plot(s_data, label="Sharers (S)", color='blue', alpha=0.8)
ax3.plot(p_data, label="Passive (P)", color='green', alpha=0.5, linestyle='--')
ax3.axvline(peak_time, color='black', linestyle=':', label="Viral Peak")
ax3.set_xlabel("Time Steps")
ax3.set_ylabel("User Count")
ax3.legend()
st.pyplot(fig3)

# --- Interpretation ---
st.header("📝 Result Interpretation")
with st.expander("Click to see analysis", expanded=True):
    if peak_views > (N * 0.5):
        st.success(f"**Massive Virality:** The video reached {int(peak_views)} users simultaneously. The Growth rate (α={alpha}) successfully overcame the Decay rate (β={beta}).")
    else:
        st.warning("**Niche Reach:** The video did not break into the mainstream. The decay rate was too high relative to the network connections.")

    st.write(f"- **Network Centrality Impact:** The peak occurred at step {peak_time}. By using the '{intervention}' strategy, the 'hubs' in the scale-free network either accelerated or throttled the spread.")
    st.write("- **Saturation Point:** Notice where the Passive (Green) line stabilizes; this represents the 'exhausted audience' who can no longer be reached.")
