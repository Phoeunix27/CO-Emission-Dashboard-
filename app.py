import streamlit as st
import pandas as pd
import plotly.express as px

# App Theme
st.set_page_config(
    page_title="CO₂ Emission Dashboard",
    layout="wide"
)

BANNER_URL = "https://static.vecteezy.com/system/resources/previews/029/098/585/non_2x/net-zero-and-carbon-neutral-banner-concept-of-reducing-carbon-dioxide-emissions-responsible-development-vector.jpg"

# Helper — load dataset
@st.cache_data
def load_data(file):
    return pd.read_csv(file)


# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page:", ["Home", "Dataset Explorer", "CO₂ Sector Dashboard"])

st.sidebar.markdown("---")


# Home Page
if page == "Home":
    st.image(BANNER_URL, use_container_width=True)
    st.title("Global CO₂ Emission Visualization")
    st.markdown("""
    
    This app lets you explore **Global CO₂ emissions** using an interactive dashboard.

    ### Features:
    - Multi-page navigation  
    - Upload your dataset or use sample  
    - Multiple interactive charts  
    - Sector-based emission analytics  
    - Clean modern UI  
    """)

    st.markdown("---")

    st.subheader("How to Start")
    st.write("Go to **Dataset Explorer** to load your CO₂ dataset.")


# DATASET EXPLORER
elif page == "Dataset Explorer":
    st.image(BANNER_URL, use_container_width=True)
    st.title("Dataset Explorer")

    uploaded = st.file_uploader("Upload your CO₂ dataset (CSV)", type=["csv"])

    if uploaded:
        df = load_data(uploaded)
        st.success("Dataset loaded successfully!")
    else:
        st.info("Please upload the Kaggle CO₂ dataset to continue.")
        st.stop()

    #date format
    import pandas as pd

    # Strip column names just in case
    df.columns = df.columns.str.strip()

    # Convert date column, handle day-first, coerce errors
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')

    # Check
    print(df["date"].head())
    print("Failed to parse:", df["date"].isna().sum())


    st.subheader("Preview Dataset")
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary Statistics")
    st.write(df.describe())

    st.markdown("---")

    st.subheader("Top 10 Emitting Countries (Total Value)")
    top10 = df.groupby("country")["value"].sum().sort_values(ascending=False).head(10)

    fig = px.bar(
        top10,
        x=top10.index,
        y=top10.values,
        title="Top 10 CO₂ Emitting Countries",
        labels={"x": "Country", "y": "Total CO₂ Emission"}
    )
    st.plotly_chart(fig, use_container_width=True)


# CO₂ SECTOR DASHBOARD
elif page == "CO₂ Sector Dashboard":
    st.image(BANNER_URL, use_container_width=True)
    st.title("CO₂ Emission Sector Dashboard")

    uploaded = st.sidebar.file_uploader("Upload CSV Dataset", type=["csv"])

    if uploaded:
        df = load_data(uploaded)
    else:
        st.warning("Upload your dataset in the sidebar to begin.")
        st.stop()

    # Clean date
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')

    # Sidebar filtering
    st.sidebar.subheader("Filter Options")
    countries = sorted(df["country"].unique())
    sectors = sorted(df["sector"].unique())

    selected_country = st.sidebar.selectbox("Select Country", ["All"] + countries)
    selected_sector = st.sidebar.selectbox("Select Sector", ["All"] + sectors)

    filtered = df.copy()

    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]

    if selected_sector != "All":
        filtered = filtered[filtered["sector"] == selected_sector]

    st.markdown(f"### Showing data for: **{selected_country} | {selected_sector}**")

    # 1) Line Chart — Trend Over Time
    st.subheader("Emission Trend Over Time")
    fig_line = px.line(
        filtered,
        x="date",
        y="value",
        color="sector",
        title="CO₂ Emission Trend"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # 2) Bar Chart — By Sector
    st.subheader("Total Emissions by Sector")
    sector_sum = filtered.groupby("sector")["value"].sum().reset_index()
    fig_bar = px.bar(
        sector_sum,
        x="sector",
        y="value",
        color="sector",
        title="Total CO₂ Emission per Sector"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 3) Box Plot — Distribution
    st.subheader("Distribution of Emissions")
    fig_box = px.box(
        filtered,
        x="sector",
        y="value",
        color="sector",
        title="Distribution of CO₂ Emission Values"
    )
    st.plotly_chart(fig_box, use_container_width=True)

    
    # 4) Sunburst Chart for Country & Sector Hierarchy
    st.subheader("Sector Breakdown by Country")
    fig_sun = px.sunburst(
        filtered,
        path=["country", "sector"],
        values="value",
        title="CO₂ Emission Breakdown"
    )
    st.plotly_chart(fig_sun, use_container_width=True)

    # 5) Animated Chart — Time Animation
    st.subheader("🎞 Animated CO₂ Change Over Time")
    fig_anim = px.bar(
        filtered,
        x="sector",
        y="value",
        color="sector",
        animation_frame=filtered["date"].dt.strftime("%Y-%m-%d"),
        title="CO₂ Emission Over Time (Animated)"
    )
    st.plotly_chart(fig_anim, use_container_width=True)
