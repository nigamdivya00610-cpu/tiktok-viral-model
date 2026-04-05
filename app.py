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

 import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 TikTok Viral Spread Model")
st.info("Growth-Decay + Network Theory based simulation of viral content spread")

# -----------------------------
# SIDEBAR INPUT (Cleaner UI)
# -----------------------------
st.sidebar.header("🔧 Model Parameters")

N = st.sidebar.slider("Total Users (N)", 100, 1000, 500)

alpha = st.sidebar.slider("Growth Rate (α)", 0.0, 1.0, 0.6)
beta = st.sidebar.slider("Decay Rate (β)", 0.0, 1.0, 0.2)
gamma = st.sidebar.slider("Viewer → Sharer (γ)", 0.0, 1.0, 0.3)
delta = st.sidebar.slider("Sharer Decay (δ)", 0.0, 1.0, 0.1)

time_steps = st.sidebar.slider("Time Steps", 10, 200, 100)

V0 = st.sidebar.number_input("Initial Viewers (V0)", 1, N, 10)
S0 = st.sidebar.number_input("Initial Sharers (S0)", 1, N, 5)

p = st.sidebar.slider("Network Connection Probability", 0.0, 0.1, 0.02)

dt = 0.1

# -----------------------------
# DESCRIPTION
# -----------------------------
st.markdown("""
### 📖 Model Overview
This model simulates how a TikTok video spreads using:
- Growth-Decay equations
- Network influence (centrality)

Users are classified into:
- Viewers (V)
- Sharers (S)
- Passive (P)
""")

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def run_simulation(N, alpha, beta, gamma, delta, V, S, p, time_steps):
    G = nx.erdos_renyi_graph(N, p)
    centrality = np.mean(list(nx.degree_centrality(G).values()))

    V_list, S_list, P_list = [], [], []

    for _ in range(time_steps):
        dV = (alpha * S * centrality - beta * V) * dt
        dS = (gamma * V - delta * S) * dt

        V += dV
        S += dS
        P = N - (V + S)

        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    return V_list, S_list, P_list, centrality

# -----------------------------
# RUN BUTTON
# -----------------------------
if st.button("🚀 Run Simulation"):

    V_list, S_list, P_list, centrality = run_simulation(
        N, alpha, beta, gamma, delta, V0, S0, p, time_steps
    )

    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    # -----------------------------
    # METRICS (Nice UI)
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("🔥 Peak Views", int(peak_views))
    col2.metric("⏱ Peak Time", peak_time)
    col3.metric("🌐 Centrality", round(centrality, 4))

    st.markdown("---")

    # -----------------------------
    # GRAPHS (Side-by-side)
    # -----------------------------
    col1, col2 = st.columns(2)

    # Viewers
    fig1, ax1 = plt.subplots()
    ax1.plot(V_list)
    ax1.axvline(x=peak_time, linestyle='--')
    ax1.set_title("📈 Viewers")
    ax1.grid(False)
    col1.pyplot(fig1)

    # Sharers
    fig2, ax2 = plt.subplots()
    ax2.plot(S_list)
    ax2.set_title("🔁 Sharers")
    ax2.grid(False)
    col2.pyplot(fig2)

    # Passive
    fig3, ax3 = plt.subplots()
    ax3.plot(P_list)
    ax3.set_title("😴 Passive Users")
    ax3.grid(False)
    st.pyplot(fig3)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("""
### 📊 Interpretation

- Initial rise → video gaining popularity  
- Peak → maximum viral reach  
- Decline → fading interest  

Higher α and γ → stronger virality  
Higher β and δ → faster decline  
""")

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
