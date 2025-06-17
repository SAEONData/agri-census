import streamlit as st
import plotly.graph_objects as go
import json
import re
from rapidfuzz import process
from utils.filters import render_sidebar_filters
from utils.layout import PAGE_HELP_TEXT
from utils.database import (
    farming_units_by_prov,
    farming_units_by_district
)

province_iso_map = {
    "Eastern Cape": "ZA-EC",
    "Free State": "ZA-FS",
    "Gauteng": "ZA-GP",
    "Kwazulu-Natal": "ZA-KZN",
    "Limpopo": "ZA-LP",
    "Mpumalanga": "ZA-MP",
    "North West": "ZA-NW",
    "Northern Cape": "ZA-NC",
    "Western Cape": "ZA-WC"
}

def show():
    st.title("🖼️ Map Explorer")
    st.markdown(PAGE_HELP_TEXT.get("map", "Explore spatial patterns in the Agricultural Census."))

    level = st.radio("Select level", options=["Province", "District"], horizontal=True)

    province_options = list(province_iso_map.keys())
    selected_province = st.selectbox("Filter by Province", options=["All"] + province_options)

    ss = st.session_state
    district = ss.get("filter.district", [])
    indicator = ss.get("filter.indicator")
    sub_indicator = ss.get("filter.sub_indicator")

    province = [selected_province] if selected_province != "All" else []

    if level == "Province":
        df = farming_units_by_prov(
            province=province,
            district=district,
            indicator=indicator,
            sub_indicator=sub_indicator
        )

        if df.empty:
            st.warning("No data available for selected filters.")
            return

        df["iso"] = df["province"].map(province_iso_map)
        geojson_file = "data/gadm41_ZAF_1.geojson"
        featureidkey = "properties.ISO_1"
        locations = df["iso"]

        with open(geojson_file) as f:
            sa_geojson = json.load(f)

    else:
        df = farming_units_by_district(
            province=province,
            district=district,
            indicator=indicator,
            sub_indicator=sub_indicator
        )

        if df.empty:
            st.warning("No data available for selected filters.")
            return

        geojson_file = "data/gadm41_ZAF_2.geojson"
        featureidkey = "properties.NAME_2"

        with open(geojson_file) as f:
            sa_geojson = json.load(f)

        gadm_names = [f["properties"]["NAME_2"] for f in sa_geojson["features"]]
         
        def clean_and_match(name):
            cleaned = re.sub(r"\s+(District|Metropolitan) Municipality\s*(\([^)]+\))?", "", name, flags=re.IGNORECASE)
            cleaned = cleaned.replace(" ", "")
            match, score, _ = process.extractOne(cleaned, gadm_names)
            return match if score >= 80 else None

        df["gadm_district"] = df["district_municipality"].apply(clean_and_match)
        df = df.dropna(subset=["farming_units", "gadm_district"])
        locations = df["gadm_district"]

    fig = go.Figure(
        go.Choropleth(
            geojson=sa_geojson,
            featureidkey=featureidkey,
            locations=locations,
            z=df["farming_units"],
            text=df["district_municipality"] if level == "District" else df["province"],
            colorscale="Viridis",
            marker_line_color="white",
            colorbar_title="Farming Units"
        )
    )

    fig.update_geos(
        visible=False,
        fitbounds="locations",
        showcountries=False,
        showcoastlines=False,
        showland=True,
        landcolor="lightgray"
    )

    fig.update_layout(
        title=f"Farming Units by {level}",
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
