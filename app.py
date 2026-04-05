import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📊 TikTok Viral Spread Model (Improved)")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.sidebar.header("🔧 Parameters")

N = st.sidebar.number_input("Total Users (N)", value=1000)
beta = st.sidebar.slider("β (Viewer → Sharer)", 0.0, 1.0, 0.3)
gamma = st.sidebar.slider("γ (Viewer → Passive)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay)", 0.0, 1.0, 0.1)
k = st.sidebar.slider("k (Network Influence)", 0.1, 2.0, 1.0)

V0 = st.sidebar.number_input("Initial Viewers", value=10)
S0 = st.sidebar.number_input("Initial Sharers", value=5)
P0 = st.sidebar.number_input("Initial Passive", value=0)

T = st.sidebar.slider("Time Steps", 20, 300, 100)

# Run Button
run = st.button("▶ Run Simulation")

# -----------------------------
# FUNCTION: SIMULATION
# -----------------------------
def simulate():
    # Create network
    G = nx.erdos_renyi_graph(N, 0.01)

    # Centrality
    centrality = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality.values()))

    # Effective influence
    k_eff = k * (1 + avg_centrality)

    # Initialize arrays
    V = np.zeros(T)
    S = np.zeros(T)
    P = np.zeros(T)

    V[0], S[0], P[0] = V0, S0, P0

    dt = 0.1   # smaller step → smoother graph

    # Simulation loop
    for t in range(1, T):
        dV = k_eff * S[t-1] * ((N - V[t-1]) / N) - delta * V[t-1]
        dS = beta * V[t-1] - gamma * S[t-1]
        dP = gamma * V[t-1]

        V[t] = V[t-1] + dV * dt
        S[t] = S[t-1] + dS * dt
        P[t] = P[t-1] + dP * dt

        # Prevent negative values
        V[t] = max(V[t], 0)
        S[t] = max(S[t], 0)
        P[t] = max(P[t], 0)

    return V, S, P, avg_centrality

# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    V, S, P, C = simulate()

    # Peak Analysis
    peak_views = np.max(V)
    peak_time = np.argmax(V)

    st.subheader("📈 Results")
    st.write(f"Peak Views: {peak_views:.2f}")
    st.write(f"Peak Time: {peak_time}")
    st.write(f"Network Centrality: {C:.4f}")

    # -----------------------------
    # GRAPHS (SMALL SIZE)
    # -----------------------------
    st.subheader("📉 Graphs")

    # Graph 1
    fig1, ax1 = plt.subplots(figsize=(4,3))
    ax1.plot(V)
    ax1.set_title("Viewers")
    st.pyplot(fig1)

    # Graph 2
    fig2, ax2 = plt.subplots(figsize=(4,3))
    ax2.plot(S, label="Sharers")
    ax2.plot(P, label="Passive")
    ax2.legend()
    ax2.set_title("Sharers & Passive")
    st.pyplot(fig2)

    # Graph 3 (Combined)
    fig3, ax3 = plt.subplots(figsize=(4,3))
    ax3.plot(V, label="Viewers")
    ax3.plot(S, label="Sharers")
    ax3.plot(P, label="Passive")
    ax3.legend()
    ax3.set_title("Combined")
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
        st.write("🌐 Influencers (central nodes) significantly boost spread.")

    # -----------------------------
    # NETWORK VISUAL (SMALL)
    # -----------------------------
    st.subheader("🕸️ Network Structure")

    G = nx.erdos_renyi_graph(100, 0.05)

    fig_net, ax_net = plt.subplots(figsize=(4,3))
    nx.draw(G, node_size=20, ax=ax_net)
    st.pyplot(fig_net)
