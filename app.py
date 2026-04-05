import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# =============================
# 📱 TITLE
# =============================
st.title("📱 TikTok Viral Spread Modelling")

st.info("Growth-Decay Model + Network Structure + Influencers")

# =============================
# 📌 PROBLEM DEFINITION
# =============================
st.markdown("""
## 📌 Problem Definition
This project models how a TikTok video spreads and becomes viral in a social network.

Objectives:
- Study how users interact and spread content
- Identify peak viral time
- Understand influencer impact
- Analyze spread and decline behavior
""")

# =============================
# 📘 MODEL DESCRIPTION
# =============================
st.markdown("""
## 📘 Model Description

### User Categories:
- **Viewers (V)** – Users watching the video  
- **Sharers (S)** – Users sharing the video  
- **Passive (P)** – Users who haven’t seen it  

### Network:
Users are connected through a random network.  
Highly connected users act as influencers.
""")

# =============================
# 🧮 MATHEMATICAL MODEL
# =============================
st.markdown("""
## 🧮 Mathematical Model

dV/dt = α * S * (P/N) * (1 + Centrality + Influencers) − β * V  

dS/dt = γ * V * (P/N) − δ * S  

P = N − (V + S)
""")

# =============================
# ⚙️ ASSUMPTIONS
# =============================
st.markdown("""
## ⚙️ Assumptions
- Total users remain constant  
- Spread occurs via network connections  
- Influencers accelerate spread  
- Users lose interest over time (decay)  
""")

# =============================
# 🔧 PARAMETERS
# =============================
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

# =============================
# ▶ RUN SIMULATION
# =============================
if st.button("Run Simulation"):

    # 🌐 Create Network
    G = nx.erdos_renyi_graph(N, p)

    # 📊 Centrality
    centrality = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality.values()))

    # ⭐ Influencers (Top 5%)
    threshold = np.percentile(list(centrality.values()), 95)
    influencers = [node for node, val in centrality.items() if val >= threshold]
    influencer_effect = len(influencers) / N

    st.write("📊 Average Centrality:", round(avg_centrality, 4))
    st.write("🌟 Influencers:", len(influencers))

    # Initial values
    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []

    dt = 0.1

    # 🔁 Simulation Loop
    for t in range(time_steps):

        growth = (1 + avg_centrality + influencer_effect)

        dV = (alpha * S * (P/N) * growth - beta * V) * dt
        dS = (gamma * V * (P/N) - delta * S) * dt

        V += dV
        S += dS
        P = N - (V + S)

        # Prevent negatives
        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    # 🔥 Peak Detection
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time {peak_time}")

    # =============================
    # 🌐 NETWORK GRAPH
    # =============================
    st.markdown("## 🌐 Network Structure")

    fig_net = plt.figure()
    nx.draw(G, node_size=10)
    st.pyplot(fig_net)

    # =============================
    # 📊 COMBINED GRAPH
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

# =============================
# 📊 INTERPRETATION
# =============================
st.markdown("""
## 📊 Interpretation

- Initial phase → slow growth  
- Viral phase → rapid increase  
- Peak → maximum reach  
- Decline → saturation  

## ✅ Validation
The model follows real-world TikTok trends:
- Content spreads quickly due to sharing  
- Influencers increase reach  
- Interest decreases over time  

## 🌍 Real-World Use
- Digital marketing strategies  
- Predict viral content  
- Social media analysis  
""")
