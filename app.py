import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# -------------------------------
# PAGE TITLE
# -------------------------------
st.set_page_config(page_title="TikTok Viral Spread Model", layout="wide")

st.title("🎬 TikTok Viral Spread Modelling")
st.markdown("""
This simulation models how a TikTok video spreads across a social network using:

### 🔹 Model Components
- **Growth–Decay Model** → captures rise & fall of views  
- **Network Structure** → users connected as a graph  
- **User Types**:
  - 👀 Viewer (watches content)
  - 🔁 Sharer (spreads content)
  - ⚪ Passive (inactive)

### 🔹 Objective
To analyze:
- Peak virality 📈  
- Influence of network structure 🌐  
- Effect of user behavior 🔄  
""")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("⚙️ Simulation Parameters")

num_users = st.sidebar.slider("Total Users", 50, 500, 200)
initial_sharers = st.sidebar.slider("Initial Sharers", 1, 50, 5)
timesteps = st.sidebar.slider("Time Steps", 10, 100, 50)

growth_rate = st.sidebar.slider("Growth Rate", 0.1, 1.0, 0.5)
decay_rate = st.sidebar.slider("Decay Rate", 0.01, 0.5, 0.1)
share_prob = st.sidebar.slider("Sharing Probability", 0.1, 1.0, 0.3)

st.sidebar.markdown("""
### 🧠 Parameter Meaning
- **Growth Rate** → how fast video gains attention  
- **Decay Rate** → how fast interest drops  
- **Sharing Probability** → likelihood of viewers becoming sharers  
""")

# -------------------------------
# RUN SIMULATION
# -------------------------------
if st.button("🚀 Run Simulation"):

    # -------------------------------
    # NETWORK CREATION
    # -------------------------------
    G = nx.erdos_renyi_graph(num_users, 0.05)

    # Node states: 0=Passive, 1=Viewer, 2=Sharer
    states = {node: 0 for node in G.nodes()}
    initial_nodes = random.sample(list(G.nodes()), initial_sharers)

    for node in initial_nodes:
        states[node] = 2

    view_counts, share_counts, passive_counts = [], [], []

    # -------------------------------
    # SIMULATION LOOP
    # -------------------------------
    for t in range(timesteps):
        new_states = states.copy()

        for node in G.nodes():
            if states[node] == 2:  # sharer spreads
                for neighbor in G.neighbors(node):
                    if states[neighbor] == 0:
                        new_states[neighbor] = 1
                    elif states[neighbor] == 1:
                        if random.random() < share_prob:
                            new_states[neighbor] = 2

        # decay effect
        for node in G.nodes():
            if new_states[node] == 1 and random.random() < decay_rate:
                new_states[node] = 0

        states = new_states

        viewers = sum(1 for s in states.values() if s == 1)
        sharers = sum(1 for s in states.values() if s == 2)
        passive = sum(1 for s in states.values() if s == 0)

        view_counts.append(viewers)
        share_counts.append(sharers)
        passive_counts.append(passive)

    # -------------------------------
    # GROWTH-DECAY MODEL
    # -------------------------------
    time = np.arange(timesteps)
    growth_curve = (initial_sharers * np.exp(growth_rate * time)) * np.exp(-decay_rate * time)

    # -------------------------------
    # GRAPH 1: NETWORK
    # -------------------------------
    st.subheader("🌐 Network Spread Visualization")
    st.markdown("""
Shows how the video propagates through the network:
- 🔴 Sharers → actively spreading  
- 🔵 Viewers → consuming content  
- ⚪ Passive → not engaged  
""")

    fig1, ax1 = plt.subplots()
    color_map = []

    for node in G.nodes():
        if states[node] == 0:
            color_map.append('gray')
        elif states[node] == 1:
            color_map.append('blue')
        else:
            color_map.append('red')

    nx.draw(G, node_color=color_map, node_size=30, ax=ax1)
    st.pyplot(fig1)

    # -------------------------------
    # GRAPH 2: GROWTH-DECAY
    # -------------------------------
    st.subheader("📈 Growth–Decay Curve")
    st.markdown("""
This graph represents the theoretical lifecycle of a viral video:
- Initial exponential growth 🚀  
- Peak popularity 📊  
- Gradual decline 📉  
""")

    fig2, ax2 = plt.subplots()
    ax2.plot(time, growth_curve)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Views")
    st.pyplot(fig2)

    # -------------------------------
    # GRAPH 3: COMBINED
    # -------------------------------
    st.subheader("📊 Combined Simulation Analysis")
    st.markdown("""
Comparison between real simulation and theoretical model:
- Viewer growth vs sharing dynamics  
- Passive users vs engagement  
- Model prediction vs actual spread  
""")

    fig3, ax3 = plt.subplots()
    ax3.plot(time, view_counts, label="Viewers")
    ax3.plot(time, share_counts, label="Sharers")
    ax3.plot(time, passive_counts, label="Passive Users")
    ax3.plot(time, growth_curve, linestyle='--', label="Growth-Decay Model")
    ax3.legend()

    st.pyplot(fig3)

    # -------------------------------
    # INTERPRETATION
    # -------------------------------
    peak_views = max(view_counts)
    peak_time = view_counts.index(peak_views)

    centrality = nx.degree_centrality(G)
    top_nodes = sorted(centrality, key=centrality.get, reverse=True)[:5]

    st.subheader("🧠 Interpretation of Results")

    st.write(f"📌 **Peak Viewers:** {peak_views} at time step {peak_time}")

    if peak_views > num_users * 0.5:
        st.success("🔥 The video achieved VIRAL spread across the network.")
    else:
        st.warning("⚠️ The video had limited reach and did not go fully viral.")

    st.write("### 🌟 Influential Nodes (High Centrality)")
    st.write(top_nodes)

    st.markdown("""
### 📌 Key Insights
- High **growth rate** → faster virality  
- High **decay rate** → shorter lifespan  
- Influencers (high-degree nodes) amplify reach  
- Sharing probability directly impacts spread  

### 🎯 Intervention Strategies
- Target influencers for initial promotion  
- Increase engagement to reduce decay  
- Optimize content for higher share probability  
""")
