import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 TikTok Viral Spread Model")

# -----------------------------
# THEORY SECTION
# -----------------------------
st.markdown("## 📘 Model Overview")

st.write("""
This model simulates how a TikTok video spreads using:
- Mathematical growth-decay dynamics
- Real social network structure
- User interaction behavior
""")

st.markdown("### 🧠 Mathematical Model")

st.latex(r"\frac{dV}{dt} = \beta S \cdot \frac{(N - V)}{N} - \delta V")
st.latex(r"\frac{dS}{dt} = \beta V - \gamma S")
st.latex(r"\frac{dP}{dt} = \gamma V")

st.write("""
- β → Share probability  
- γ → Passive rate  
- δ → Decay rate  
- N → Total users  
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
def simulate_network(N, beta, gamma, delta, T, initial_sharers):
    G = nx.barabasi_albert_graph(N, 3)

    # 0=viewer, 1=sharer, 2=passive
    state = {node: 0 for node in G.nodes()}

    # Initialize sharers
    initial_nodes = random.sample(list(G.nodes()), initial_sharers)
    for node in initial_nodes:
        state[node] = 1

    V, S, P = [], [], []

    for t in range(T):
        new_state = state.copy()

        for node in G.nodes():
            if state[node] == 1:
                for neighbor in G.neighbors(node):
                    if state[neighbor] == 0 and random.random() < beta:
                        new_state[neighbor] = 1

                if random.random() < gamma:
                    new_state[node] = 2

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
    V, S, P, G, state = simulate_network(N, beta, gamma, delta, T, initial_sharers)

    # Metrics
    peak_views = max(V)
    peak_time = int(np.argmax(V))
    final_sharers = S[-1]

    virality_score = (peak_views / N) * beta * (1 - gamma)
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
    # INTERPRETATION
    # -----------------------------
    st.markdown("## 📌 Interpretation")

    # Sharing dynamics
    if beta > gamma:
        st.success("🚀 Strong sharing dominates (β > γ)")
    elif gamma > beta:
        st.warning("⚠️ Users become passive quickly (γ > β)")
    else:
        st.info("⚖️ Balanced sharing and drop-off")

    # Decay
    if delta > 0.3:
        st.warning("⏳ High decay → trend fades quickly")
    elif delta < 0.1:
        st.success("🌱 Low decay → content stays relevant")
    else:
        st.info("📉 Moderate decay")

    # Virality
    if peak_views > 0.7 * N:
        st.success("🔥 Highly Viral")
    elif peak_views > 0.4 * N:
        st.info("📈 Moderate Spread")
    else:
        st.error("📉 Low Spread")

    # Speed
    if spread_speed > 5:
        st.success("⚡ Fast Spread")
    elif spread_speed > 2:
        st.info("🚶 Moderate Speed")
    else:
        st.warning("🐢 Slow Spread")

    # -----------------------------
    # GRAPHS
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
    st.subheader("🕸️ Network State")

    fig_net, ax_net = plt.subplots(figsize=(6,4))
    pos = nx.spring_layout(G, seed=42)

    colors = [
        "red" if state[n] == 1 else
        "gray" if state[n] == 2 else
        "blue"
        for n in G.nodes()
    ]

    nx.draw(G, pos, node_color=colors, node_size=50, ax=ax_net)
    st.pyplot(fig_net)

    # -----------------------------
    # STRATEGY
    # -----------------------------
    st.markdown("## 🎯 Strategy")

    st.write("""
- Increase β → More sharing → faster spread  
- Reduce γ → Better retention  
- Reduce δ → Slower decay  
- Target influencers → maximize reach  
""")
