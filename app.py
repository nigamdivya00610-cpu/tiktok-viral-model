import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📈 TikTok Viral Spread Simulation")

# -----------------------------
# USER INPUTS
# -----------------------------
st.sidebar.header("Model Parameters")

N = st.sidebar.number_input("Total Users (N)", value=1000)
beta = st.sidebar.slider("β (Viewer → Sharer rate)", 0.0, 1.0, 0.3)
gamma = st.sidebar.slider("γ (Viewer → Passive rate)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("δ (Decay rate)", 0.0, 1.0, 0.1)
k = st.sidebar.slider("k (Network Influence)", 0.0, 2.0, 1.0)

# Initial values
V0 = st.sidebar.number_input("Initial Viewers", value=10)
S0 = st.sidebar.number_input("Initial Sharers", value=5)
P0 = st.sidebar.number_input("Initial Passive", value=0)

T = st.sidebar.slider("Time Steps", 10, 200, 100)

# -----------------------------
# NETWORK STRUCTURE
# -----------------------------
st.subheader("🌐 Network Structure")

G = nx.erdos_renyi_graph(N, 0.01)

# Centrality
centrality = nx.degree_centrality(G)
avg_centrality = np.mean(list(centrality.values()))

st.write(f"Average Network Centrality: {avg_centrality:.4f}")

# Modify influence using centrality
k_effective = k * (1 + avg_centrality)

# -----------------------------
# SIMULATION
# -----------------------------
V = np.zeros(T)
S = np.zeros(T)
P = np.zeros(T)

V[0], S[0], P[0] = V0, S0, P0

dt = 1

for t in range(1, T):
    dV = k_effective * S[t-1] * ((N - V[t-1]) / N) - delta * V[t-1]
    dS = beta * V[t-1] - gamma * S[t-1]
    dP = gamma * V[t-1]

    V[t] = max(V[t-1] + dV * dt, 0)
    S[t] = max(S[t-1] + dS * dt, 0)
    P[t] = max(P[t-1] + dP * dt, 0)

# -----------------------------
# PEAK ANALYSIS
# -----------------------------
peak_views = np.max(V)
peak_time = np.argmax(V)

st.write(f"📊 Peak Views: {peak_views:.2f} at time {peak_time}")

# -----------------------------
# PLOTS
# -----------------------------
st.subheader("📉 Graphs")

# Graph 1: Viewers
fig1, ax1 = plt.subplots()
ax1.plot(V)
ax1.set_title("Viewers Over Time")
st.pyplot(fig1)

# Graph 2: Sharers + Passive
fig2, ax2 = plt.subplots()
ax2.plot(S, label="Sharers")
ax2.plot(P, label="Passive")
ax2.legend()
ax2.set_title("Sharers and Passive Users")
st.pyplot(fig2)

# Graph 3: Combined
fig3, ax3 = plt.subplots()
ax3.plot(V, label="Viewers")
ax3.plot(S, label="Sharers")
ax3.plot(P, label="Passive")
ax3.legend()
ax3.set_title("Combined Dynamics")
st.pyplot(fig3)

# -----------------------------
# INTERPRETATION
# -----------------------------
st.subheader("📌 Interpretation")

if peak_views > N * 0.6:
    st.write("🔥 The video went highly viral reaching a large portion of the network.")
elif peak_views > N * 0.3:
    st.write("📈 Moderate virality observed with significant spread.")
else:
    st.write("📉 Low virality — content did not spread widely.")

if delta > 0.3:
    st.write("⚠️ High decay rate reduced long-term engagement.")
    
if beta > gamma:
    st.write("🚀 More viewers are converting into sharers → strong viral growth.")

if avg_centrality > 0.01:
    st.write("🌐 Strong network connectivity boosted spread via influencers.")

# -----------------------------
# NETWORK VISUALIZATION
# -----------------------------
st.subheader("🕸️ Network Graph")

fig_net, ax_net = plt.subplots()
nx.draw(G, node_size=10, ax=ax_net)
st.pyplot(fig_net)
