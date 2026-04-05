import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown("""
<style>
.title {
    font-size:40px;
    font-weight:bold;
    color:#ff0050;
}
.subtitle {
    font-size:18px;
    color:gray;
}
.section {
    font-size:24px;
    font-weight:bold;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<p class="title">📱 TikTok Viral Spread Simulator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Growth-Decay Model</p>', unsafe_allow_html=True)

# -----------------------------
# TOPIC CONTENT
# -----------------------------
st.markdown("## 📱 Trending Video Spread on TikTok Modelling")

st.markdown("""
This project models how a video becomes viral on TikTok using a mathematical approach.

The spread of a video is treated as a dynamic process where users interact with content over time. The model divides the population into three main groups:

- 👀 **Viewers (V)**  
- 🔁 **Sharers (S)**  
- 😶 **Passive Users (P)**  

The model is based on:
- 📈 Growth (sharing increases reach)  
- 📉 Decay (interest decreases over time)  

It helps analyze peak views, peak time, and engagement behavior.
""")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.markdown("### 📱 TikTok Controls")

N = st.sidebar.slider("Total Users (N)", 100, 2000, 500)
V0 = st.sidebar.number_input("Initial Viewers", 1, N, 10)

alpha = st.sidebar.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
gamma = st.sidebar.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)

beta = st.sidebar.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
delta = st.sidebar.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

time_steps = st.sidebar.slider("Time Steps", 50, 300, 150)
S0 = st.sidebar.number_input("Initial Sharers", 1, N, 5)

run = st.sidebar.button("Run Simulation 🚀")

# -----------------------------
# SIMULATION
# -----------------------------
if run:

    progress = st.progress(0)

    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []
    dt = 0.1

    for t in range(time_steps):

        progress.progress((t + 1) / time_steps)

        dV = (alpha * S * (P/N) - beta * V) * dt
        dS = (gamma * V * (P/N) - delta * S) * dt

        V += dV
        S += dS
        P = N - (V + S)

        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    # -----------------------------
    # METRICS
    # -----------------------------
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.markdown("## 📊 Key Metrics")

    m1, m2 = st.columns(2)
    m1.metric("🔥 Peak Views", int(peak_views))
    m2.metric("⏱ Peak Time", peak_time)

    # -----------------------------
    # GRAPHS
    # -----------------------------
    st.markdown("## 📈 Simulation Results")

    g1, g2 = st.columns(2)

    # Viewers Graph
    with g1:
        fig2, ax2 = plt.subplots()
        ax2.plot(V_list, color='red')
        ax2.axvline(x=peak_time, linestyle='--')
        ax2.set_title("Viewers Over Time")
        st.pyplot(fig2)

    # Sharers Graph
    with g2:
        fig3, ax3 = plt.subplots()
        ax3.plot(S_list, color='blue')
        ax3.set_title("Sharers Over Time")
        st.pyplot(fig3)

    # -----------------------------
    # FINAL COMBINED GRAPH
    # -----------------------------
    st.markdown("## 📊 Final Combined Overview")

    fig4, ax4 = plt.subplots()
    ax4.plot(V_list, label="Viewers", color='red')
    ax4.plot(S_list, label="Sharers", color='blue')
    ax4.plot(P_list, label="Passive", color='green')
    ax4.axvline(x=peak_time, linestyle='--', label="Peak Time")
    ax4.set_title("Final Combined Spread (Actual Values)")
    ax4.set_xlabel("Time")
    ax4.set_ylabel("Users")
    ax4.legend()
    st.pyplot(fig4)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("**Interpretation**")

    insights = []

    if peak_time < time_steps * 0.3:
        insights.append("🚀 The video spreads very quickly and becomes viral early.")
    elif peak_time < time_steps * 0.7:
        insights.append("📈 The video shows steady growth before reaching peak.")
    else:
        insights.append("🐢 The video spreads slowly and takes time to gain attention.")

    if peak_views > 0.6 * N:
        insights.append("🔥 The video achieves high virality and reaches most users.")
    elif peak_views > 0.3 * N:
        insights.append("⚡ The video achieves moderate popularity.")
    else:
        insights.append("📉 The video has limited reach.")

    if alpha > beta:
        insights.append("💡 Growth is stronger than decay → sustained engagement.")
    else:
        insights.append("⛔ High decay reduces interest quickly.")

    if gamma > delta:
        insights.append("🔁 Sharing behavior boosts the spread.")
    else:
        insights.append("📉 Low sharing limits virality.")

    for i in insights:
        st.write(i)
# =============================
# 🌐 NETWORK-BASED VIRAL MODEL (ADVANCED ADD-ON)
# =============================

st.markdown("## 🌐 Advanced Network-Based Viral Spread")

import networkx as nx

run_network = st.button("Run Network Simulation 🌐")

if run_network:

    progress_net = st.progress(0)

    # Create Scale-Free Network (TikTok-like)
    G = nx.barabasi_albert_graph(N, 3)

    # Centrality (influencer detection)
    centrality = nx.degree_centrality(G)

    # Initialize states
    states = {i: "P" for i in G.nodes()}

    # Initial viewers & sharers
    init_V = np.random.choice(list(G.nodes()), V0, replace=False)
    init_S = np.random.choice(list(G.nodes()), S0, replace=False)

    for i in init_V:
        states[i] = "V"

    for i in init_S:
        states[i] = "S"

    V_net, S_net, P_net = [], [], []

    # Simulation loop
    for t in range(time_steps):

        progress_net.progress((t + 1) / time_steps)

        new_states = states.copy()

        for node in G.nodes():

            if states[node] == "P":
                neighbors = list(G.neighbors(node))

                influence = sum(1 for n in neighbors if states[n] == "S")

                prob_view = alpha * (influence / len(neighbors)) if len(neighbors) > 0 else 0

                if np.random.rand() < prob_view:
                    new_states[node] = "V"

            elif states[node] == "V":
                prob_share = gamma * centrality[node]

                if np.random.rand() < prob_share:
                    new_states[node] = "S"
                elif np.random.rand() < beta:
                    new_states[node] = "P"

            elif states[node] == "S":
                if np.random.rand() < delta:
                    new_states[node] = "P"

        states = new_states

        # Count states
        V_count = sum(1 for s in states.values() if s == "V")
        S_count = sum(1 for s in states.values() if s == "S")
        P_count = sum(1 for s in states.values() if s == "P")

        V_net.append(V_count)
        S_net.append(S_count)
        P_net.append(P_count)

    # -----------------------------
    # METRICS
    # -----------------------------
    peak_views_net = max(V_net)
    peak_time_net = V_net.index(peak_views_net)

    st.markdown("### 📊 Network Model Metrics")

    c1, c2 = st.columns(2)
    c1.metric("🔥 Peak Views (Network)", int(peak_views_net))
    c2.metric("⏱ Peak Time (Network)", peak_time_net)

    # -----------------------------
    # GRAPH
    # -----------------------------
    fig_net, ax_net = plt.subplots()
    ax_net.plot(V_net, label="Viewers", color='red')
    ax_net.plot(S_net, label="Sharers", color='blue')
    ax_net.plot(P_net, label="Passive", color='green')
    ax_net.axvline(x=peak_time_net, linestyle='--', label="Peak Time")
    ax_net.set_title("Network-Based Viral Spread")
    ax_net.set_xlabel("Time")
    ax_net.set_ylabel("Users")
    ax_net.legend()

    st.pyplot(fig_net)

    # -----------------------------
    # INFLUENCER ANALYSIS
    # -----------------------------
    top_node = max(centrality, key=centrality.get)

    st.markdown("### 🌟 Influencer Insight")
    st.write(f"Top Influencer Node: {top_node}")
    st.write(f"Centrality Score: {centrality[top_node]:.4f}")

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("### 🧠 Network Interpretation")

    if peak_views_net > 0.6 * N:
        st.write("🔥 Strong viral spread driven by network influencers.")
    elif peak_views_net > 0.3 * N:
        st.write("⚡ Moderate spread with limited influencer effect.")
    else:
        st.write("📉 Weak spread due to low connectivity or influence.")

    if peak_time_net < time_steps * 0.3:
        st.write("🚀 Rapid viral explosion due to highly connected nodes.")
    else:
        st.write("🐢 Slower spread across the network.")
