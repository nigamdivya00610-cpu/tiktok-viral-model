import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 TikTok Viral Spread Model")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("🔧 Parameters")

N = st.sidebar.number_input("Total Users (N)", value=100)
beta = st.sidebar.slider("β (Viewer → Sharer)", 0.0, 1.0, 0.6)
gamma = st.sidebar.slider("γ (Sharer → Passive)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay)", 0.0, 1.0, 0.1)
k = st.sidebar.slider("k (Network Influence)", 0.1, 2.0, 1.0)

V0 = st.sidebar.number_input("Initial Viewers", value=10)
S0 = st.sidebar.number_input("Initial Sharers", value=5)
P0 = st.sidebar.number_input("Initial Passive", value=0)

T = st.sidebar.slider("Time Steps", 20, 200, 100)

run = st.sidebar.button("▶ Run Simulation")

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate():
    G = nx.erdos_renyi_graph(N, 0.05)

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
        dP = gamma * S[t-1]

        V[t] = max(V[t-1] + dV * dt, 0)
        S[t] = max(S[t-1] + dS * dt, 0)
        P[t] = max(P[t-1] + dP * dt, 0)

    return V, S, P, avg_centrality

# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    V, S, P, C = simulate()

    # -----------------------------
    # DATAFRAME FOR CLEAN GRAPH
    # -----------------------------
    df = pd.DataFrame({
        "Viewers": V,
        "Sharers": S,
        "Passive": P
    })

    # -----------------------------
    # RESULTS
    # -----------------------------
    st.subheader("📈 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Views", f"{np.max(V):.2f}")
    col2.metric("Peak Time", int(np.argmax(V)))
    col3.metric("Centrality", f"{C:.4f}")

    # -----------------------------
    # INTERACTIVE FILTER
    # -----------------------------
    st.subheader("🎛 Select Data")

    options = st.multiselect(
        "Choose lines to display",
        ["Viewers", "Sharers", "Passive"],
        default=["Viewers", "Sharers"]
    )

    st.line_chart(df[options])

    # -----------------------------
    # MATPLOTLIB GRAPHS (FIXED SIZE)
    # -----------------------------
    st.subheader("📊 Detailed Graphs")

    col1, col2 = st.columns(2)

    # Viewers
    with col1:
        fig1, ax1 = plt.subplots(figsize=(6,3))
        ax1.plot(V, linewidth=2)
        ax1.set_title("Viewers")
        ax1.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig1)

    # Sharers + Passive
    with col2:
        fig2, ax2 = plt.subplots(figsize=(6,3))
        ax2.plot(S, label="Sharers", linewidth=2)
        ax2.plot(P, label="Passive", linewidth=2)
        ax2.legend()
        ax2.set_title("Sharers & Passive")
        ax2.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig2)

    # Combined Graph
    st.subheader("📈 Combined Graph")

    fig3, ax3 = plt.subplots(figsize=(8,4))
    ax3.plot(V, label="Viewers", linewidth=2)
    ax3.plot(S, label="Sharers", linewidth=2)
    ax3.plot(P, label="Passive", linewidth=2)

    ax3.set_title("Performance Over Time")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Users")
    ax3.legend()
    ax3.grid(True, linestyle="--", alpha=0.6)

    st.pyplot(fig3)

    # -----------------------------
    # NETWORK GRAPH
    # -----------------------------
    st.subheader("🕸️ Network Structure")

    G = nx.erdos_renyi_graph(50, 0.05)

    fig_net, ax_net = plt.subplots(figsize=(6,4))
    nx.draw(G, node_size=30, ax=ax_net)
    st.pyplot(fig_net)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.subheader("📌 Interpretation")

    if np.max(V) > 0.7 * N:
        st.success("🔥 Highly Viral")
    elif np.max(V) > 0.4 * N:
        st.info("📈 Moderate Viral")
    else:
        st.warning("📉 Low Viral Spread")

    if beta > gamma:
        st.write("🚀 Strong sharing behavior")
    else:
        st.write("⚠️ Users turning passive quickly")

    if delta > 0.3:
        st.write("⏳ High decay → trend dies fast")

    if C > 0.05:
        st.write("🌐 Influencers boosting spread")
