import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown("""
<style>
.title {
    font-size:40px;
    font-weight:bold;
    color:#ff0050;
}
.subtitle {
    font-size:18px;
    color:gray;
}
.section {
    font-size:24px;
    font-weight:bold;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<p class="title">📱 TikTok Viral Spread Simulator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Growth-Decay Model</p>', unsafe_allow_html=True)

# -----------------------------
# TOPIC CONTENT
# -----------------------------
st.markdown("## 📱 Trending Video Spread on TikTok Modelling")

st.markdown("""
This project models how a video becomes viral on TikTok using a mathematical approach.

The spread of a video is treated as a dynamic process where users interact with content over time. The model divides the population into three main groups:

- 👀 **Viewers (V):** Users who are watching the video  
- 🔁 **Sharers (S):** Users who actively share the video  
- 😶 **Passive Users (P):** Users who have not yet seen the video  

The model is based on a **Growth-Decay mechanism**:

- 📈 **Growth:** Sharers increase the number of viewers by spreading the content  
- 📉 **Decay:** Users gradually lose interest and stop engaging  

The interaction between these groups determines how fast and how widely a video spreads.

The model also helps identify:
- 🔥 Peak Views  
- ⏱ Peak Time  
- 📊 Engagement behavior  
""")

# -----------------------------
# PARAMETERS
# -----------------------------
st.markdown('<p class="section">🔧 Model Parameters</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    N = st.slider("Total Users (N)", 100, 2000, 500)
    V0 = st.number_input("Initial Viewers", 1, N, 10)

with col2:
    alpha = st.slider("Growth Rate (α)", 0.1, 1.0, 0.8)
    gamma = st.slider("Viewer → Sharer (γ)", 0.1, 1.0, 0.6)

with col3:
    beta = st.slider("Decay Rate (β)", 0.01, 0.5, 0.1)
    delta = st.slider("Sharer Decay (δ)", 0.01, 0.5, 0.2)

col4, col5 = st.columns(2)

with col4:
    time_steps = st.slider("Time Steps", 50, 300, 150)

with col5:
    S0 = st.number_input("Initial Sharers", 1, N, 5)

# -----------------------------
# RUN BUTTON
# -----------------------------
st.markdown("### ▶ Run Simulation")
run = st.button("Run Simulation 🚀")

# -----------------------------
# SIMULATION
# -----------------------------
if run:

    progress = st.progress(0)

    V, S = V0, S0
    P = N - (V + S)

    V_list, S_list, P_list = [], [], []

    dt = 0.1

    for t in range(time_steps):

        progress.progress((t + 1) / time_steps)

        dV = (alpha * S * (P/N) - beta * V) * dt
        dS = (gamma * V * (P/N) - delta * S) * dt

        V += dV
        S += dS
        P = N - (V + S)

        V = max(V, 0)
        S = max(S, 0)
        P = max(P, 0)

        V_list.append(V)
        S_list.append(S)
        P_list.append(P)

    # -----------------------------
    # METRICS
    # -----------------------------
    peak_views = max(V_list)
    peak_time = V_list.index(peak_views)

    st.markdown("## 📊 Key Metrics")

    m1, m2 = st.columns(2)
    m1.metric("🔥 Peak Views", int(peak_views))
    m2.metric("⏱ Peak Time", peak_time)

    # -----------------------------
    # GRAPHS
    # -----------------------------
    st.markdown("## 📈 Simulation Results")

    g1, g2 = st.columns(2)

    with g1:
        fig1, ax1 = plt.subplots()
        ax1.plot(np.array(V_list)/N, label="Viewers", color='red')
        ax1.plot(np.array(S_list)/N, label="Sharers", color='blue')
        ax1.plot(np.array(P_list)/N, label="Passive", color='green')
        ax1.axvline(x=peak_time, linestyle='--')
        ax1.set_title("Viral Spread (Normalized)")
        ax1.legend()
        st.pyplot(fig1)

    with g2:
        fig2, ax2 = plt.subplots()
        ax2.plot(V_list, color='red')
        ax2.axvline(x=peak_time, linestyle='--')
        ax2.set_title("Viewers Over Time")
        st.pyplot(fig2)

    fig3, ax3 = plt.subplots()
    ax3.plot(S_list, color='blue')
    ax3.set_title("Sharers Over Time")
    st.pyplot(fig3)

    # -----------------------------
    # DYNAMIC INTERPRETATION
    # -----------------------------
    st.markdown("Interpretation")

    insights = []

    if peak_time < time_steps * 0.3:
        insights.append("🚀 The video spreads very quickly and becomes viral early.")
    elif peak_time < time_steps * 0.7:
        insights.append("📈 The video shows steady growth before reaching peak.")
    else:
        insights.append("🐢 The video spreads slowly and takes time to gain attention.")

    if peak_views > 0.6 * N:
        insights.append("🔥 The video achieves high virality and reaches most users.")
    elif peak_views > 0.3 * N:
        insights.append("⚡ The video achieves moderate popularity.")
    else:
        insights.append("📉 The video has limited reach and does not go strongly viral.")

    if alpha > beta:
        insights.append("💡 Growth rate is higher than decay, so engagement is sustained.")
    else:
        insights.append("⛔ High decay reduces user interest quickly.")

    if gamma > delta:
        insights.append("🔁 Users actively share the content, boosting spread.")
    else:
        insights.append("📉 Sharing is limited, reducing virality.")

    for i in insights:
        st.write(i)
