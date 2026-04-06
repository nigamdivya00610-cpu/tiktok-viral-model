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
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("🔧 Parameters")

N = st.sidebar.slider("Total Users (N)", 10, 100, 13)
beta = st.sidebar.slider("β (Share Probability)", 0.0, 1.0, 0.5)
gamma = st.sidebar.slider("γ (Passive Rate)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay)", 0.0, 1.0, 0.1)

T = st.sidebar.slider("Time Steps", 20, 200, 100)
initial_sharers = st.sidebar.slider("Initial Sharers", 1, 5, 2)

run = st.sidebar.button("▶ Run Simulation")

# -----------------------------
# CUSTOM NETWORK (LIKE IMAGE)
# -----------------------------
def create_custom_network():
    G = nx.Graph()

    # Fixed nodes (1–13)
    nodes = list(range(1, 14))
    G.add_nodes_from(nodes)

    # Fixed edges (similar structure)
    edges = [
        (1,2),(2,11),(2,9),(2,4),
        (4,6),(6,7),(7,5),(7,13),
        (6,3),(6,12),(6,8),(8,10)
    ]
    G.add_edges_from(edges)

    return G

# -----------------------------
# SIMULATION
# -----------------------------
def simulate_network():
    G = create_custom_network()

    state = {node: 0 for node in G.nodes()}  # 0 viewer,1 sharer,2 passive

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

    return V, S, P, G, state

# -----------------------------
# RUN
# -----------------------------
if run:
    V, S, P, G, state = simulate_network()

    peak_views = max(V)
    peak_time = np.argmax(V)
    final_sharers = S[-1]

    virality_score = (peak_views / len(G.nodes())) * beta * (1 - gamma)
    spread_speed = peak_views / (peak_time + 1)

    # -----------------------------
    # METRICS
    # -----------------------------
    st.subheader("📈 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", len(G.nodes()))
    col2.metric("Peak Viewers", peak_views)
    col3.metric("Peak Time", peak_time)
    col4.metric("Virality Score", f"{virality_score:.2f}")

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("## 📌 Interpretation")

    if beta > gamma:
        st.success("🚀 Strong sharing → viral growth likely")
    else:
        st.warning("⚠️ High drop-off → weak spread")

    if delta > 0.3:
        st.warning("⏳ High decay → short trend")

    if peak_views > 0.7 * len(G.nodes()):
        st.success("🔥 Highly Viral")
    else:
        st.info("📉 Limited Spread")

    # -----------------------------
    # SINGLE GRAPH
    # -----------------------------
    st.subheader("📊 Spread Dynamics")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(V, label="Viewers")
    ax.plot(S, label="Sharers")
    ax.plot(P, label="Passive")
    ax.legend()
    ax.set_title("Growth-Decay Curve")
    st.pyplot(fig)

    # -----------------------------
    # NETWORK VISUALIZATION
    # -----------------------------
    st.subheader("🕸️ Network Structure")

    fig_net, ax_net = plt.subplots(figsize=(6,4))

    pos = nx.spring_layout(G, seed=42)

    colors = []
    for node in G.nodes():
        if state[node] == 1:
            colors.append("red")
        elif state[node] == 2:
            colors.append("gray")
        else:
            colors.append("lightgreen")

    nx.draw(
        G, pos,
        with_labels=True,   # ✅ show numbers
        node_color=colors,
        node_size=800,
        font_size=10,
        ax=ax_net
    )

    st.pyplot(fig_net)

    # -----------------------------
    # STRATEGY
    # -----------------------------
    st.markdown("## 🎯 Strategy Based on Model")

    st.write("""
- Increase β → Boost sharing  
- Reduce γ → Improve retention  
- Reduce δ → Slow decay  
- Target key nodes → Faster spread  
""")
