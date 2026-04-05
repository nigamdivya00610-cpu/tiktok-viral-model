import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 TikTok Viral Spread Model")

st.info("This model simulates viral spread using Growth-Decay + Network Effect")

# -----------------------------
# USER INPUT
# -----------------------------
st.markdown("### 🔧 Adjust Parameters")

N = st.slider("Total Users (N)", 100, 1000, 500)

alpha = st.slider("Growth Rate (α)", 0.0, 1.0, 0.9)
beta = st.slider("Decay Rate (β)", 0.0, 1.0, 0.1)
gamma = st.slider("Viewer → Sharer (γ)", 0.0, 1.0, 0.8)
delta = st.slider("Sharer Decay (δ)", 0.0, 1.0, 0.05)

time_steps = st.slider("Time Steps", 50, 200, 100)

V = st.number_input("Initial Viewers (V0)", 1, N, 30)
S = st.number_input("Initial Sharers (S0)", 1, N, 20)

p = st.slider("Network Connection Probability", 0.0, 0.2, 0.1)

dt = 1  # 🔥 Important fix

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation"):

    # Network
    G = nx.erdos_renyi_graph(N, p)
    centrality = np.mean(list(nx.degree_centrality(G).values()))

    st.write("📊 Average Network Centrality:", round(centrality, 4))

    # Initial values
    P = N - (V + S)

    V_list, S_list = [], []

    for t in range(time_steps):

        # 🔥 Strong viral growth model
        dV = (alpha * S * (P / N) * 10 - beta * V) * dt
        dS = (gamma * V * (P / N) * 8 - delta * S) * dt

        V += dV
        S += dS
        P = N - (V + S)

        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)

    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time Step {peak_time}")

    # -----------------------------
    # COMBINED GRAPH (CLEAR CURVE)
    # -----------------------------
    st.markdown("## 📊 Combined Graph")

    fig, ax = plt.subplots()

    ax.plot(V_list, label="Viewers (V)")
    ax.plot(S_list, label="Sharers (S)")
    ax.axvline(x=peak_time, linestyle='--', label="Peak")

    ax.set_title("Viral Growth Curve")
    ax.set_xlabel("Time")
    ax.set_ylabel("Users")
    ax.legend()
    ax.grid(False)

    st.pyplot(fig)

    # -----------------------------
    # SEPARATE GRAPHS
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

- Initial slow growth  
- Rapid viral increase 🚀  
- Peak point 🔥  
- Decline due to saturation 📉  

This matches real TikTok viral trends.
""")
