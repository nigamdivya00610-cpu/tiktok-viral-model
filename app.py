import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 TikTok Viral Spread Model")

st.info("This model combines Growth-Decay equations with Network Theory to simulate viral spread.")

# -----------------------------
# PROJECT DESCRIPTION
# -----------------------------
st.markdown("""
## 📖 Project Description

This project models how a TikTok video spreads in a social network.

The viral spread depends on:
- 👥 User interaction  
- 🔗 Network connections  
- 📈 Sharing behavior  
- ⏳ Decay of interest  

### User Categories:
- **Viewers (V)** → Users who watch the video  
- **Sharers (S)** → Users who share the video  
- **Passive Users (P)** → Users who ignore the video  
""")

# -----------------------------
# MATHEMATICAL MODEL
# -----------------------------
st.markdown("""
## 📐 Mathematical Model

The system is defined using differential equations:

- dV/dt = αS − βV  
- dS/dt = γV − δS  
- P = N − (V + S)

Where:
- α → Growth rate  
- β → Decay rate  
- γ → Conversion to sharer  
- δ → Sharer fatigue  
""")

# -----------------------------
# NETWORK STRUCTURE
# -----------------------------
st.markdown("""
## 🌐 Network Structure

We model the system using a random network:

- Nodes → Users  
- Edges → Connections  

Network centrality represents influence:
- Higher centrality → faster viral spread 🚀  
""")

# -----------------------------
# USER INPUT
# -----------------------------
st.markdown("### 🔧 Adjust Parameters")

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
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation"):

    # Create Network
    G = nx.erdos_renyi_graph(N, p)

    # Centrality
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

- 📈 Growth phase → Video becomes popular  
- 🔥 Peak → Maximum reach  
- 📉 Decay → Interest decreases  

### Observations:
- High α and γ → Faster viral spread  
- High β and δ → Faster decline  
- Strong network → Higher peak  

This model successfully explains how TikTok trends rise and fall over time.
""")
