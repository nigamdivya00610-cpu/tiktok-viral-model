import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 TikTok Viral Spread Model)

# -----------------------------
# THEORY + FORMULAS
# -----------------------------
st.markdown("## 📘 Model Overview")

st.write("""
This model combines **mathematical growth-decay dynamics** with a **real social network**.

- Spread happens through connections (neighbors)
- Influencers accelerate growth
- Content fades over time (decay)
""")

st.markdown("### 🧠 Mathematical Model")

st.latex(r"\frac{dV}{dt} = \beta S \cdot \frac{(N - V)}{N} - \delta V")
st.latex(r"\frac{dS}{dt} = \beta V - \gamma S")
st.latex(r"\frac{dP}{dt} = \gamma V")

st.write("""
### 🔍 Meaning:
- β → Share probability  
- γ → Users becoming passive  
- δ → Content decay  
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
def simulate_network():
    G = nx.barabasi_albert_graph(N, 3)

    state = {node: 0 for node in G.nodes()}  # 0=viewer,1=sharer,2=passive

    initial = random.sample(list(G.nodes()), initial_sharers)
    for node in initial:
        state[node] = 1

    V, S, P = [], [], []

    for t in range(T):
        new_state = state.copy()

        for node in G.nodes():
            if state[node] == 1:
                for n in G.neighbors(node):
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

        V.append(list(state.values()).count(0))
        S.append(list(state.values()).count(1))
        P.append(list(state.values()).count(2))

    return V, S, P, G, state

# -----------------------------
# RUN
# -----------------------------
if run:
    V, S, P, G, state = simulate_network()

    peak_views = max(V)
    peak_time = np.argmax(V)
    final_sharers = S[-1]

    # Derived metrics
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
    # INTERPRETATION LINKED TO FORMULAS
    # -----------------------------
    st.markdown("## 📌 Interpretation (Based on Model Equations)")

    if beta > gamma:
        st.write("🚀 From dS/dt = βV - γS → Growth dominates → More sharers created")

    if gamma > beta:
        st.write("⚠️ From dS/dt → Users become passive faster than sharing")

    if delta > 0.3:
        st.write("⏳ From dV/dt → High decay reduces viewers quickly")

    if peak_views > 0.7 * N:
        st.success("🔥 Strong growth term in dV/dt → Viral spread achieved")
    elif peak_views < 0.4 * N:
        st.warning("📉 Weak growth → Spread limited")

    if spread_speed > 5:
        st.write("⚡ High initial dV/dt → Rapid viral growth")

    # -----------------------------
    # GRAPHS
    # -----------------------------
    st.subheader("📊 Spread Dynamics")

    colA, colB = st.columns(2)

    with colA:
        fig1, ax1 = plt.subplots(figsize=(6,4))
        ax1.plot(S, label="Sharers")
        ax1.plot(P, label="Passive")
        ax1.legend()
        ax1.set_title("Sharers vs Passive")
        st.pyplot(fig1)

    with colB:
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.plot(V, label="Viewers")
        ax2.plot(S, label="Sharers")
        ax2.plot(P, label="Passive")
        ax2.legend()
        ax2.set_title("Growth-Decay")
        st.pyplot(fig2)

    # -----------------------------
    # NETWORK VISUALIZATION
    # -----------------------------
    st.subheader("🕸️ Network State")

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

    # -----------------------------
    # STRATEGY (CONNECTED TO FORMULAS)
    # -----------------------------
    st.markdown("## 🎯 Strategy Based on Model")

    st.write("""
- Increase β → Boost sharing → increases dS/dt
- Reduce γ → Retain users → fewer passive users
- Reduce δ → Slow decay → sustain dV/dt
- Use influencers → increases effective spread rate
""")
