import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Piezo Smart Energy System", layout="wide")

st.title("⚡ Piezoelectric Smart Road Energy Generation System")

# ================= SIDEBAR =================
st.sidebar.header("🚗 Traffic Input")

vehicles = st.sidebar.slider("Vehicles per Minute", 0, 200, 80)
weight = st.sidebar.slider("Average Vehicle Weight (kg)", 500, 3000, 1500)
runtime = st.sidebar.slider("Runtime (minutes)", 1, 120, 30)
coverage = st.sidebar.slider("Piezo Road Coverage (%)", 10, 100, 50)

# ================= CALCULATIONS =================

# Piezo system
energy_per_min = vehicles * weight * 0.00005 * (coverage/100)
total_energy = energy_per_min * runtime
co2_saved = total_energy * 0.02
revenue = total_energy * 0.0002

# Traditional system
fuel_saved_old = vehicles * 0.00015 * runtime
co2_old = fuel_saved_old * 2.3
energy_old = 0

# ================= METRICS =================
c1, c2, c3, c4 = st.columns(4)

c1.metric("⚡ Energy / min", f"{energy_per_min:.2f} Wh")
c2.metric("🔋 Total Energy", f"{total_energy:.2f} Wh")
c3.metric("🌱 CO₂ Offset", f"{co2_saved:.2f} kg")
c4.metric("💰 Revenue", f"${revenue:.2f}")

# ================= ENERGY SUMMARY =================
st.subheader("⚡ Energy Generation Summary")

c1, c2, c3 = st.columns(3)

c1.metric("Energy per Minute", f"{energy_per_min:.2f} Wh")
c2.metric("Total Energy Generated", f"{total_energy:.2f} Wh")
c3.metric("Energy Efficiency", f"{(coverage):.0f}%")

st.success("📊 Clean energy generated from vehicle pressure in real-time.")

# ================= COMPARISON =================
st.subheader("⚖ Traditional vs Smart Piezo System")

labels = ["Traditional", "Piezo Smart"]

energy_vals = [energy_old, total_energy]
co2_vals = [co2_old, co2_saved]

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.bar(labels, energy_vals)
    ax1.set_title("⚡ Energy Comparison")
    ax1.set_ylabel("Energy (Wh)")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.bar(labels, co2_vals)
    ax2.set_title("🌱 CO₂ Comparison")
    ax2.set_ylabel("CO₂ (kg)")
    st.pyplot(fig2)

# ================= BATTERY =================
st.subheader("🔋 Energy Storage")

battery = min(int((total_energy/100)*100), 100)
st.progress(battery)
st.write(f"Battery Level: {battery}%")

# ================= SUMMARY =================
st.success("🚀 Piezoelectric roads convert vehicle pressure into clean, renewable energy.")

st.info("📊 Compared to traditional systems, this approach generates energy while reducing carbon emissions.")