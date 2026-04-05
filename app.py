import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("# 📱 TikTok Viral Spread Simulator")
st.markdown("### Growth-Decay + Network Model")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.markdown("## 📱 Simulation Controls")

# Base inputs
N = st.sidebar.slider("Total Users (N)", 100, 2000, 500)
V0 = st.sidebar.number_input("Initial Viewers", 1, N, 10)
S0 = st.sidebar.number_input("Initial Sharers", 1, N, 5)

alpha = st.sidebar.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
gamma = st.sidebar.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)
beta = st.sidebar.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
delta = st.sidebar.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

time_steps = st.sidebar.slider("Time Steps", 50, 300, 150)

# NEW Network Inputs
st.sidebar.markdown("## 🌐 Network Controls")
connection_k = st.sidebar.slider("Connections per User (k)", 1, 10, 3)
influencer_boost = st.sidebar.slider("Influencer Boost", 1.0, 5.0, 1.5)

run = st.sidebar.button("Run Simulation 🚀")

# =============================
# RUN MODELS
# =============================
if run:

    # =============================
    # 1️⃣ GROWTH-DECAY MODEL
    # =============================
    st.markdown("## 📈 Growth-Decay Model")

    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []
    dt = 0.1

    for t in range(time_steps):

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

    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.metric("🔥 Peak Views", int(peak_views))
    st.metric("⏱ Peak Time", peak_time)

    fig1, ax1 = plt.subplots()
    ax1.plot(V_list, label="Viewers")
    ax1.plot(S_list, label="Sharers")
    ax1.plot(P_list, label="Passive")
    ax1.axvline(x=peak_time, linestyle='--')
    ax1.set_title("Growth-Decay Model")
    ax1.legend()
    st.pyplot(fig1)

    # 🔍 Interpretation (Model 1)
    st.markdown("### 🧠 Interpretation (Growth-Decay)")

    if peak_time < time_steps * 0.3:
        st.write("🚀 Rapid viral growth (early peak).")
    elif peak_time < time_steps * 0.7:
        st.write("📈 Steady growth before peak.")
    else:
        st.write("🐢 Slow spread.")

    if peak_views > 0.6 * N:
        st.write("🔥 High virality (reaches most users).")
    elif peak_views > 0.3 * N:
        st.write("⚡ Moderate popularity.")
    else:
        st.write("📉 Low reach.")

    if alpha > beta:
        st.write("💡 Growth dominates decay → sustained trend.")
    else:
        st.write("⛔ Decay dominates → short-lived trend.")

    # =============================
    # 2️⃣ NETWORK MODEL
    # =============================
    st.markdown("## 🌐 Network-Based Model")

    G = nx.barabasi_albert_graph(N, connection_k)
    centrality = nx.degree_centrality(G)

    states = {i: "P" for i in G.nodes()}

    init_V = np.random.choice(list(G.nodes()), V0, replace=False)
    init_S = np.random.choice(list(G.nodes()), S0, replace=False)

    for i in init_V:
        states[i] = "V"
    for i in init_S:
        states[i] = "S"

    V_net, S_net, P_net = [], [], []

    for t in range(time_steps):

        new_states = states.copy()

        for node in G.nodes():

            if states[node] == "P":
                neighbors = list(G.neighbors(node))
                influence = sum(1 for n in neighbors if states[n] == "S")

                prob_view = alpha * (influence / len(neighbors)) if len(neighbors) > 0 else 0

                if np.random.rand() < prob_view:
                    new_states[node] = "V"

            elif states[node] == "V":
                prob_share = gamma * centrality[node] * influencer_boost

                if np.random.rand() < prob_share:
                    new_states[node] = "S"
                elif np.random.rand() < beta:
                    new_states[node] = "P"

            elif states[node] == "S":
                if np.random.rand() < delta:
                    new_states[node] = "P"

        states = new_states

        V_net.append(sum(1 for s in states.values() if s == "V"))
        S_net.append(sum(1 for s in states.values() if s == "S"))
        P_net.append(sum(1 for s in states.values() if s == "P"))

    peak_views_net = max(V_net)
    peak_time_net = V_net.index(peak_views_net)

    st.metric("🔥 Peak Views (Network)", int(peak_views_net))
    st.metric("⏱ Peak Time (Network)", peak_time_net)

    fig2, ax2 = plt.subplots()
    ax2.plot(V_net, label="Viewers")
    ax2.plot(S_net, label="Sharers")
    ax2.plot(P_net, label="Passive")
    ax2.axvline(x=peak_time_net, linestyle='--')
    ax2.set_title("Network Model")
    ax2.legend()
    st.pyplot(fig2)

    # 🔍 Influencer Insight
    top_node = max(centrality, key=centrality.get)

    st.markdown("### 🌟 Influencer Insight")
    st.write(f"Top Influencer Node: {top_node}")
    st.write(f"Centrality Score: {centrality[top_node]:.4f}")

    # 🔍 Interpretation (Model 2)
    st.markdown("### 🧠 Interpretation (Network Model)")

    if peak_views_net > 0.6 * N:
        st.write("🔥 Strong viral spread driven by influencers.")
    elif peak_views_net > 0.3 * N:
        st.write("⚡ Moderate spread with limited influencer impact.")
    else:
        st.write("📉 Weak spread (poor network influence).")

    if peak_time_net < time_steps * 0.3:
        st.write("🚀 Fast viral explosion via highly connected users.")
    else:
        st.write("🐢 Slower spread across network.")

    if influencer_boost > 2:
        st.write("🌟 Influencers play a major role in virality.")
    else:
        st.write("👥 Spread is more organic (less influencer-driven).")
