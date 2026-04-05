import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📱 TikTok Viral Spread Model")

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
    # PLOT GRAPH
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
    ax.grid()

    st.pyplot(fig)
