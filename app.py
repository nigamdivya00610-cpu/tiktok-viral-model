import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(page_title="TikTok Viral Model", layout="wide")
st.title("📱 TikTok Viral Spread Model Pro")

# ==========================================
# 🧠 MODEL DESCRIPTION
# ==========================================
with st.expander("📌 View Model Logic"):
    st.write("""
    This enhanced model simulates viral spread using:
    - **Stochastic Growth:** Adds randomness to daily view counts.
    - **Influencer Factor:** Network centrality now directly impacts peak potential.
    - **Saturation (K):** Represents the 'For You Page' limit for a specific niche.
    """)

# ==========================================
# 🎛 INPUT PARAMETERS
# ==========================================
st.sidebar.header("Control Panel")
days = st.sidebar.slider("Simulation Duration (Days)", 10, 150, 60)
v0 = st.sidebar.number_input("Seed Viewers", 1, 1000, 50)
r = st.sidebar.slider("Base Growth Rate", 0.1, 2.0, 0.8)
d = st.sidebar.slider("Content Decay Rate", 0.01, 0.5, 0.15)
k = st.sidebar.number_input("Niche Max Audience (K)", 100, 50000, 5000)

st.sidebar.markdown("---")
influencer_boost = st.sidebar.checkbox("Enable Influencer Boost", value=True)
boost_strength = st.sidebar.slider("Boost Intensity", 1.1, 3.0, 1.5) if influencer_boost else 1.0

# ==========================================
# ▶ RUN SIMULATION
# ==========================================
if st.button("▶ Run Viral Simulation"):
    
    # Generate Network first to get Influencer Data
    G = nx.powerlaw_cluster_graph(50, 2, 0.1) # More realistic social network
    centrality = nx.degree_centrality(G)
    top_node = max(centrality, key=centrality.get)
    # The 'influence' is based on how connected the top node is
    network_power = centrality[top_node] * boost_strength

    # Arrays for simulation
    viewers = np.zeros(days)
    viewers[0] = v0

    for t in range(days - 1):
        vt = viewers[t]
        
        # Add randomness (Stochasticity) to growth
        noise = np.random.normal(1, 0.2) 
        
        # Growth logic: influenced by network power if boost is enabled
        effective_r = r * network_power if influencer_boost else r
        
        growth = effective_r * vt * (1 - vt / k) * noise
        decay = d * vt
        
        viewers[t+1] = max(0, vt + growth - decay)

    # ==========================================
    # 📈 VISUALIZATION
    # ==========================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Growth Curve")
        fig1, ax1 = plt.subplots()
        ax1.fill_between(range(days), viewers, color="skyblue", alpha=0.4)
        ax1.plot(viewers, color="dodgerblue", lw=2)
        ax1.set_xlabel("Days")
        ax1.set_ylabel("Total Viewers")
        st.pyplot(fig1)

    with col2:
        st.subheader("🌐 Social Graph")
        fig_net, ax_net = plt.subplots()
        node_colors = ['red' if n == top_node else 'gray' for n in G.nodes()]
        nx.draw(G, pos=nx.spring_layout(G), with_labels=False, 
                node_size=50, node_color=node_colors, ax=ax_net, alpha=0.7)
        st.pyplot(fig_net)

    # ==========================================
    # 📌 RESULTS & ANALYTICS
    # ==========================================
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Peak Views", f"{np.max(viewers):,.0f}")
    res_col2.metric("Viral Peak Day", int(np.argmax(viewers)))
    res_col3.metric("Influencer Node", f"ID: {top_node}")

    if np.max(viewers) >= k * 0.8:
        st.success("🔥 **CRITICAL VIRALITY:** You've saturated the niche audience!")
    else:
        st.info("📉 **Niche Content:** The video reached a steady audience but didn't break the algorithm.")
