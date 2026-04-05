import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

st.title("📱 TikTok Viral Spread Simulator")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("⚙️ Controls")

N = st.sidebar.slider("Total Users", 100, 2000, 500)
V0 = st.sidebar.number_input("Initial Viewers", 1, N, 10)
S0 = st.sidebar.number_input("Initial Sharers", 1, N, 5)

alpha = st.sidebar.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
gamma = st.sidebar.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)

beta = st.sidebar.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
delta = st.sidebar.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

time_steps = st.sidebar.slider("Time Steps", 50, 300, 150)

run = st.sidebar.button("🚀 Run Simulation")

# =============================
# RUN SIMULATION
# =============================
if run:

    # -----------------------------
    # GROWTH-DECAY MODEL
    # -----------------------------
    st.header("📈 Growth-Decay Model")

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

        V, S, P = max(V, 0), max(S, 0), max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)
    final_views = V_list[-1]

    st.metric("🔥 Peak Views", int(peak_views))
    st.metric("⏱ Peak Time", peak_time)

    # Plot
    fig1, ax1 = plt.subplots()
    ax1.plot(V_list, label="Viewers")
    ax1.plot(S_list, label="Sharers")
    ax1.plot(P_list, label="Passive")
    ax1.axvline(x=peak_time, linestyle='--')
    ax1.legend()
    st.pyplot(fig1)

    # -----------------------------
    # RESULT-BASED INTERPRETATION
    # -----------------------------
    st.subheader("📊 Interpretation (Based on Results)")

    growth_ratio = peak_views / V0

    if peak_time < time_steps * 0.3:
        timing_msg = "The video went viral very quickly (early peak)."
    elif peak_time < time_steps * 0.7:
        timing_msg = "The video showed steady growth before peaking."
    else:
        timing_msg = "The video took a long time to gain popularity."

    if final_views < peak_views * 0.3:
        decay_msg = "Interest dropped sharply after peak."
    elif final_views < peak_views * 0.7:
        decay_msg = "Moderate decline after peak."
    else:
        decay_msg = "The video maintained popularity even after peak."

    if growth_ratio > 5:
        viral_msg = "Highly viral content 🚀"
    elif growth_ratio > 2:
        viral_msg = "Moderately viral content"
    else:
        viral_msg = "Low virality"

    st.write(f"""
- Peak occurred at time **{peak_time}**
- Viewers increased **{growth_ratio:.2f}x** from initial

### 🔍 Insights:
👉 {timing_msg}  
👉 {decay_msg}  
👉 Overall: **{viral_msg}**
""")

    # -----------------------------
    # NETWORK MODEL
    # -----------------------------
    st.header("🌐 Network Model")

    G = nx.barabasi_albert_graph(N, 3)
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

                prob_view = alpha * (influence / len(neighbors)) if neighbors else 0

                if np.random.rand() < prob_view:
                    new_states[node] = "V"

            elif states[node] == "V":
                if np.random.rand() < gamma * centrality[node]:
                    new_states[node] = "S"
                elif np.random.rand() < beta:
                    new_states[node] = "P"

            elif states[node] == "S":
                if np.random.rand() < delta:
                    new_states[node] = "P"

        states = new_states

        V_net.append(sum(1 for s in states.values() if s == "V"))

    peak_views_net = max(V_net)
    peak_time_net = V_net.index(peak_views_net)
    final_views_net = V_net[-1]

    st.metric("🔥 Peak Views (Network)", int(peak_views_net))
    st.metric("⏱ Peak Time (Network)", peak_time_net)

    # Plot
    fig2, ax2 = plt.subplots()
    ax2.plot(V_net, label="Viewers")
    ax2.axvline(x=peak_time_net, linestyle='--')
    ax2.legend()
    st.pyplot(fig2)

    # -----------------------------
    # NETWORK INTERPRETATION
    # -----------------------------
    st.subheader("📊 Interpretation (Network Results)")

    if peak_views_net > peak_views:
        compare_msg = "Network effect boosted virality significantly."
    else:
        compare_msg = "Network structure limited the spread."

    if peak_time_net < peak_time:
        speed_msg = "Spread was faster due to social connections."
    else:
        speed_msg = "Spread was slower compared to basic model."

    retention = final_views_net / peak_views_net

    if retention > 0.7:
        sustain_msg = "Strong audience retention."
    elif retention > 0.3:
        sustain_msg = "Moderate retention."
    else:
        sustain_msg = "Poor retention after peak."

    st.write(f"""
- Network peak at time **{peak_time_net}**
- Retention ratio: **{retention:.2f}**

### 🔍 Insights:
👉 {compare_msg}  
👉 {speed_msg}  
👉 {sustain_msg}
""")
