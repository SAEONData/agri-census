# app.py

import streamlit as st
from views import home, summary

# Sidebar routing
#st.set_page_config(page_title="CoCA 2017 Dashboard", layout="wide")

PAGES = {
    "🏠 Home": home.show,
    "📊 Summary": summary.show,
    # More to come:
    # "🗺️ Map Explorer": map.show,
    # "📋 Data Explorer": table.show,
    # "📈 Time Comparison": time.show,
    # "📚 Methodology & About": about.show,
}

st.sidebar.title("📌 Menu")
selection = st.sidebar.radio("Go to:", list(PAGES.keys()))
PAGES[selection]()
