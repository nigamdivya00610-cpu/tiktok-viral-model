import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 TikTok Viral Spread Model")

st.info("This project models how a TikTok video becomes viral using Growth-Decay equations and Network Structure.")

# -----------------------------
# PROJECT DESCRIPTION
# -----------------------------
st.markdown("""
## 📖 Project Description

This model simulates how a TikTok video spreads among users in a network.

The spread depends on:
- 👥 User interaction
- 🔗 Network connectivity
- 📈 Sharing behavior
- ⏳ Loss of interest over time

### 👤 User Categories:
- **Viewers (V)** → Users who watch the video  
- **Sharers (S)** → Users who share the video  
- **Passive Users (P)** → Users who ignore the video  
""")

# -----------------------------
# MATHEMATICAL MODEL
# -----------------------------
st.markdown("""
## 📐 Mathematical Model

The system is based on the following equations:

- dV/dt = αS − βV  
- dS/dt = γV − δS  
- P = N − (V + S)

### Where:
- α → Growth rate (how fast video spreads)  
- β → Decay rate (loss of interest)  
- γ → Conversion rate (viewer → sharer)  
- δ → Sharer fatigue  
""")

# -----------------------------
# NETWORK STRUCTURE
# -----------------------------
st.markdown("""
## 🌐 Network Structure

The model uses a random network to represent users.

- Nodes → Users  
- Edges → Connections  

We calculate **centrality** to measure influence:
- Higher centrality → faster spread 🚀  
""")

st.markdown("### 🔧 Adjust Parameters")

# -----------------------------
# USER INPUT (Streamlit UI)
# -----------------------------
N = st.slider("Total Users (N)", 100, 1000, 500)

alpha = st.slider("Growth Rate (α)", 0.0, 1.0, 0.6)
beta = st.slider("Decay Rate (β)", 0.0, 1.0, 0.2)
gamma = st.slider("Viewer → Sharer (γ)", 0.0, 1.0, 0.3)
delta = st.slider("Sharer Decay (δ)", 0.0, 1.0, 0.1)

time_steps = st.slider("Time Steps", 10, 200, 100)

V = st.number_input("Initial Viewers (V0)", 1, N, 10)
S = st.number_input("Initial Sharers (S0)", 1, N, 5)

p = st.slider("Network Connection Probability", 0.0, 0.1, 0.02)

dt = 0.1

# -----------------------------
# RUN SIMULATION BUTTON
# -----------------------------
if st.button("Run Simulation"):

    # Create Network
    G = nx.erdos_renyi_graph(N, p)

    # Centrality factor
    centrality = np.mean(list(nx.degree_centrality(G).values()))

    st.write("📊 Average Network Centrality:", round(centrality, 4))

    # Storage
    V_list = []
    S_list = []
    P_list = []

    # Simulation
    for t in range(time_steps):

        dV = (alpha * S * centrality - beta * V) * dt
        dS = (gamma * V - delta * S) * dt

        V = V + dV
        S = S + dS
        P = N - (V + S)

        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    # Peak
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time Step {peak_time}")

    # -----------------------------
    # SEPARATE GRAPHS
    # -----------------------------
    st.markdown("## 📊 Graphical Results")

    # Viewers Graph
    fig1, ax1 = plt.subplots()
    ax1.plot(V_list, label="Viewers (V)")
    ax1.axvline(x=peak_time, linestyle='--', label="Peak")
    ax1.set_title("📈 Viewers Over Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Users")
    ax1.legend()
    ax1.grid(False)
    st.pyplot(fig1)

    # Sharers Graph
    fig2, ax2 = plt.subplots()
    ax2.plot(S_list, label="Sharers (S)")
    ax2.set_title("🔁 Sharers Over Time")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Users")
    ax2.legend()
    ax2.grid(False)
    st.pyplot(fig2)

    # Passive Graph
    fig3, ax3 = plt.subplots()
    ax3.plot(P_list, label="Passive Users (P)")
    ax3.set_title("😴 Passive Users Over Time")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Users")
    ax3.legend()
    ax3.grid(False)
    st.pyplot(fig3)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("""
## 📊 Interpretation of Results

- 📈 Initial growth → video becomes popular  
- 🔥 Peak → maximum reach  
- 📉 Decline → interest decreases  

### Key Observations:
- Higher α and γ → faster viral spread  
- Higher β and δ → faster decline  
- Strong network → higher peak  

This model explains how TikTok trends grow and fade over time.
""")
