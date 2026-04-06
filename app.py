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

    edges = [
        (1,2),(2,11),(2,9),(1,2),
        (4,9),(4,6),
        (6,7),(7,5),(7,13),
        (6,12),(6,3),
        (6,8),(8,10)
    ]

    G.add_edges_from(edges)
    return G

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate_network():
    G = create_custom_network()

    state = {node: 0 for node in G.nodes()}  # 0=viewer,1=sharer,2=passive

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
    V, S, P, G, state = simulate_network()

    peak_views = max(V)
    peak_time = int(np.argmax(V))
    final_sharers = S[-1]

    virality_score = (peak_views / len(G.nodes())) * beta * (1 - gamma)
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

    if beta > gamma:
        st.success("🚀 Strong sharing dominates (β > γ)")
    elif gamma > beta:
        st.warning("⚠️ Users become passive quickly (γ > β)")
    else:
        st.info("⚖️ Balanced sharing")

    if delta > 0.3:
        st.warning("⏳ High decay")
    else:
        st.info("📉 Controlled decay")

    if peak_views > 0.7 * len(G.nodes()):
        st.success("🔥 Highly Viral")
    else:
        st.info("📊 Moderate / Low Spread")

    # -----------------------------
    # SINGLE GRAPH
    # -----------------------------
    st.subheader("📊 Spread Dynamics")

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(V, label="Viewers")
    ax.plot(S, label="Sharers")
    ax.plot(P, label="Passive")
    ax.set_title("Growth-Decay Dynamics")
    ax.legend()
    st.pyplot(fig)

    # -----------------------------
    # NETWORK VISUALIZATION (WITH NUMBERS)
    # -----------------------------
    st.subheader("🕸️ Network Structure")

    fig_net, ax_net = plt.subplots(figsize=(6,4))

    pos = nx.spring_layout(G, seed=42)

    colors = [
        "red" if state[n] == 1 else
        "gray" if state[n] == 2 else
        "green"
        for n in G.nodes()
    ]

    nx.draw(
        G, pos,
        node_color=colors,
        node_size=800,
        with_labels=True,   # 🔥 THIS SHOWS NUMBERS
        font_size=10,
        ax=ax_net
    )

    st.pyplot(fig_net)

    # -----------------------------
    # STRATEGY
    # -----------------------------
    st.markdown("## 🎯 Strategy")

    st.write("""
- Increase β → More sharing → faster spread  
- Reduce γ → Better retention  
- Reduce δ → Slower decay  
- Use influencers → increases effective spread rate
""")
