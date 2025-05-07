# app.py
import streamlit as st
from views import home

home.show()


# app.py
#import streamlit as st
#from views import home, summary, map, table, indicator, time

#pages = {
#    "Home": home.show,
#    "Summary Dashboard": summary.show,
#    "Indicator Explorer": indicator.show,
#    "Map Explorer": map.show,
#    "Data Explorer": table.show,
#    "Time Comparison": time.show
#}

#st.sidebar.title("📌 CoCA 2017 Navigation")
#page = st.sidebar.radio("Go to", list(pages.keys()))
#pages[page]()
