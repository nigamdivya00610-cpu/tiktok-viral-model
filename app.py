import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📱 TikTok Viral Spread Model")

# ==========================================
# 🧠 MODEL DESCRIPTION
# ==========================================
st.markdown("""
### 📌 Model Overview
- Growth → Sharing increases viewers  
- Decay → Interest decreases  
- Users → Viewers, Sharers, Passive  
- Network → Influencers boost spread  
""")

# ==========================================
# 🎛 INPUT PARAMETERS
# ==========================================
st.sidebar.header("⚙ Parameters")

days = st.sidebar.slider("Days", 10, 100, 50)
v0 = st.sidebar.number_input("Initial Viewers", 1, 1000, 10)

r = st.sidebar.slider("Growth Rate", 0.1, 1.0, 0.5)
d = st.sidebar.slider("Decay Rate", 0.01, 0.5, 0.1)
k = st.sidebar.number_input("Max Audience", 50, 10000, 500)

share_ratio = st.sidebar.slider("Sharer Ratio", 0.1, 1.0, 0.5)

# ==========================================
# SESSION STATE (IMPORTANT)
# ==========================================
if "run_sim" not in st.session_state:
    st.session_state.run_sim = False

if st.button("▶ Run Simulation"):
    st.session_state.run_sim = True

# ==========================================
# RUN SIMULATION
# ==========================================
if st.session_state.run_sim:

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

        next_v = vt + growth - decay

        # Prevent negative values
        next_v = max(next_v, 0)

        viewers[t+1] = next_v
        sharers[t+1] = next_v * share_ratio
        passive[t+1] = next_v - sharers[t+1]

    # ==========================================
    # 📊 GRAPHS IN COLUMNS (SMALL SIZE)
    # ==========================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Viewers")
        fig1, ax1 = plt.subplots(figsize=(3.5, 2.5))
        ax1.plot(viewers)
        st.pyplot(fig1)

    with col2:
        st.subheader("Sharers vs Passive")
        fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))
        ax2.plot(sharers, label="Sharers")
        ax2.plot(passive, label="Passive")
        ax2.legend()
        st.pyplot(fig2)

    st.subheader("Combined Graph")
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    ax3.plot(viewers, label="Viewers")
    ax3.plot(sharers, label="Sharers")
    ax3.plot(passive, label="Passive")
    ax3.legend()
    st.pyplot(fig3)

    # ==========================================
    # 📌 RESULTS (BETTER DISPLAY)
    # ==========================================
    st.subheader("📌 Results")

    peak_views = np.max(viewers)
    peak_day = np.argmax(viewers)
    total_views = np.sum(viewers)

    r1, r2, r3 = st.columns(3)
    r1.metric("Peak Views", f"{peak_views:.2f}")
    r2.metric("Peak Day", peak_day)
    r3.metric("Total Views", f"{total_views:.2f}")

    # ==========================================
    # 🌐 NETWORK STRUCTURE (LAST)
    # ==========================================
    st.subheader("🌐 Network Structure")

    G = nx.erdos_renyi_graph(20, 0.2)
    degree_centrality = nx.degree_centrality(G)

    top_node = max(degree_centrality, key=degree_centrality.get)

    st.write(f"Top Influencer Node: **{top_node}**")

    fig_net, ax_net = plt.subplots(figsize=(3.5, 2.5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=400, ax=ax_net)
    st.pyplot(fig_net)

    # ==========================================
    # 📖 INTERPRETATION (SHORT & CLEAN)
    # ==========================================
    st.subheader("📖 Interpretation")

    if peak_day < days/3:
        st.write("Fast viral growth.")
    elif peak_day < 2*days/3:
        st.write("Moderate spread.")
    else:
        st.write("Slow but sustained growth.")

    if r > d:
        st.write("High virality due to strong growth.")
    else:
        st.write("Decay limits spread.")

    st.write("Influencers accelerate content reach.")
