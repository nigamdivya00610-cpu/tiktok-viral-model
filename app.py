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
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("🔧 Parameters")

N = st.sidebar.slider("Total Users (N)", 50, 500, 150)
beta = st.sidebar.slider("β (Share Probability)", 0.0, 1.0, 0.5)
gamma = st.sidebar.slider("γ (Passive Rate)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay Rate)", 0.0, 1.0, 0.1)

T = st.sidebar.slider("Time Steps", 20, 200, 100)
initial_sharers = st.sidebar.slider("Initial Sharers", 1, 20, 5)

run = st.sidebar.button("▶ Run Simulation")

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate_network():
    # Create scale-free network (real social network)
    G = nx.barabasi_albert_graph(N, 3)

    # Node states:
    # 0 = Viewer, 1 = Sharer, 2 = Passive
    state = {node: 0 for node in G.nodes()}

    # Initialize sharers
    initial = random.sample(list(G.nodes()), initial_sharers)
    for node in initial:
        state[node] = 1

    V, S, P = [], [], []

    for t in range(T):
        new_state = state.copy()

        for node in G.nodes():

            # -----------------------------
            # Sharer spreads to neighbors
            # -----------------------------
            if state[node] == 1:
                for neighbor in G.neighbors(node):
                    if state[neighbor] == 0:
                        if random.random() < beta:
                            new_state[neighbor] = 1

                # Sharer becomes passive
                if random.random() < gamma:
                    new_state[node] = 2

        # -----------------------------
        # Decay: viewers lose interest
        # -----------------------------
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

    return V, S, P

# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    V, S, P = simulate_network()

    peak_views = max(V)
    peak_time = np.argmax(V)
    final_sharers = S[-1]

    # -----------------------------
    # RESULTS
    # -----------------------------
    st.subheader("📈 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Viewers", peak_views)
    col2.metric("Peak Time", peak_time)
    col3.metric("Final Sharers", final_sharers)

    # -----------------------------
    # INTERPRETATION (CLEAN)
    # -----------------------------
    st.markdown("### 📌 Interpretation")

    # Virality level
    if peak_views > 0.7 * N:
        st.success("🔥 Highly Viral: Content spreads to most of the network.")
    elif peak_views > 0.4 * N:
        st.info("📈 Moderate Spread: Good engagement but limited reach.")
    else:
        st.warning("📉 Low Spread: Video fails to spread widely.")

    # Sharing vs passive behavior
    if beta > gamma:
        st.write("🚀 Strong sharing behavior → Users actively spread the content.")
    else:
        st.write("⚠️ Users become passive quickly → Weak viral potential.")

    # Decay effect
    if delta > 0.3:
        st.write("⏳ High decay rate → Trend fades quickly.")
    else:
        st.write("📊 Low decay → Content remains relevant longer.")

    # Final engagement insight
    if final_sharers > 0.3 * N:
        st.write("🌐 High engagement network → Strong community sharing.")
    else:
        st.write("🔍 Limited engagement → Weak network effect.")

    # -----------------------------
    # GRAPH 1: Sharers vs Passive
    # -----------------------------
    st.subheader("🔁 Sharers vs Passive")

    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(S, label="Sharers")
    ax1.plot(P, label="Passive")
    ax1.legend()
    ax1.set_title("Sharers vs Passive Over Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Users")

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
    ax2.set_title("Growth vs Decay Dynamics")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Users")

    st.pyplot(fig2)
