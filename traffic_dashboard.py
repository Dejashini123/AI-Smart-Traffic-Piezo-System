import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Traffic AI", layout="wide")

st.title("🚦 AI Smart Traffic Control System")

# SIDEBAR
st.sidebar.header("Traffic Input")

north = st.sidebar.slider("North Lane", 0, 200, 80)
south = st.sidebar.slider("South Lane", 0, 200, 40)
east  = st.sidebar.slider("East Lane", 0, 200, 60)
west  = st.sidebar.slider("West Lane", 0, 200, 20)

emergency = st.sidebar.checkbox("🚑 Emergency Mode")
lane = st.sidebar.selectbox("Priority Lane", ["None","North","South","East","West"])

lanes = {"North":north,"South":south,"East":east,"West":west}

# AI LOGIC
total = sum(lanes.values())
TOTAL_TIME = 120
MIN_GREEN = 10

green_times = []

if emergency and lane != "None":
    for l in lanes:
        green_times.append(80 if l==lane else 10)
else:
    for v in lanes.values():
        g = (v/total)*TOTAL_TIME if total else MIN_GREEN
        green_times.append(max(g, MIN_GREEN))

# METRICS
c1,c2,c3 = st.columns(3)

density = min(total/200,1)

c1.metric("🚗 Total Vehicles", total)
c2.metric("📊 Traffic Density", f"{density*100:.1f}%")
c3.metric("⚖ Fairness", round(1 - (max(green_times)-min(green_times))/max(green_times),2))

# CHARTS
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.bar(lanes.keys(), lanes.values())
    ax.set_title("Traffic Distribution")
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.bar(lanes.keys(), green_times)
    ax2.set_title("AI Signal Allocation")
    st.pyplot(fig2)

# STATUS
if emergency:
    st.error(f"🚨 Emergency at {lane} lane")

st.success("AI dynamically optimizes traffic signals based on vehicle density.")