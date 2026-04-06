import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 TikTok Viral Spread Model (Network-Based)")

# -----------------------------
# THEORY
# -----------------------------
st.markdown("## 📘 Model Overview")

st.write("""
This model simulates viral spread using a real-world network:

- Users are connected in a scale-free network
- Sharers influence their neighbors
- Spread depends on connectivity and user behavior
""")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("🔧 Parameters")

N = st.sidebar.slider("Total Users (N)", 50, 500, 150)

beta = st.sidebar.slider("β (Share Probability)", 0.0, 1.0, 0.5)
gamma = st.sidebar.slider("γ (Passive Rate)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay)", 0.0, 1.0, 0.1)

T = st.sidebar.slider("Time Steps", 20, 200, 100)

initial_sharers = st.sidebar.slider("Initial Sharers", 1, 20, 5)

run = st.sidebar.button("▶ Run Simulation")

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate_network():
    G = nx.barabasi_albert_graph(N, 3)

    # 0 = viewer, 1 = sharer, 2 = passive
    state = {node: 0 for node in G.nodes()}

    # Initialize sharers
    initial = random.sample(list(G.nodes()), initial_sharers)
    for node in initial:
        state[node] = 1

    V, S, P = [], [], []

    for t in range(T):
        new_state = state.copy()

        for node in G.nodes():
            if state[node] == 1:
                for n in G.neighbors(node):
                    if state[n] == 0 and random.random() < beta:
                        new_state[n] = 1

                # Sharer becomes passive
                if random.random() < gamma:
                    new_state[node] = 2

        # Decay
        for node in G.nodes():
            if state[node] == 0 and random.random() < delta:
                new_state[node] = 2

        state = new_state

        V.append(list(state.values()).count(0))
        S.append(list(state.values()).count(1))
        P.append(list(state.values()).count(2))

    return V, S, P, G, state

# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    V, S, P, G, state = simulate_network()

    peak_views = max(V)
    peak_time = np.argmax(V)

    virality_score = (peak_views / N) * (1 / (peak_time + 1))

    # -----------------------------
    # RESULTS
    # -----------------------------
    st.subheader("📈 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Viewers", peak_views)
    col2.metric("Peak Time", peak_time)
    col3.metric("Virality Score", f"{virality_score:.3f}")

    # -----------------------------
    # INTERPRETATION (NEW 🔥)
    # -----------------------------
    st.subheader("📌 Interpretation")

    # Virality level
    if peak_views > 0.7 * N:
        st.success("🔥 Highly Viral: Video spreads to most users quickly.")
    elif peak_views > 0.4 * N:
        st.info("📈 Moderate Spread: Good reach but limited penetration.")
    else:
        st.warning("📉 Low Spread: Video fails to reach majority.")

    # Speed analysis
    if peak_time < T * 0.3:
        st.write("⚡ Fast Growth: Video goes viral quickly.")
    else:
        st.write("🐢 Slow Growth: Spread is gradual.")

    # Behavior analysis
    if beta > gamma:
        st.write("🚀 Strong sharing behavior dominates.")
    else:
        st.write("⚠️ Users lose interest quickly.")

    # Decay analysis
    if delta > 0.3:
        st.write("⏳ High decay → trend dies quickly.")
    else:
        st.write("📌 Content stays relevant longer.")

    # Network insight
    avg_degree = np.mean([deg for _, deg in G.degree()])
    st.write(f"🌐 Avg Network Degree: {avg_degree:.2f}")

    if avg_degree > 4:
        st.write("🔥 Dense network → faster spread.")
    else:
        st.write("📉 Sparse network → slower spread.")

    # -----------------------------
    # GRAPH 1
    # -----------------------------
    st.subheader("🔁 Sharers vs Passive")

    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(S, label="Sharers")
    ax1.plot(P, label="Passive")
    ax1.legend()
    st.pyplot(fig1)

    # -----------------------------
    # GRAPH 2
    # -----------------------------
    st.subheader("📊 Growth-Decay Graph")

    fig2, ax2 = plt.subplots(figsize=(5,3))
    ax2.plot(V, label="Viewers")
    ax2.plot(S, label="Sharers")
    ax2.plot(P, label="Passive")
    ax2.legend()
    st.pyplot(fig2)

    # -----------------------------
    # NETWORK GRAPH
    # -----------------------------
    st.subheader("🕸️ Network Spread")

    fig_net, ax_net = plt.subplots(figsize=(4,3))
    pos = nx.spring_layout(G, seed=42)

    colors = [
        "red" if state[n] == 1 else
        "gray" if state[n] == 2 else
        "blue"
        for n in G.nodes()
    ]

    nx.draw(G, pos, node_color=colors, node_size=40, ax=ax_net)
    st.pyplot(fig_net)
