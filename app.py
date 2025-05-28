import streamlit as st
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page config for a clean, minimalist look
st.set_page_config(page_title="Smart Wristwatch", layout="centered")

# Function to predict stress based on user inputs
def predict_stress(heart_rate, systolic_bp, diastolic_bp, blood_sugar):
    stress_conditions = [
        heart_rate > 100,  # From your report
        systolic_bp > 140 or diastolic_bp > 90,  # General hypertension threshold
        blood_sugar > 180 or blood_sugar < 70  # Extreme blood sugar levels
    ]
    return "Stressed" if any(stress_conditions) else "Calm"

# Function to create a simple breathing animation (text-based)
def breathing_guide():
    st.subheader("Breathing Exercise")
    placeholder = st.empty()
    for _ in range(3):  # Simulate 3 breathing cycles
        placeholder.markdown("<h3 style='text-align: center; color: #4CAF50;'>Inhale...</h3>", unsafe_allow_html=True)
        time.sleep(4)
        placeholder.markdown("<h3 style='text-align: center; color: #4CAF50;'>Exhale...</h3>", unsafe_allow_html=True)
        time.sleep(4)
    placeholder.markdown("<h3 style='text-align: center; color: #4CAF50;'>Breathing Complete!</h3>", unsafe_allow_html=True)
    if st.button("Back to Home", key="back"):
        st.session_state.page = "home"

# Function to plot heart rate trend
def plot_heart_rate(heart_rates):
    fig, ax = plt.subplots()
    ax.plot(heart_rates, marker='o', color='b')
    ax.set_title("Heart Rate Trend (Last 5 Readings)")
    ax.set_xlabel("Reading")
    ax.set_ylabel("Heart Rate (bpm)")
    ax.grid(True)
    st.pyplot(fig)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'heart_rates' not in st.session_state:
    st.session_state.heart_rates = [80] * 5  # Initialize with default heart rate

# Main app logic
st.markdown("<h1 style='text-align: center; color: #333;'>Smart Wristwatch</h1>", unsafe_allow_html=True)

if st.session_state.page == "home":
    # Home Screen
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"<h2 style='text-align: center; color: #555;'>Time: {current_time}</h2>", unsafe_allow_html=True)

    # Input form for health metrics
    st.subheader("Enter Your Health Metrics")
    with st.form(key="health_form"):
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=80)
        systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=200, value=120)
        diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=120, value=80)
        blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=20, max_value=400, value=100)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Update heart rate history
        st.session_state.heart_rates.append(heart_rate)
        st.session_state.heart_rates = st.session_state.heart_rates[-5:]  # Keep last 5 readings
        
        # Display health metrics
        st.markdown(f"<h2 style='text-align: center; color: #555;'>Heart Rate: {heart_rate} bpm</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: #555;'>Blood Pressure: {systolic_bp}/{diastolic_bp} mmHg</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: #555;'>Blood Sugar: {blood_sugar} mg/dL</h2>", unsafe_allow_html=True)

        # Predict stress
        status = predict_stress(heart_rate, systolic_bp, diastolic_bp, blood_sugar)
        
        # Display status with visual alert
        if status == "Stressed":
            st.markdown(
                "<h2 style='text-align: center; color: red; animation: blinker 1s linear infinite;'>Status: Stressed</h2>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<style>@keyframes blinker {50% {opacity: 0.5;}}</style>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"<h2 style='text-align: center; color: green;'>Status: Calm</h2>", unsafe_allow_html=True)

        # Plot heart rate trend
        plot_heart_rate(st.session_state.heart_rates)

    # Button to simulate gesture for breathing exercise
    if st.button("Start Breathing Exercise", key="breathing"):
        st.session_state.page = "breathing"

    # Settings button
    if st.button("Settings", key="settings"):
        st.session_state.page = "settings"

elif st.session_state.page == "breathing":
    breathing_guide()

elif st.session_state.page == "settings":
    st.subheader("Settings")
    st.write("Adjust preferences for alerts and gestures.")
    alert_toggle = st.checkbox("Enable Vibration Alerts", value=True)
    gesture_sensitivity = st.slider("Gesture Sensitivity", 1, 10, 5)
    if alert_toggle:
        st.write("Vibration Alerts: Enabled")
    else:
        st.write("Vibration Alerts: Disabled")
    st.write(f"Gesture Sensitivity: {gesture_sensitivity}")
    if st.button("Back to Home", key="back_settings"):
        st.session_state.page = "home"

# Footer
st.markdown("<hr><p style='text-align: center; color: #777;'>Designed for ADHD/Autism Support</p>", unsafe_allow_html=True)