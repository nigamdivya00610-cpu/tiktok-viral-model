import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="centered")
st.title("📊 TikTok Viral Spread Model")

# -----------------------------
# 📘 THEORY SECTION (ADDED)
# -----------------------------
st.markdown("## 📘 Model Overview")

st.write("""
This model simulates how a TikTok video spreads in a social network by combining:

- 📈 Growth–Decay dynamics (how content grows and fades)
- 🕸️ Network structure (how users are connected)
- 👥 User behavior (viewers, sharers, passive users)

The goal is to understand how videos become viral and what factors influence their reach.
""")

st.markdown("### 👥 User Types")

st.write("""
- 👀 **Viewers (V):** Users who watch the video  
- 🔁 **Sharers (S):** Users who share the video and increase reach  
- 😐 **Passive (P):** Users who lose interest and stop engaging  
""")

st.markdown("### 🧠 Model Equations")

st.latex(r"dV/dt = k \cdot S \cdot (N - V)/N - \delta V")
st.latex(r"dS/dt = \beta V - \gamma S")
st.latex(r"dP/dt = \gamma V")

st.write("""
- **β (beta):** Probability of viewers becoming sharers  
- **γ (gamma):** Rate at which users lose interest  
- **δ (delta):** Decay rate of the trend  
- **k:** Network influence factor  
""")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("🔧 Parameters")

N = st.sidebar.slider("Total Users (N)", 50, 1000, 200)

beta = st.sidebar.slider("β (Viewer → Sharer)", 0.0, 1.0, 0.6)
gamma = st.sidebar.slider("γ (Viewer → Passive)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay)", 0.0, 1.0, 0.1)
k = st.sidebar.slider("k (Network Influence)", 0.1, 2.0, 1.0)

V0 = st.sidebar.number_input("Initial Viewers", value=10)
S0 = st.sidebar.number_input("Initial Sharers", value=5)
P0 = st.sidebar.number_input("Initial Passive", value=0)

T = st.sidebar.slider("Time Steps", 50, 300, 150)

run = st.sidebar.button("▶ Run Simulation")

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate():
    G = nx.erdos_renyi_graph(N, 0.03)

    centrality = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality.values()))

    k_eff = k * (1 + avg_centrality)

    V = np.zeros(T)
    S = np.zeros(T)
    P = np.zeros(T)

    V[0], S[0], P[0] = V0, S0, P0

    dt = 0.1

    for t in range(1, T):
        dV = k_eff * S[t-1] * ((N - V[t-1]) / N) - delta * V[t-1]
        dS = beta * V[t-1] - gamma * S[t-1]
        dP = gamma * V[t-1]

        V[t] = max(V[t-1] + dV * dt, 0)
        S[t] = max(S[t-1] + dS * dt, 0)
        P[t] = max(P[t-1] + dP * dt, 0)

    return V, S, P, avg_centrality

# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    V, S, P, C = simulate()

    peak_views = np.max(V)
    peak_time = np.argmax(V)

    # -----------------------------
    # RESULTS + INTERPRETATION
    # -----------------------------
    st.subheader("📈 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Views", f"{peak_views:.1f}")
    col2.metric("Peak Time", peak_time)
    col3.metric("Centrality", f"{C:.4f}")

    st.markdown("### 📌 Interpretation")

    if peak_views > 0.7 * N:
        st.success("🔥 Highly Viral: Video spreads to most users")
    elif peak_views > 0.4 * N:
        st.info("📈 Moderate Spread: Good engagement")
    else:
        st.warning("📉 Low Spread: Limited reach")

    if beta > gamma:
        st.write("🚀 Strong sharing behavior")
    else:
        st.write("⚠️ Users becoming passive quickly")

    if delta > 0.3:
        st.write("⏳ High decay: Trend fades fast")

    if C > 0.02:
        st.write("🌐 Influencers boosting spread")

    # -----------------------------
    # GRAPH 1: Sharers & Passive
    # -----------------------------
    st.subheader("🔁 Sharers vs Passive")

    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(S, label="Sharers")
    ax1.plot(P, label="Passive")
    ax1.legend()
    ax1.set_title("Sharers vs Passive Over Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Users")

    st.pyplot(fig1)

    # -----------------------------
    # GRAPH 2: Growth-Decay
    # -----------------------------
    st.subheader("📊 Growth-Decay Graph")

    fig2, ax2 = plt.subplots(figsize=(5,3))
    ax2.plot(V, label="Viewers")
    ax2.plot(S, label="Sharers")
    ax2.plot(P, label="Passive")
    ax2.legend()
    ax2.set_title("Growth vs Decay Dynamics")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Users")

    st.pyplot(fig2)

# -----------------------------
# 🕸️ NETWORK EXPLANATION (ADDED)
# -----------------------------
st.markdown("## 🕸️ Network Structure")

st.write("""
- Each node represents a user  
- Each edge represents a connection (followers/friends)  
- High centrality nodes = influencers  
- Dense networks → faster spread  
- Sparse networks → slower spread  
""")

# -----------------------------
# 🎯 STRATEGIES (ADDED)
# -----------------------------
st.markdown("## 🎯 How to Make a Video Go Viral")

st.write("""
### 🚀 Increase Virality
- Improve content quality (increase β)
- Use trending sounds and hashtags
- Target influencers early

### ⚠️ Reduce Drop-Off
- Hook viewers in first 3 seconds
- Maintain engagement throughout

### ⏳ Reduce Decay
- Post consistently
- Follow trends

### 🌐 Network Strategy
- Collaborate with creators
- Share in communities
""")
