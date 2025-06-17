import streamlit as st
st.set_page_config(page_title="2017 Coca Census", page_icon="images/saeon.svg" , layout="wide")

from utils.layout import PAGE_HELP_TEXT
from views import home, summary, map, explorer

PAGES = {
    "🏠 Home": home.show,
    "📊 Summary": summary.show,
    "🗺️ Map Explorer": map.show,
    "📋 Data Explorer": explorer.show
}

col1, col2 = st.columns([1, 1])
with col1:
    st.sidebar.image("images/saeon_logo.png", width=180)

with col2:
    st.sidebar.image("images/statssa_logo.png", width=180)

st.sidebar.title("Menu")
selection = st.sidebar.radio("Go to:", list(PAGES.keys()))
PAGES[selection]()
st.sidebar.markdown(PAGE_HELP_TEXT["home_links"])