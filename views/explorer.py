import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from utils.filters import render_sidebar_filters
from utils.layout import PAGE_HELP_TEXT
from utils.database import load_coca_view


def show():
    st.title("📋 Data Explorer")
    st.markdown(PAGE_HELP_TEXT.get("table", "Browse detailed agricultural census data below."))

    ss = st.session_state
    province = ss.get("filter.province", [])
    district = ss.get("filter.district", [])
    indicator = ss.get("filter.indicator")
    sub_indicator = ss.get("filter.sub_indicator")

    df = load_coca_view(
        province=province,
        district=district,
        indicator=indicator,
        sub_indicator=sub_indicator
    )

    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    default_columns = [
        "province", "district_municipality", "census_region",
        "indicator", "sub_indicator", "unit",
        "farming_units", "y2007", "y2017"
    ]
    hidden_columns = list(set(df.columns) - set(default_columns))

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False, resizable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    for col in hidden_columns:
        gb.configure_column(col, hide=True)

    grid_options = gb.build()

    st.markdown("### 🔍 Filtered Results")
    AgGrid(
        df,
        gridOptions=grid_options,
        height=600,
        width='100%',
        update_mode=GridUpdateMode.NO_UPDATE,
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True
    )

    with st.expander("📥 Download filtered data"):
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="coca_filtered_data.csv",
            mime="text/csv"
        )
