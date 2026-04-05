import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Page Config
st.set_page_config(page_title="TikTok Viral Model", layout="wide")
st.title("📊 TikTok Viral Spread Model (Pro)")

# -----------------------------
# SIDEBAR PARAMETERS
# -----------------------------
with st.sidebar:
    st.header("🔧 Model Parameters")
    N = st.number_input("Total Population (N)", value=1000, step=100)
    
    col_params = st.columns(2)
    beta = col_params[0].slider("β (Sharing Rate)", 0.0, 1.0, 0.4)
    gamma = col_params[1].slider("γ (Boredom Rate)", 0.0, 1.0, 0.2)
    
    delta = st.slider("δ (Content Decay/Algorithm Drop)", 0.0, 1.0, 0.1)
    k_input = st.slider("k (Algo Amplification)", 0.1, 5.0, 1.5)

    st.divider()
    V0 = st.number_input("Initial Viewers", value=10)
    S0 = st.number_input("Initial Sharers", value=5)
    T_max = st.slider("Time Horizon", 50, 500, 150)
    
    run = st.button("▶ Run Simulation", type="primary", use_container_width=True)

# -----------------------------
# SIMULATION ENGINE
# -----------------------------
def run_simulation():
    # Generate a more realistic social network (Scale-Free)
    # We use a subset for centrality calculation to keep it fast
    G = nx.barabasi_albert_graph(min(N, 500), 2)
    centrality = nx.degree_centrality(G)
    avg_centrality = np.mean(list(centrality.values()))
    
    # Effective Influence: Algorithm k * Network Structure
    k_eff = k_input * (1 + avg_centrality)

    # State vectors
    V, S, P = np.zeros(T_max), np.zeros(T_max), np.zeros(T_max)
    V[0], S[0], P[0] = V0, S0, 0

    dt = 0.1 
    for t in range(1, T_max):
        # Differential equations for spread
        # New Viewers = k * Sharers * (Remaining Pool) - Decay
        dV = k_eff * S[t-1] * ((N - V[t-1]) / N) - delta * V[t-1]
        # New Sharers = Viewer conversion - Sharer attrition
        dS = beta * V[t-1] - gamma * S[t-1]
        # Passive (History)
        dP = gamma * V[t-1]

        V[t] = max(V[t-1] + dV * dt, 0)
        S[t] = max(S[t-1] + dS * dt, 0)
        P[t] = max(P[t-1] + dP * dt, 0)

    return V, S, P, avg_centrality, G

# -----------------------------
# DASHBOARD EXECUTION
# -----------------------------
if run:
    V, S, P, avg_C, G_sample = run_simulation()
    
    # 1. Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    peak_v = np.max(V)
    m1.metric("Peak Reach", f"{peak_v:.0f} users")
    m2.metric("Peak Time", f"T={np.argmax(V)}")
    m3.metric("Network Density", f"{avg_C:.4f}")
    m4.metric("Virality Score", "High" if peak_v > N*0.6 else "Low")

    st.divider()

    # 2. Main Graphs
    col_graph, col_net = st.columns([2, 1])

    with col_graph:
        st.subheader("📈 Engagement Over Time")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.fill_between(range(T_max), V, color="skyblue", alpha=0.3, label="Viewers (Reach)")
        ax.plot(V, color="dodgerblue", lw=2)
        ax.plot(S, color="red", lw=2, label="Sharers (Active)")
        ax.plot(P, color="gray", linestyle="--", alpha=0.5, label="Passive")
        
        ax.set_xlabel("Time")
        ax.set_ylabel("User Count")
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)

    with col_net:
        st.subheader("🕸️ Viral Hubs")
        # Visualizing a representative sub-graph
        fig_net, ax_net = plt.subplots(figsize=(5, 5))
        pos = nx.spring_layout(G_sample, k=0.2)
        
        # Color nodes by their importance (degree)
        d = dict(G_sample.degree)
        nx.draw(G_sample, pos, 
                node_size=[v * 10 for v in d.values()], 
                node_color=list(d.values()), 
                cmap=plt.cm.magma,
                edge_color="#EEEEEE",
                width=0.5,
                with_labels=False)
        st.pyplot(fig_net)

    # 3. Automated Insight
    st.subheader("📌 Strategy Insights")
    if beta > gamma * 1.5:
        st.success("🚀 **Highly Shareable:** Your 'Conversion to Sharer' is high. This content has 'hook' potential.")
    if delta > 0.4:
        st.warning("⏱️ **Fast Decay:** The algorithm is dropping this quickly. Consider a 'Part 2' to keep momentum.")
    if avg_C > 0.05:
        st.info("🌐 **Hub Effect:** The network is tight. One 'Big Influencer' share will cause an exponential spike.")
else:
    st.info("Adjust the parameters in the sidebar and click 'Run Simulation' to see the viral trajectory.")
