import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 TikTok Viral Spread Model")

st.info("Mathematical Modelling using Growth-Decay + Network + Influencers")

# -----------------------------
# 📌 PROBLEM DEFINITION
# -----------------------------
st.markdown("""
## 📌 Problem Definition

This project models how a TikTok video goes viral in a social network.

We aim to:
- Understand how content spreads among users
- Identify peak viral time
- Analyze the role of influencers and network structure
- Study how promotion or suppression affects reach
""")

# -----------------------------
# 📘 MODEL DESCRIPTION
# -----------------------------
st.markdown("""
## 📘 Model Description

### 👤 User Categories:
- **Viewers (V):** Users who watch the video
- **Sharers (S):** Users who share the video
- **Passive Users (P):** Users who have not seen the video

### 🌐 Network:
Users are connected through a random network.  
Highly connected users (influencers) increase spread.
""")

# -----------------------------
# 🧮 MATHEMATICAL MODEL
# -----------------------------
st.markdown("""
## 🧮 Mathematical Formulation

The spread is modeled using differential equations:

dV/dt = α * S * (P/N) * (1 + Centrality + Influencers) - β * V  

dS/dt = γ * V * (P/N) - δ * S  

P = N - (V + S)

Where:
- α = Growth rate
- β = Viewer decay
- γ = Conversion to sharers
- δ = Sharer decay
""")

# -----------------------------
# ⚙️ ASSUMPTIONS
# -----------------------------
st.markdown("""
## ⚙️ Assumptions

- Total population is constant
- Users interact through a network
- Influencers accelerate spread
- Passive users become viewers via sharers
- Decay represents loss of interest over time
""")

# -----------------------------
# PARAMETERS
# -----------------------------
st.markdown("## 🔧 Model Parameters")

N = st.slider("Total Users (N)", 100, 2000, 500)

alpha = st.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
beta = st.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
gamma = st.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)
delta = st.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

p = st.slider("Network Density (p)", 0.001, 0.1, 0.01)
time_steps = st.slider("Time Steps", 50, 300, 150)

V0 = st.number_input("Initial Viewers", 1, N, 10)
S0 = st.number_input("Initial Sharers", 1, N, 5)

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation"):

    # Create network
    G = nx.erdos_renyi_graph(N, p)

    # Centrality & Influencers
    centrality = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality.values()))

    threshold = np.percentile(list(centrality.values()), 95)
    influencers = [n for n, v in centrality.items() if v >= threshold]
    influencer_effect = len(influencers) / N

    st.write("📊 Avg Centrality:", round(avg_centrality, 4))
    st.write("🌟 Influencers:", len(influencers))

    # Initial values
    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []

    dt = 0.1

    # -----------------------------
    # SIMULATION LOOP
    # -----------------------------
    for t in range(time_steps):

        growth_factor = (1 + avg_centrality + influencer_effect)

        dV = (alpha * S * (P/N) * growth_factor - beta * V) * dt
        dS = (gamma * V * (P/N) - delta * S) * dt

        V += dV
        S += dS
        P = N - (V + S)

        # Avoid negative values
        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    # -----------------------------
    # PEAK DETECTION
    # -----------------------------
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time {peak_time}")

    # =============================
    # 📊 GRAPH 1: COMBINED
    # =============================
    st.markdown("## 📊 Combined Graph")

    fig1, ax1 = plt.subplots()
    ax1.plot(np.array(V_list)/N, label="Viewers")
    ax1.plot(np.array(S_list)/N, label="Sharers")
    ax1.plot(np.array(P_list)/N, label="Passive")
    ax1.axvline(x=peak_time, linestyle='--', label="Peak")

    ax1.set_title("Viral Spread")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Proportion")
    ax1.legend()

    st.pyplot(fig1)

    # =============================
    # 📈 VIEWERS GRAPH
    # =============================
    st.markdown("## 📈 Viewers Graph")

    fig2, ax2 = plt.subplots()
    ax2.plot(V_list)
    ax2.axvline(x=peak_time, linestyle='--')

    ax2.set_title("Viewers Over Time")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Viewers")

    st.pyplot(fig2)

    # =============================
    # 🔁 SHARERS GRAPH
    # =============================
    st.markdown("## 🔁 Sharers Graph")

    fig3, ax3 = plt.subplots()
    ax3.plot(S_list)

    ax3.set_title("Sharers Over Time")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Sharers")

    st.pyplot(fig3)

# -----------------------------
# 📊 INTERPRETATION
# -----------------------------
st.markdown("""
## 📊 Interpretation & Real-World Use

- Slow start → initial exposure  
- Rapid growth → viral phase  
- Peak → maximum popularity  
- Decline → audience saturation  

### 🌍 Real-World Applicability:
- Helps understand TikTok algorithm behavior  
- Useful for digital marketing strategies  
- Can predict viral trends  
""")
