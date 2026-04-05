import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 Advanced TikTok Viral Spread Model (Improved)")

# -----------------------------
# PARAMETERS
# -----------------------------
st.markdown("## 🔧 Model Parameters")

N = st.slider("Total Users (N)", 100, 2000, 500)

alpha = st.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
beta = st.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
gamma = st.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)
delta = st.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

time_steps = st.slider("Time Steps", 50, 300, 150)

V0 = st.number_input("Initial Viewers", 1, N, 10)
S0 = st.number_input("Initial Sharers", 1, N, 5)

boost = st.slider("Algorithm Boost", 1.0, 3.0, 1.0)
suppression = st.slider("Suppression", 0.0, 1.0, 0.0)

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation"):

    # ✅ FIX 1: Scale-Free Network (Realistic)
    G = nx.barabasi_albert_graph(N, 3)

    centrality = nx.degree_centrality(G)

    # ✅ FIX 2: True Influencers (top nodes)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    influencers = [node for node, _ in sorted_nodes[:int(0.05*N)]]

    st.write("🌟 Influencers:", len(influencers))

    # Initial populations
    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []

    dt = 0.1

    for t in range(time_steps):

        # ✅ FIX 3: Influencer-driven spread
        influencer_boost = 1 + (len(influencers)/N)

        # Random factor (stochastic behavior)
        randomness = random.uniform(0.9, 1.1)

        # Growth equation improved
        dV = (alpha * S * (P/N) * boost * influencer_boost * randomness - beta * V) * dt
        dS = (gamma * V * (P/N) * randomness - delta * S) * dt

        # Apply suppression
        dV *= (1 - suppression)

        # Update
        V += dV
        S += dS
        P = N - (V + S)

        # ✅ FIX 4: Stability check
        V = max(0, min(V, N))
        S = max(0, min(S, N))
        P = max(0, min(P, N))

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    # -----------------------------
    # PEAK DETECTION
    # -----------------------------
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time {peak_time}")

    # -----------------------------
    # GRAPH
    # -----------------------------
    fig, ax = plt.subplots()

    ax.plot(np.array(V_list)/N, label="Viewers")
    ax.plot(np.array(S_list)/N, label="Sharers")
    ax.plot(np.array(P_list)/N, label="Passive")

    ax.axvline(x=peak_time, linestyle='--', label="Peak")

    ax.set_title("Viral Spread (Improved Model)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Proportion")
    ax.legend()

    st.pyplot(fig)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("""
### 📊 Interpretation

- Faster rise → strong influencer impact  
- Randomness → realistic viral uncertainty  
- Peak → maximum reach  
- Decline → audience saturation  
""")
