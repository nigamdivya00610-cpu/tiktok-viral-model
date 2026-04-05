import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

st.title("📱 TikTok Viral Spread Simulation")

# =========================
# USER INPUTS
# =========================
st.sidebar.header("Input Parameters")

days = st.sidebar.slider("Number of Days", 10, 100, 50)
v0 = st.sidebar.number_input("Initial Viewers", 1, 1000, 10)

r = st.sidebar.slider("Growth Rate (Sharers)", 0.1, 1.0, 0.5)
d = st.sidebar.slider("Decay Rate (Interest Loss)", 0.01, 0.5, 0.1)
k = st.sidebar.number_input("Max Audience (K)", 50, 10000, 500)

share_ratio = st.sidebar.slider("Sharer Ratio", 0.1, 1.0, 0.5)

# =========================
# NETWORK CREATION
# =========================
st.subheader("🌐 Social Network Structure")

G = nx.erdos_renyi_graph(20, 0.2)

degree_centrality = nx.degree_centrality(G)

# Plot network
fig_net, ax_net = plt.subplots()
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=500, ax=ax_net)
st.pyplot(fig_net)

# =========================
# SIMULATION ARRAYS
# =========================
viewers = np.zeros(days)
sharers = np.zeros(days)
passive = np.zeros(days)

viewers[0] = v0
sharers[0] = v0 * share_ratio
passive[0] = v0 - sharers[0]

# =========================
# SIMULATION LOOP
# =========================
for t in range(days - 1):
    vt = viewers[t]
    
    growth = r * sharers[t] * (1 - vt / k)
    decay = d * vt
    
    new_viewers = vt + growth - decay
    
    viewers[t+1] = new_viewers
    sharers[t+1] = new_viewers * share_ratio
    passive[t+1] = new_viewers - sharers[t+1]

# =========================
# METRICS
# =========================
peak_views = np.max(viewers)
peak_day = np.argmax(viewers)
total_views = np.sum(viewers)

# Central node
top_node = max(degree_centrality, key=degree_centrality.get)

# =========================
# GRAPH 1: Viewers
# =========================
st.subheader("📊 Graph 1: Viewers Growth")

fig1, ax1 = plt.subplots()
ax1.plot(viewers)
ax1.set_title("Viewers vs Days")
ax1.set_xlabel("Days")
ax1.set_ylabel("Viewers")
st.pyplot(fig1)

# =========================
# GRAPH 2: User Types
# =========================
st.subheader("📊 Graph 2: User Types")

fig2, ax2 = plt.subplots()
ax2.plot(sharers, label="Sharers")
ax2.plot(passive, label="Passive Users")
ax2.legend()
ax2.set_title("Sharers vs Passive Users")
st.pyplot(fig2)

# =========================
# GRAPH 3: COMBINED
# =========================
st.subheader("📊 Graph 3: Combined Graph")

fig3, ax3 = plt.subplots()
ax3.plot(viewers, label="Viewers")
ax3.plot(sharers, label="Sharers")
ax3.plot(passive, label="Passive")
ax3.legend()
ax3.set_title("Combined Viral Spread")
st.pyplot(fig3)

# =========================
# RESULTS
# =========================
st.subheader("📌 Results")

st.write(f"Peak Views: {peak_views:.2f}")
st.write(f"Peak Day: {peak_day}")
st.write(f"Total Views: {total_views:.2f}")
st.write(f"Top Influencer Node: {top_node}")

# =========================
# INTERPRETATION (ONLY RESULT)
# =========================
st.subheader("📖 Interpretation")

if peak_day < days/3:
    st.write("Video spreads quickly and peaks early.")
elif peak_day < 2*days/3:
    st.write("Video shows moderate viral growth.")
else:
    st.write("Video spreads slowly but sustains longer.")

if d > r:
    st.write("High decay reduces virality quickly.")
else:
    st.write("Growth dominates → higher viral potential.")

st.write("Nodes with high centrality act as influencers boosting spread.")
