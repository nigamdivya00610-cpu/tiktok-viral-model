import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📱 TikTok Viral Spread Model")

# ==========================================
# 🧠 MODEL DESCRIPTION
# ==========================================
st.header("📌 Model Description")

st.write("""
This model simulates viral spread of a TikTok video using:
- Growth (sharing increases views)
- Decay (loss of interest)
- User types: Viewers, Sharers, Passive users
- Network influence (central nodes boost spread)
""")

# ==========================================
# 🎛 INPUT PARAMETERS
# ==========================================
st.sidebar.header("Input Parameters")

days = st.sidebar.slider("Days", 10, 100, 50)
v0 = st.sidebar.number_input("Initial Viewers", 1, 1000, 10)

r = st.sidebar.slider("Growth Rate", 0.1, 1.0, 0.5)
d = st.sidebar.slider("Decay Rate", 0.01, 0.5, 0.1)
k = st.sidebar.number_input("Max Audience", 50, 10000, 500)

share_ratio = st.sidebar.slider("Sharer Ratio", 0.1, 1.0, 0.5)

# ==========================================
# ▶ RUN BUTTON
# ==========================================
run = st.button("▶ Run Simulation")

if run:

    # ==========================================
    # 📊 SIMULATION
    # ==========================================
    viewers = np.zeros(days)
    sharers = np.zeros(days)
    passive = np.zeros(days)

    viewers[0] = v0
    sharers[0] = v0 * share_ratio
    passive[0] = v0 - sharers[0]

    for t in range(days - 1):
        vt = viewers[t]

        growth = r * sharers[t] * (1 - vt / k)
        decay = d * vt

        viewers[t+1] = vt + growth - decay
        sharers[t+1] = viewers[t+1] * share_ratio
        passive[t+1] = viewers[t+1] - sharers[t+1]

    # ==========================================
    # 📈 SMALL GRAPHS
    # ==========================================
    st.subheader("📊 Graph 1: Viewers")

    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.plot(viewers)
    ax1.set_title("Viewers vs Days")
    st.pyplot(fig1)

    st.subheader("📊 Graph 2: User Types")

    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.plot(sharers, label="Sharers")
    ax2.plot(passive, label="Passive")
    ax2.legend()
    st.pyplot(fig2)

    st.subheader("📊 Graph 3: Combined")

    fig3, ax3 = plt.subplots(figsize=(4, 3))
    ax3.plot(viewers, label="Viewers")
    ax3.plot(sharers, label="Sharers")
    ax3.plot(passive, label="Passive")
    ax3.legend()
    st.pyplot(fig3)

    # ==========================================
    # 📌 RESULTS
    # ==========================================
    st.header("📌 Results")

    peak_views = np.max(viewers)
    peak_day = np.argmax(viewers)
    total_views = np.sum(viewers)

    st.write(f"Peak Views: {peak_views:.2f}")
    st.write(f"Peak Day: {peak_day}")
    st.write(f"Total Views: {total_views:.2f}")

    # ==========================================
    # 🌐 NETWORK STRUCTURE (LAST)
    # ==========================================
    st.header("🌐 Network Structure")

    G = nx.erdos_renyi_graph(20, 0.2)

    degree_centrality = nx.degree_centrality(G)
    top_node = max(degree_centrality, key=degree_centrality.get)

    st.write(f"Top Influencer Node: {top_node}")

    fig_net, ax_net = plt.subplots(figsize=(4, 3))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=400, ax=ax_net)
    st.pyplot(fig_net)

    # ==========================================
    # 📖 INTERPRETATION
    # ==========================================
    st.header("📖 Interpretation")

    if peak_day < days/3:
        st.write("Fast viral growth observed.")
    elif peak_day < 2*days/3:
        st.write("Moderate viral spread.")
    else:
        st.write("Slow but sustained spread.")

    if r > d:
        st.write("Growth dominates → high virality.")
    else:
        st.write("Decay dominates → short-lived trend.")

    st.write("Influencers (high centrality nodes) boost video spread.")
