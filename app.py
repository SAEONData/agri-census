import streamlit as st
from utils.layout import PAGE_HELP_TEXT
from views import home, summary, map, explorer

st.set_page_config(page_title="2017 Coca Census", layout="wide")

PAGES = {
    "🏠 Home": home.show,
    "📊 Summary": summary.show,
    "🗺️ Map Explorer": map.show,
    "📋 Data Explorer": explorer.show
}

st.sidebar.title("Menu")
selection = st.sidebar.radio("Go to:", list(PAGES.keys()))
PAGES[selection]()
st.sidebar.markdown(PAGE_HELP_TEXT["home_links"])