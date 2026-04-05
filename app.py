import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📱 TikTok Viral Spread Model")

# =========================
# INPUT
# =========================
st.sidebar.header("Parameters")

days = st.sidebar.slider("Days", 10, 100, 50)
v0 = st.sidebar.number_input("Initial Viewers", 1, 1000, 10)

r = st.sidebar.slider("Growth Rate", 0.1, 1.0, 0.5)
d = st.sidebar.slider("Decay Rate", 0.01, 0.5, 0.1)
k = st.sidebar.number_input("Max Audience", 50, 10000, 500)

share_ratio = st.sidebar.slider("Sharer Ratio", 0.1, 1.0, 0.5)

run = st.button("▶ Run Simulation")

# =========================
# RUN
# =========================
if run:

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

        next_v = max(vt + growth - decay, 0)

        viewers[t+1] = next_v
        sharers[t+1] = next_v * share_ratio
        passive[t+1] = next_v - sharers[t+1]

    # =========================
    # GRAPH 1 (FIXED)
    # =========================
    st.subheader("📊 Viewers Growth")

    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(range(days), viewers, linewidth=2)
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Viewers")
    ax1.grid(True)
    fig1.tight_layout()
    st.pyplot(fig1)

    # =========================
    # GRAPH 2 (FIXED)
    # =========================
    st.subheader("📊 User Types")

    fig2, ax2 = plt.subplots(figsize=(5,3))
    ax2.plot(range(days), sharers, label="Sharers", linewidth=2)
    ax2.plot(range(days), passive, label="Passive", linewidth=2)
    ax2.set_xlabel("Days")
    ax2.set_ylabel("Users")
    ax2.legend()
    ax2.grid(True)
    fig2.tight_layout()
    st.pyplot(fig2)

    # =========================
    # GRAPH 3 (FIXED BEST)
    # =========================
    st.subheader("📊 Combined Graph")

    fig3, ax3 = plt.subplots(figsize=(5,3))
    ax3.plot(range(days), viewers, label="Viewers", linewidth=2)
    ax3.plot(range(days), sharers, label="Sharers", linewidth=2)
    ax3.plot(range(days), passive, label="Passive", linewidth=2)
    ax3.set_xlabel("Days")
    ax3.set_ylabel("Count")
    ax3.legend()
    ax3.grid(True)
    fig3.tight_layout()
    st.pyplot(fig3)

    # =========================
    # RESULTS
    # =========================
    peak_views = np.max(viewers)
    peak_day = np.argmax(viewers)
    total_views = np.sum(viewers)

    st.write("### 📌 Results")
    st.write(f"Peak Views: {peak_views:.2f}")
    st.write(f"Peak Day: {peak_day}")
    st.write(f"Total Views: {total_views:.2f}")

    # =========================
    # NETWORK
    # =========================
    st.write("### 🌐 Network Structure")

    G = nx.erdos_renyi_graph(20, 0.2)
    degree_centrality = nx.degree_centrality(G)

    top_node = max(degree_centrality, key=degree_centrality.get)

    st.write(f"Top Influencer Node: {top_node}")

    fig_net, ax_net = plt.subplots(figsize=(5,3))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=400, ax=ax_net)
    fig_net.tight_layout()
    st.pyplot(fig_net)

    # =========================
    # INTERPRETATION
    # =========================
    st.write("### 📖 Interpretation")

    if peak_day < days/3:
        st.write("Fast viral growth.")
    elif peak_day < 2*days/3:
        st.write("Moderate spread.")
    else:
        st.write("Slow but sustained spread.")

    if r > d:
        st.write("Growth dominates → high virality.")
    else:
        st.write("Decay dominates → short-lived trend.")
