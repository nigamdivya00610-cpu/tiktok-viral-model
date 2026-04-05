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

This project models how a TikTok video goes viral using **mathematical modelling and network theory**.

The spread of a video depends on:
- 👥 User interactions
- 🔗 Network connections
- 📈 Sharing behavior
- ⏳ Loss of interest over time

### User Categories:
- **Viewers (V)** – Users who watch the video  
- **Sharers (S)** – Users who share the video  
- **Passive Users (P)** – Users who ignore the video  
""")

# -----------------------------
# MATHEMATICAL MODEL
# -----------------------------
st.markdown("""
## 📐 Mathematical Model

The system is based on growth-decay equations:

- dV/dt = αS − βV  
- dS/dt = γV − δS  
- P = N − (V + S)

Where:
- α → Growth rate (sharing effect)  
- β → Decay rate (loss of interest)  
- γ → Viewer to sharer conversion  
- δ → Sharer fatigue  
""")

# -----------------------------
# NETWORK STRUCTURE
# -----------------------------
st.markdown("""
## 🌐 Network Structure

The model uses a **random network** to simulate social connections.

- Nodes → Users  
- Edges → Connections  

Higher connectivity increases the spread of the video.

We also use **centrality** to measure influence:
- High centrality → faster viral spread 🚀  
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
    # GRAPH
    # -----------------------------
    fig, ax = plt.subplots()

    ax.plot(V_list, label="Viewers (V)")
    ax.plot(S_list, label="Sharers (S)")
    ax.plot(P_list, label="Passive (P)")

    ax.axvline(x=peak_time, linestyle='--', label="Peak")

    ax.set_xlabel("Time")
    ax.set_ylabel("Users")
    ax.set_title("TikTok Viral Spread Simulation")
    ax.legend()

    # ❌ Removed grid for cleaner look
    ax.grid(False)

    # Optional styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("""
    ## 📊 Result Interpretation

    - 📈 Initial growth shows video gaining popularity  
    - 🔥 Peak indicates maximum viral reach  
    - 📉 Decline shows loss of user interest  

    ### Key Observations:
    - Strong network → faster spread  
    - High decay → shorter viral life  
    - More sharers → higher peak  

    This model demonstrates how TikTok trends rise and fall over time.
    """)
