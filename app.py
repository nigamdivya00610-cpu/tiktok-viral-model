import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="centered")
st.title("📊 TikTok Viral Spread Model (Network-Based)")

# -----------------------------
# THEORY
# -----------------------------
st.markdown("## 📘 Model Overview")

st.write("""
This model simulates viral spread using a real network:

- Users are connected in a graph
- Sharers influence their neighbors
- Spread depends on network structure (not random global spread)
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
# SIMULATION FUNCTION (NETWORK BASED)
# -----------------------------
def simulate_network():
    # Scale-free network (realistic social network)
    G = nx.barabasi_albert_graph(N, 3)

    # Node states: 0 = viewer, 1 = sharer, 2 = passive
    state = {node: 0 for node in G.nodes()}

    # Initialize sharers
    initial = random.sample(list(G.nodes()), initial_sharers)
    for node in initial:
        state[node] = 1

    V, S, P = [], [], []

    for t in range(T):
        new_state = state.copy()

        for node in G.nodes():
            if state[node] == 1:  # sharer
                neighbors = list(G.neighbors(node))

                for n in neighbors:
                    if state[n] == 0:  # viewer
                        if random.random() < beta:
                            new_state[n] = 1

                # Sharer becomes passive
                if random.random() < gamma:
                    new_state[node] = 2

        # Decay: viewers lose interest
        for node in G.nodes():
            if state[node] == 0:
                if random.random() < delta:
                    new_state[node] = 2

        state = new_state

        # Count states
        v = list(state.values()).count(0)
        s = list(state.values()).count(1)
        p = list(state.values()).count(2)

        V.append(v)
        S.append(s)
        P.append(p)

    return V, S, P, G, state

# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    V, S, P, G, state = simulate_network()

    peak_views = max(V)
    peak_time = np.argmax(V)

    # -----------------------------
    # RESULTS + INTERPRETATION
    # -----------------------------
    st.subheader("📈 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Viewers", peak_views)
    col2.metric("Peak Time", peak_time)
    col3.metric("Final Sharers", S[-1])

    st.markdown("### 📌 Interpretation")

    if peak_views > 0.7 * N:
        st.success("🔥 Highly Viral")
    elif peak_views > 0.4 * N:
        st.info("📈 Moderate Spread")
    else:
        st.warning("📉 Low Spread")

    if beta > gamma:
        st.write("🚀 Strong sharing behavior")
    else:
        st.write("⚠️ Users quickly become passive")

    if delta > 0.3:
        st.write("⏳ High decay rate")

    # -----------------------------
    # GRAPH 1: Sharers vs Passive
    # -----------------------------
    st.subheader("🔁 Sharers vs Passive")

    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(S, label="Sharers")
    ax1.plot(P, label="Passive")
    ax1.legend()
    ax1.set_title("Sharers vs Passive")
    st.pyplot(fig1)

    # -----------------------------
    # GRAPH 2: Growth-Decay
    # -----------------------------
    st.subheader("📊 Growth-Decay Graph")

    fig2, ax2 = plt.subplots(figsize=(5,3))
    ax2.plot(V, label="Viewers")
    ax2.plot(S, label="Sharers")
    ax2.plot(P, label="Passive")
    ax2.legend()
    ax2.set_title("Spread Dynamics")
    st.pyplot(fig2)

    # -----------------------------
    # NETWORK VISUALIZATION
    # -----------------------------
    st.subheader("🕸️ Network Spread")

    fig_net, ax_net = plt.subplots(figsize=(4,3))
    pos = nx.spring_layout(G, seed=42)

    colors = []
    for node in G.nodes():
        if state[node] == 1:
            colors.append("red")      # sharer
        elif state[node] == 2:
            colors.append("gray")     # passive
        else:
            colors.append("blue")     # viewer

    nx.draw(G, pos, node_color=colors, node_size=40, ax=ax_net)
    st.pyplot(fig_net)
