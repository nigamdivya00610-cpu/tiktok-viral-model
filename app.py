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

### 👤 User Categories:
- Viewers (V)
- Sharers (S)
- Passive Users (P)
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

    # Network
    G = nx.erdos_renyi_graph(N, p)
    centrality = np.mean(list(nx.degree_centrality(G).values()))

    st.write("📊 Average Network Centrality:", round(centrality, 4))

    # Initialize P correctly ✅
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []

    for t in range(time_steps):

        # ✅ Improved viral formula (with network + audience)
        dV = (alpha * S * (P / N) * (1 + centrality) - beta * V) * dt
        dS = (gamma * V * (P / N) - delta * S) * dt

        V += dV
        S += dS
        P = N - (V + S)

        # Avoid negatives
        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time Step {peak_time}")

    # -----------------------------
    # GRAPHICAL RESULTS
    # -----------------------------
    st.markdown("## 📊 Graphical Results")

    # ✅ Combined Graph (Normalized for better curve)
    fig_comb, ax_comb = plt.subplots()

    ax_comb.plot(np.array(V_list)/N, label="Viewers")
    ax_comb.plot(np.array(S_list)/N, label="Sharers")
    ax_comb.plot(np.array(P_list)/N, label="Passive")

    ax_comb.axvline(x=peak_time, linestyle='--', label="Peak")

    ax_comb.set_title("📊 Combined Graph (Normalized)")
    ax_comb.set_xlabel("Time")
    ax_comb.set_ylabel("Proportion")
    ax_comb.legend()
    ax_comb.grid(False)

    st.pyplot(fig_comb)

    # -----------------------------
    # Separate Graphs
    # -----------------------------

    # Viewers
    fig1, ax1 = plt.subplots()
    ax1.plot(V_list)
    ax1.axvline(x=peak_time, linestyle='--')
    ax1.set_title("📈 Viewers Curve")
    ax1.grid(False)
    st.pyplot(fig1)

    # Sharers
    fig2, ax2 = plt.subplots()
    ax2.plot(S_list)
    ax2.set_title("🔁 Sharers Curve")
    ax2.grid(False)
    st.pyplot(fig2)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("""
## 📊 Interpretation

- Curve rises → viral growth  
- Peak → maximum reach  
- Decline → saturation  

This matches real TikTok viral behavior.
""").
