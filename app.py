import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")
st.title("TikTok Viral Spread Model")

# -----------------------------
# THEORY
# -----------------------------
st.markdown("## Model Overview")
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
### Meaning:
- β → Share probability  
- γ → Users becoming passive  
- δ → Content decay  
- N → Total users  
""")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("🔧 Parameters")

beta = st.sidebar.slider("β (Share Probability)", 0.0, 1.0, 0.5)
gamma = st.sidebar.slider("γ (Passive Rate)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay)", 0.0, 1.0, 0.1)

T = st.sidebar.slider("Time Steps", 20, 200, 100)
initial_sharers = st.sidebar.slider("Initial Sharers", 1, 5, 2)

run = st.sidebar.button("▶ Run Simulation")

# -----------------------------
# CUSTOM NETWORK (LIKE IMAGE)
# -----------------------------
def create_fixed_network():
    G = nx.Graph()

    edges = [
        (1,2),(2,11),(2,9),(2,4),
        (4,6),(6,7),(7,5),(7,13),
        (6,12),(6,3),(6,8),(8,10)
    ]

    G.add_edges_from(edges)
    return G

# -----------------------------
# SIMULATION
# -----------------------------
def simulate_network(G):
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
                    if state[n] == 0 and random.random() < beta:
                        new_state[n] = 1

                if random.random() < gamma:
                    new_state[node] = 2

        for node in G.nodes():
            if state[node] == 0 and random.random() < delta:
                new_state[node] = 2

        state = new_state

        V.append(list(state.values()).count(0))
        S.append(list(state.values()).count(1))
        P.append(list(state.values()).count(2))

    return V, S, P, state

# -----------------------------
# RUN
# -----------------------------
if run:
    G = create_fixed_network()
    V, S, P, state = simulate_network(G)

    N = len(G.nodes())
    peak_views = max(V)
    peak_time = np.argmax(V)
    final_sharers = S[-1]

    virality_score = (peak_views / N) * beta * (1 - gamma)
    spread_speed = peak_views / (peak_time + 1)

    # -----------------------------
    # METRICS
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
    st.markdown("## 📌 Interpretation (Based on Model Equations)")

    if beta > gamma:
        st.success("🚀 Strong sharing dominates (β > γ)")
    elif gamma > beta:
        st.warning("⚠️ Users become passive faster (γ > β)")
    else:
        st.info("⚖️ Balanced behavior")

    if delta > 0.3:
        st.warning("⏳ High decay → content fades quickly")

    if peak_views > 0.7 * N:
        st.success("🔥 Highly Viral")
    elif peak_views < 0.4 * N:
        st.warning("📉 Low Spread")

    if spread_speed > 5:
        st.success("⚡ Fast Spread")

    # -----------------------------
    # SINGLE GRAPH
    # -----------------------------
    st.subheader("📊 Spread Dynamics")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(V, label="Viewers")
    ax.plot(S, label="Sharers")
    ax.plot(P, label="Passive")
    ax.set_title("Growth-Decay")
    ax.legend()
    st.pyplot(fig)

    # -----------------------------
    # CUSTOM NETWORK VISUALIZATION
    # -----------------------------
    st.subheader("🕸️ Network Structure")

    pos = nx.spring_layout(G, seed=42)

    colors = []
    for node in G.nodes():
        if state[node] == 1:
            colors.append("purple")   # sharer
        elif state[node] == 2:
            colors.append("green")    # passive
        else:
            colors.append("yellow")   # viewer

    fig_net, ax_net = plt.subplots(figsize=(6,4))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, ax=ax_net)
    st.pyplot(fig_net)

    # -----------------------------
    # STRATEGY
    # -----------------------------
    st.markdown("## 🎯 Strategy Based on Model")

    st.write("""
- Increase β → Boost sharing → increases dS/dt
- Reduce γ → Retain users → fewer passive users
- Reduce δ → Slow decay → sustain dV/dt
- Use influencers → increases effective spread rate
""")
