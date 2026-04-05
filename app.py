import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# TITLE
# -----------------------------
st.title("📱 Advanced TikTok Viral Spread Model")

st.info("Growth-Decay + Network + Influencers + Intervention Strategy")

# -----------------------------
# DESCRIPTION
# -----------------------------
st.markdown("""
### 👤 User Categories:
- Viewers (V)
- Sharers (S)
- Passive Users (P)

### 📊 Model Features:
✔ Growth-Decay Equations  
✔ Network Structure  
✔ Influencer Effect  
✔ Intervention Strategy  
✔ Peak Detection  
✔ Multiple Graphs  
""")

# -----------------------------
# PARAMETERS
# -----------------------------
st.markdown("## 🔧 Model Parameters")

N = st.slider("Total Users (N)", 100, 2000, 500)

alpha = st.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
beta = st.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
gamma = st.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)
delta = st.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

p = st.slider("Network Density (p)", 0.001, 0.1, 0.01)

time_steps = st.slider("Time Steps", 50, 300, 150)

V0 = st.number_input("Initial Viewers", 1, N, 10)
S0 = st.number_input("Initial Sharers", 1, N, 5)

# -----------------------------
# INTERVENTION STRATEGY
# -----------------------------
st.markdown("## 🚀 Intervention Strategy")

boost = st.slider("Algorithm Boost (Promotion)", 1.0, 3.0, 1.0)
suppression = st.slider("Content Suppression", 0.0, 1.0, 0.0)

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation"):

    # Create network
    G = nx.erdos_renyi_graph(N, p)

    # Centrality
    centrality_values = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality_values.values()))

    # Influencers (top 5%)
    threshold = np.percentile(list(centrality_values.values()), 95)
    influencers = [node for node, val in centrality_values.items() if val >= threshold]
    influencer_effect = len(influencers) / N

    st.write("📊 Average Centrality:", round(avg_centrality, 4))
    st.write("🌟 Number of Influencers:", len(influencers))

    # Initial values
    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []

    dt = 0.1

    # -----------------------------
    # SIMULATION LOOP
    # -----------------------------
    for t in range(time_steps):

        growth_factor = (1 + avg_centrality + influencer_effect) * boost

        dV = (alpha * S * (P/N) * growth_factor - beta * V) * dt
        dS = (gamma * V * (P/N) - delta * S) * dt

        # Apply suppression
        dV *= (1 - suppression)

        # Update values
        V += dV
        S += dS
        P = N - (V + S)

        # Avoid negative values
        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    # -----------------------------
    # PEAK ANALYSIS
    # -----------------------------
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.success(f"🔥 Peak Views: {int(peak_views)} at Time Step {peak_time}")

    # -----------------------------
    # GRAPH 1: COMBINED GRAPH
    # -----------------------------
    st.markdown("## 📊 Combined Graph")

    fig_comb, ax_comb = plt.subplots()

    ax_comb.plot(np.array(V_list)/N, label="Viewers")
    ax_comb.plot(np.array(S_list)/N, label="Sharers")
    ax_comb.plot(np.array(P_list)/N, label="Passive")

    ax_comb.axvline(x=peak_time, linestyle='--', label="Peak")

    ax_comb.set_title("Normalized Viral Spread")
    ax_comb.set_xlabel("Time")
    ax_comb.set_ylabel("Proportion")
    ax_comb.legend()
    ax_comb.grid(False)

    st.pyplot(fig_comb)

    # -----------------------------
    # GRAPH 2: VIEWERS
    # -----------------------------
    st.markdown("## 📈 Viewers Graph")

    fig_v, ax_v = plt.subplots()
    ax_v.plot(V_list)
    ax_v.axvline(x=peak_time, linestyle='--')
    ax_v.set_title("Viewers Over Time")
    ax_v.set_xlabel("Time")
    ax_v.set_ylabel("Viewers")
    ax_v.grid(False)

    st.pyplot(fig_v)

    # -----------------------------
    # GRAPH 3: SHARERS
    # -----------------------------
    st.markdown("## 🔁 Sharers Graph")

    fig_s, ax_s = plt.subplots()
    ax_s.plot(S_list)
    ax_s.set_title("Sharers Over Time")
    ax_s.set_xlabel("Time")
    ax_s.set_ylabel("Sharers")
    ax_s.grid(False)

    st.pyplot(fig_s)

    # -----------------------------
    # SCENARIO COMPARISON
    # -----------------------------
    st.markdown("## 🔍 Scenario Insights")

    st.write("""
    - High Boost → Faster viral growth 🚀  
    - High Suppression → Reduced spread 📉  
    - Dense Network → More reach 🌐  
    - More Influencers → Strong virality ⭐  
    """)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.markdown("""
## 📊 Interpretation

- Initial rise → content discovery  
- Rapid increase → viral phase  
- Peak → maximum audience reach  
- Decline → saturation and reduced engagement  

This behavior closely represents real TikTok viral trends.
""")
