import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 TikTok Viral Spread Modelling")

# -----------------------------
# PROBLEM DEFINITION
# -----------------------------
st.markdown("""
## 📌 Problem Definition

This project models how a TikTok video becomes viral in a social network.

We aim to:
- Understand how users interact with content
- Predict how quickly a video spreads
- Identify peak popularity
- Analyze the effect of influencers and network structure
""")

# -----------------------------
# MODEL DESCRIPTION
# -----------------------------
st.markdown("""
## 🧠 Model Description

We divide users into 3 categories:

- 👀 Viewers (V): People who watch the video  
- 🔁 Sharers (S): People who share the video  
- 😐 Passive Users (P): People who have not seen the video  

The model combines:
- Growth-Decay equations  
- Network structure  
- Influencer effect  
""")

# -----------------------------
# MATHEMATICAL MODEL
# -----------------------------
st.markdown("""
## 📐 Mathematical Formulation

dV/dt = α S (P/N) (1 + C + I) - β V  

dS/dt = γ V (P/N) - δ S  

P = N - (V + S)

Where:
- α = growth rate  
- β = decay rate  
- γ = viewer → sharer rate  
- δ = sharer decay  
- C = network centrality  
- I = influencer effect  
""")

# -----------------------------
# ASSUMPTIONS
# -----------------------------
st.markdown("""
## 📋 Assumptions

- Total users (N) remain constant  
- Passive users become viewers through sharers  
- Influencers accelerate spread  
- Network connections affect visibility  
- Decay occurs due to reduced interest  
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

    # Simulation
    for t in range(time_steps):

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

    # Peak detection
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time {peak_time}")

    # -----------------------------
    # GRAPH 1: COMBINED
    # -----------------------------
    st.markdown("## 📊 Combined Graph")

    fig1, ax1 = plt.subplots()

    ax1.plot(np.array(V_list)/N, label="Viewers")
    ax1.plot(np.array(S_list)/N, label="Sharers")
    ax1.plot(np.array(P_list)/N, label="Passive")

    ax1.axvline(x=peak_time, linestyle='--', label="Peak")

    ax1.set_title("Normalized Viral Spread")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Proportion")
    ax1.legend()

    st.pyplot(fig1)

    # -----------------------------
    # GRAPH 2: VIEWERS
    # -----------------------------
    st.markdown("## 📈 Viewers Graph")

    fig2, ax2 = plt.subplots()
    ax2.plot(V_list)
    ax2.axvline(x=peak_time, linestyle='--')

    ax2.set_title("Viewers Over Time")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Viewers")

    st.pyplot(fig2)

    # -----------------------------
    # GRAPH 3: SHARERS
    # -----------------------------
    st.markdown("## 🔁 Sharers Graph")

    fig3, ax3 = plt.subplots()
    ax3.plot(S_list)

    ax3.set_title("Sharers Over Time")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Sharers")

    st.pyplot(fig3)

# -----------------------------
# REAL WORLD USE
# -----------------------------
st.markdown("""
## 🌍 Real-World Applicability

- Helps TikTok understand viral trends  
- Useful for marketers to design campaigns  
- Predicts peak engagement time  
- Helps control misinformation spread  
""")
