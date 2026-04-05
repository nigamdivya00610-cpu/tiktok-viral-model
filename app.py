import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# -----------------------------
# 🎨 PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

# -----------------------------
# 🎯 HEADER
# -----------------------------
st.markdown("""
# 🚀 TikTok Viral Spread Simulator
### 📱 Understand how videos go viral using Network + Math Modeling
""")

st.divider()

# -----------------------------
# 📘 INTRO
# -----------------------------
with st.expander("📘 About This Project"):
    st.markdown("""
This simulator models how a TikTok video spreads through a social network.

👥 Users are divided into:
- 👀 Viewers  
- 🔁 Sharers  
- 😴 Passive users  

It combines:
- Growth–decay dynamics  
- Network connectivity  
- Influencer impact  

🔥 Goal: Predict viral peaks and spread patterns.
""")

# -----------------------------
# 🎛️ PARAMETERS PANEL
# -----------------------------
st.sidebar.header("⚙️ Simulation Controls")

N = st.sidebar.slider("Total Users", 100, 2000, 500)
p = st.sidebar.slider("Network Density", 0.001, 0.1, 0.01)
time_steps = st.sidebar.slider("Time Steps", 50, 300, 150)

st.sidebar.markdown("### 📊 Behavior Rates")

alpha = st.sidebar.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
beta = st.sidebar.slider("Viewer Decay (β)", 0.01, 0.5, 0.1)
gamma = st.sidebar.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)
delta = st.sidebar.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

V0 = st.sidebar.number_input("Initial Viewers", 1, N, 10)
S0 = st.sidebar.number_input("Initial Sharers", 1, N, 5)

# -----------------------------
# ▶️ RUN BUTTON
# -----------------------------
run = st.button("🚀 Run Simulation")

# -----------------------------
# 📊 SIMULATION
# -----------------------------
if run:

    with st.spinner("Simulating viral spread..."):

        # Create network
        G = nx.erdos_renyi_graph(N, p)

        centrality = nx.degree_centrality(G)
        avg_centrality = np.mean(list(centrality.values()))

        threshold = np.percentile(list(centrality.values()), 95)
        influencers = [n for n, v in centrality.items() if v >= threshold]

        influencer_effect = len(influencers) / N

        # Initial states
        V, S = V0, S0
        P = N - (V + S)

        V_list, S_list, P_list = [], [], []

        dt = 0.1

        progress = st.progress(0)

        for t in range(time_steps):

            growth = (1 + avg_centrality + influencer_effect)

            dV = (alpha * S * (P/N) * growth - beta * V) * dt
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

            progress.progress((t+1)/time_steps)

    # -----------------------------
    # 📈 METRICS
    # -----------------------------
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Peak Views", int(peak_views))
    col2.metric("⏱ Peak Time", peak_time)
    col3.metric("🌟 Influencers", len(influencers))

    st.divider()

    # -----------------------------
    # 📊 GRAPHS
    # -----------------------------
    st.subheader("📊 Viral Spread Overview")

    fig, ax = plt.subplots()
    ax.plot(np.array(V_list)/N, label="Viewers")
    ax.plot(np.array(S_list)/N, label="Sharers")
    ax.plot(np.array(P_list)/N, label="Passive")
    ax.axvline(x=peak_time, linestyle='--')

    ax.set_title("Normalized Viral Spread")
    ax.set_xlabel("Time")
    ax.set_ylabel("Proportion")
    ax.legend()

    st.pyplot(fig)

    # -----------------------------
    # 📈 INDIVIDUAL GRAPHS
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👀 Viewers Trend")
        fig1, ax1 = plt.subplots()
        ax1.plot(V_list)
        ax1.set_title("Viewers Over Time")
        st.pyplot(fig1)

    with col2:
        st.subheader("🔁 Sharers Trend")
        fig2, ax2 = plt.subplots()
        ax2.plot(S_list)
        ax2.set_title("Sharers Over Time")
        st.pyplot(fig2)

    # -----------------------------
    # 🌐 NETWORK VISUALIZATION
    # -----------------------------
    st.subheader("🌐 Social Network Structure")

    fig_net = plt.figure(figsize=(5,5))
    nx.draw(G, node_size=8)
    st.pyplot(fig_net)

    # -----------------------------
    # 📥 DOWNLOAD DATA
    # -----------------------------
    df = pd.DataFrame({
        "Time": range(time_steps),
        "Viewers": V_list,
        "Sharers": S_list,
        "Passive": P_list
    })

    st.download_button("📥 Download Results", df.to_csv(index=False), "viral_data.csv")

    # -----------------------------
    # 📘 INTERPRETATION
    # -----------------------------
    st.markdown("""
## 📘 Interpretation

- 📍 Early stage → slow growth  
- 🚀 Viral phase → rapid increase  
- 🔥 Peak → maximum reach  
- 📉 Decline → audience saturation  

👉 Influencers and network density strongly impact virality.
""")
