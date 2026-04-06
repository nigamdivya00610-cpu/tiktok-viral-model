import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(layout="centered")
st.title("📊 TikTok Viral Spread Model")

# -------------------------------
# 📘 MODEL DESCRIPTION
# -------------------------------
st.header("📘 Model Overview")

st.write("""
This model explains how a TikTok video spreads across users using:
- Growth–Decay mechanism
- Social network structure
- User interaction behavior
""")

st.subheader("👥 User Categories")
st.write("""
- 👀 Viewers (V): Watch the video  
- 🔁 Sharers (S): Share the video  
- 😐 Passive (P): Lose interest  
""")

st.subheader("🧠 Mathematical Model")
st.latex(r"\frac{dV}{dt} = k \cdot S \cdot \frac{(N - V)}{N} - \delta V")
st.latex(r"\frac{dS}{dt} = \beta V - \gamma S")
st.latex(r"\frac{dP}{dt} = \gamma V")

# -------------------------------
# ⚙️ INPUT PARAMETERS
# -------------------------------
st.sidebar.header("⚙️ Simulation Parameters")

N = st.sidebar.slider("Total Users (N)", 50, 1000, 200)

beta = st.sidebar.slider("β (Viewer → Sharer)", 0.0, 1.0, 0.6)
gamma = st.sidebar.slider("γ (Viewer → Passive)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay Rate)", 0.0, 1.0, 0.1)
k = st.sidebar.slider("k (Network Influence)", 0.1, 2.0, 1.0)

V0 = st.sidebar.number_input("Initial Viewers", value=10)
S0 = st.sidebar.number_input("Initial Sharers", value=5)
P0 = st.sidebar.number_input("Initial Passive", value=0)

T = st.sidebar.slider("Time Steps", 50, 300, 150)

run = st.sidebar.button("▶ Run Simulation")

# -------------------------------
# 🔁 SIMULATION FUNCTION
# -------------------------------
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

# -------------------------------
# ▶️ RUN & OUTPUT
# -------------------------------
if run:
    V, S, P, C = simulate()

    peak_views = np.max(V)
    peak_time = np.argmax(V)

    # -------- Results --------
    st.header("📈 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Views", f"{peak_views:.1f}")
    col2.metric("Peak Time", peak_time)
    col3.metric("Centrality", f"{C:.4f}")

    # -------- Interpretation --------
    st.subheader("📌 Interpretation")

    if peak_views > 0.7 * N:
        st.success("🔥 Highly Viral Spread")
    elif peak_views > 0.4 * N:
        st.info("📈 Moderate Spread")
    else:
        st.warning("📉 Low Spread")

    if beta > gamma:
        st.write("🚀 Strong sharing activity")
    else:
        st.write("⚠️ Users lose interest quickly")

    if delta > 0.3:
        st.write("⏳ High decay rate (short-lived trend)")

    if C > 0.02:
        st.write("🌐 Influencers boost spread")

    # -------- Graph 1 --------
    st.subheader("🔁 Sharers vs Passive")

    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(S, label="Sharers")
    ax1.plot(P, label="Passive")
    ax1.set_title("Sharers vs Passive Over Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Users")
    ax1.legend()

    st.pyplot(fig1)

    # -------- Graph 2 --------
    st.subheader("📊 Growth–Decay Graph")

    fig2, ax2 = plt.subplots(figsize=(5,3))
    ax2.plot(V, label="Viewers")
    ax2.plot(S, label="Sharers")
    ax2.plot(P, label="Passive")
    ax2.set_title("Growth vs Decay Dynamics")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Users")
    ax2.legend()

    st.pyplot(fig2)

# -------------------------------
# 🕸️ NETWORK INFO
# -------------------------------
st.header("🕸️ Network Structure")

st.write("""
- Users are connected in a network (graph)
- Influential users (high centrality) spread content faster
- Dense connections → fast viral growth
- Sparse connections → slow spread
""")

# -------------------------------
# 🎯 STRATEGIES
# -------------------------------
st.header("🎯 Virality Strategies")

st.write("""
- Increase β → Make content more shareable  
- Reduce γ → Improve engagement  
- Lower δ → Keep content relevant longer  
- Target influencers for faster spread  
""")
