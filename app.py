import streamlit as st
st.set_page_config(layout="wide") 
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📊 TikTok Viral Spread Model")

# -----------------------------
# THEORY SECTION (NEW)
# -----------------------------
st.markdown("## 📘 Model Overview")

st.write("""
This model simulates how a TikTok video spreads in a social network using:

### 🔹 Growth-Decay Model
- Viewers (V) increase when sharers promote content
- Viewers decrease due to content fading (decay)

### 🔹 Network Structure
- Users are connected in a graph (network)
- Influence depends on **central users (influencers)**

### 🔹 User Types
- 👀 Viewers: Watching content
- 🔁 Sharers: Actively spreading
- 😐 Passive: Lose interest and stop sharing
""")

st.markdown("## 🧠 Model Equations (Conceptual)")
st.latex(r"dV/dt = k \cdot S \cdot (N - V)/N - \delta V")
st.latex(r"dS/dt = \beta V - \gamma S")
st.latex(r"dP/dt = \gamma V")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.sidebar.header("🔧 Parameters")

N = st.sidebar.number_input("Total Users (N)", value=10)
beta = st.sidebar.slider("β (Viewer → Sharer)", 0.0, 1.0, 0.9)
gamma = st.sidebar.slider("γ (Viewer → Passive)", 0.0, 1.0, 0.1)
delta = st.sidebar.slider("δ (Decay)", 0.0, 1.0, 0.8)
k = st.sidebar.slider("k (Network Influence)", 0.1, 2.0, 1.0)

V0 = st.sidebar.number_input("Initial Viewers", value=20)
S0 = st.sidebar.number_input("Initial Sharers", value=15)
P0 = st.sidebar.number_input("Initial Passive", value=0)

T = st.sidebar.slider("Time Steps", 20, 300, 100)

run = st.button("▶ Run Simulation")

# -----------------------------
# FUNCTION: SIMULATION
# -----------------------------
def simulate():
    G = nx.erdos_renyi_graph(N, 0.01)

    centrality = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality.values()))

    k_eff = k * (1 + avg_centrality)

    V = np.zeros(T)
    S = np.zeros(T)
    P = np.zeros(T)

    V[0], S[0], P[0] = V0, S0, P0

    dt = 0.1

    for t in range(1, T):
        dV = k_eff * S[t-1] * ((N - V[t-1]) / N) - delta * V[t-1]
        dS = beta * V[t-1] - gamma * S[t-1]
        dP = gamma * V[t-1]

        V[t] = max(V[t-1] + dV * dt, 0)
        S[t] = max(S[t-1] + dS * dt, 0)
        P[t] = max(P[t-1] + dP * dt, 0)

    return V, S, P, avg_centrality

# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    V, S, P, C = simulate()

    peak_views = np.max(V)
    peak_time = np.argmax(V)

    st.subheader("📈 Results")
    st.write(f"Peak Views: {peak_views:.2f}")
    st.write(f"Peak Time: {peak_time}")
    st.write(f"Network Centrality: {C:.4f}")

    # -----------------------------
    # GRAPHS
    # -----------------------------
    st.subheader("📉 Graphs")
    
    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(V)
    ax1.set_title("Viewers")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.plot(S, label="Sharers")
    ax2.plot(P, label="Passive")
    ax2.legend()
    ax2.set_title("Sharers & Passive")
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots(figsize=(6,4))
    ax3.plot(V, label="Viewers")
    ax3.plot(S, label="Sharers")
    ax3.plot(P, label="Passive")
    ax3.legend()
    ax3.set_title("Growth-Decay Graph")
    st.pyplot(fig3)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.subheader("📌 Interpretation")

    if peak_views > 0.7 * N:
        st.write("🔥 Highly viral: Video spreads across most of the network.")
    elif peak_views > 0.4 * N:
        st.write("📈 Moderate virality: Good engagement but limited reach.")
    else:
        st.write("📉 Low virality: Content fails to spread widely.")

    if beta > gamma:
        st.write("🚀 Strong sharing behavior driving growth.")
    else:
        st.write("⚠️ Users are becoming passive quickly.")

    if delta > 0.3:
        st.write("⏳ High decay → trend dies quickly.")

    if C > 0.01:
        st.write("🌐 Influencers significantly boost spread.")

    # -----------------------------
    # NETWORK STRUCTURE (EXPLAINED)
    # -----------------------------
    st.subheader("🕸️ Network Structure")

    st.write("""
- Each node = a user
- Each edge = connection (followers/friends)
- Central nodes = influencers
- Dense network → faster spread
- Sparse network → slower spread
""")

    G = nx.erdos_renyi_graph(100, 0.05)
    fig_net, ax_net = plt.subplots(figsize=(4,3))
    nx.draw(G, node_size=20, ax=ax_net)
    st.pyplot(fig_net)

    # -----------------------------
    # INTERVENTION STRATEGIES (NEW)
    # -----------------------------
    st.subheader("🎯 How to Make Video Go Viral")

    st.write("""
### 🚀 Increase Virality
- Increase β → Make content more shareable (trendy, emotional, relatable)
- Target influencers (high centrality nodes)
- Improve network connectivity (hashtags, collaborations)

### ⚠️ Reduce Drop-off
- Reduce γ → Keep users engaged longer
- Hook viewers in first 3 seconds

### ⏳ Control Decay
- Lower δ → Post consistently
- Use trending sounds to stay relevant

### 🌐 Network Strategy
- Seed video with influencers first
- Use clustered communities for rapid spread
""")
