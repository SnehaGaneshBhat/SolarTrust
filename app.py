import streamlit as st
from ui.official_dashboard import show_official_dashboard
from ui.resident_dashboard import show_resident_dashboard

st.set_page_config(page_title="Solar Panel Verifier", layout="wide")

st.markdown(
    "<h1 style='text-align: center; font-size: 3rem;'>Rooftop Solar Panel Verification Portal</h1>",
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

role = st.selectbox("Select your role", ["Choose...", "Official", "Resident"])

if role == "Official":
    show_official_dashboard()

elif role == "Resident":
    show_resident_dashboard()

