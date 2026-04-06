import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -----------------------------
# PAGE CONFIG (WIDE)
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 TikTok Viral Spread Model (Network-Based)")

# -----------------------------
# THEORY SECTION
# -----------------------------
st.markdown("## 📘 Model Overview")

st.write("""
This model simulates how a TikTok video spreads through a **real social network**.

### 🔹 Key Concepts:
- Users are connected via a **scale-free network**
- Influencers (high-degree nodes) drive spread
- Sharers influence their neighbors
- Content spreads locally (not globally)

### 🔹 User Types:
- 👀 Viewer → Can watch content
- 🔁 Sharer → Actively spreads video
- 😐 Passive → Loses interest
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

    state = {node: 0 for node in G.nodes()}

    initial = random.sample(list(G.nodes()), initial_sharers)
    for node in initial:
        state[node] = 1

    V, S, P = [], [], []

    for t in range(T):
        new_state = state.copy()

        for node in G.nodes():
            if state[node] == 1:
                neighbors = list(G.neighbors(node))

                for n in neighbors:
                    if state[n] == 0:
                        if random.random() < beta:
                            new_state[n] = 1

                if random.random() < gamma:
                    new_state[node] = 2

        for node in G.nodes():
            if state[node] == 0:
                if random.random() < delta:
                    new_state[node] = 2

        state = new_state

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
    final_sharers = S[-1]

    # Virality score
    virality_score = (peak_views / N) * beta * (1 - gamma)

    # Spread speed
    spread_speed = peak_views / (peak_time + 1)

    # -----------------------------
    # RESULTS
    # -----------------------------
    st.subheader("📈 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Peak Viewers", peak_views)
    col2.metric("Peak Time", peak_time)
    col3.metric("Final Sharers", final_sharers)
    col4.metric("Virality Score", f"{virality_score:.2f}")

    # -----------------------------
    # INTERPRETATION (SMART)
    # -----------------------------
    st.markdown("## 📌 Detailed Interpretation")

    if peak_views > 0.7 * N:
        st.success("🔥 The video went highly viral and reached most of the network.")
    elif peak_views > 0.4 * N:
        st.info("📈 Moderate virality with decent reach.")
    else:
        st.warning("📉 Low virality — content failed to spread widely.")

    if spread_speed > 5:
        st.write("⚡ Fast spreading — strong early momentum.")
    else:
        st.write("🐢 Slow spread — weak initial push.")

    if beta > 0.6:
        st.write("🚀 High shareability — content is engaging and relatable.")
    elif beta < 0.3:
        st.write("⚠️ Low shareability — users are not motivated to share.")

    if gamma > 0.4:
        st.write("😐 Users quickly lose interest → retention problem.")

    if delta > 0.3:
        st.write("⏳ High decay → trend dies quickly.")

    # Network insight
    avg_degree = np.mean([d for n, d in G.degree()])
    if avg_degree > 5:
        st.write("🌐 Dense network → faster information spread.")
    else:
        st.write("🕸️ Sparse network → slower spread.")

    # -----------------------------
    # LAYOUT: GRAPHS SIDE BY SIDE
    # -----------------------------
    st.subheader("📊 Spread Dynamics")

    colA, colB = st.columns(2)

    with colA:
        fig1, ax1 = plt.subplots(figsize=(6,4))
        ax1.plot(S, label="Sharers")
        ax1.plot(P, label="Passive")
        ax1.set_title("Sharers vs Passive")
        ax1.legend()
        st.pyplot(fig1)

    with colB:
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.plot(V, label="Viewers")
        ax2.plot(S, label="Sharers")
        ax2.plot(P, label="Passive")
        ax2.set_title("Growth-Decay")
        ax2.legend()
        st.pyplot(fig2)

    # -----------------------------
    # NETWORK VISUALIZATION
    # -----------------------------
    st.subheader("🕸️ Final Network State")

    fig_net, ax_net = plt.subplots(figsize=(6,4))
    pos = nx.spring_layout(G, seed=42)

    colors = []
    for node in G.nodes():
        if state[node] == 1:
            colors.append("red")
        elif state[node] == 2:
            colors.append("gray")
        else:
            colors.append("blue")

    nx.draw(G, pos, node_color=colors, node_size=50, ax=ax_net)
    st.pyplot(fig_net)
