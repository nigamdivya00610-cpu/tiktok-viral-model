import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

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
st.markdown('<p class="subtitle">Growth-Decay + Network + Influencer Effect</p>', unsafe_allow_html=True)

# -----------------------------
# LAYOUT: PARAMETERS
# -----------------------------
st.markdown('<p class="section">🔧 Model Parameters</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    N = st.slider("Total Users (N)", 100, 2000, 500)
    V0 = st.number_input("Initial Viewers", 1, N, 10)

with col2:
    alpha = st.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
    gamma = st.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)

with col3:
    beta = st.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
    delta = st.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

# Extra row
col4, col5 = st.columns(2)

with col4:
    p = st.slider("Network Density (p)", 0.001, 0.1, 0.01)

with col5:
    time_steps = st.slider("Time Steps", 50, 300, 150)
    S0 = st.number_input("Initial Sharers", 1, N, 5)

# -----------------------------
# RUN BUTTON
# -----------------------------
st.markdown("### ▶ Run Simulation")
run = st.button("Run Simulation 🚀")

# -----------------------------
# SIMULATION
# -----------------------------
if run:

    progress = st.progress(0)

    # Create network
    G = nx.erdos_renyi_graph(N, p)

    # Centrality & Influencers
    centrality = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality.values()))

    threshold = np.percentile(list(centrality.values()), 95)
    influencers = [n for n, v in centrality.items() if v >= threshold]
    influencer_effect = len(influencers) / N

    # Initial values
    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []

    dt = 0.1

    # -----------------------------
    # LOOP
    # -----------------------------
    for t in range(time_steps):

        progress.progress((t + 1) / time_steps)

        growth_factor = (1 + avg_centrality + influencer_effect)

        dV = (alpha * S * (P/N) * growth_factor - beta * V) * dt
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

    m1, m2, m3 = st.columns(3)
    m1.metric("🔥 Peak Views", int(peak_views))
    m2.metric("⏱ Peak Time", peak_time)
    m3.metric("🌟 Influencers", len(influencers))

    st.write("📊 Avg Centrality:", round(avg_centrality, 4))

    # -----------------------------
    # GRAPHS
    # -----------------------------
    st.markdown("## 📈 Simulation Results")

    g1, g2 = st.columns(2)

    # Combined Graph
    with g1:
        fig1, ax1 = plt.subplots()
        ax1.plot(np.array(V_list)/N, label="Viewers", color='red')
        ax1.plot(np.array(S_list)/N, label="Sharers", color='blue')
        ax1.plot(np.array(P_list)/N, label="Passive", color='green')
        ax1.axvline(x=peak_time, linestyle='--')
        ax1.set_title("Viral Spread (Normalized)")
        ax1.legend()
        st.pyplot(fig1)

    # Viewers Graph
    with g2:
        fig2, ax2 = plt.subplots()
        ax2.plot(V_list, color='red')
        ax2.axvline(x=peak_time, linestyle='--')
        ax2.set_title("Viewers Over Time")
        st.pyplot(fig2)

    # Sharers Graph
    fig3, ax3 = plt.subplots()
    ax3.plot(S_list, color='blue')
    ax3.set_title("Sharers Over Time")
    st.pyplot(fig3)

    # -----------------------------
    # NETWORK VISUAL
    # -----------------------------
    st.markdown("## 🌐 Network Structure")

    fig_net, ax = plt.subplots()
    nx.draw(G, node_size=10, ax=ax)
    st.pyplot(fig_net)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("## 📘 Interpretation")

    st.info("""
    • Initial slow growth → discovery phase  
    • Rapid rise → viral spread  
    • Peak → maximum reach  
    • Decline → saturation  

    ✔ Influencers accelerate spread  
    ✔ Network density impacts reach  
    ✔ Decay controls trend lifespan  
    """)
