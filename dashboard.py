
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import FuncFormatter


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Retail Analytics | Data Quality",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR / "data" / "processed" / "OnlineRetail_Cleaned.csv"
)

ORIGINAL_RECORDS = 541909
DUPLICATES_REMOVED = 5268


# ==========================================================
# PROFESSIONAL DARK THEME
# ==========================================================

BG = "#0B1120"
PANEL = "#151F32"
ACCENT = "#38BDF8"
GREEN = "#34D399"
ORANGE = "#FBBF24"
RED = "#FB7185"
TEXT = "#E2E8F0"
MUTED = "#94A3B8"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
    "axes.edgecolor": "#334155",
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "grid.color": "#334155",
    "grid.alpha": 0.4,
    "axes.titleweight": "bold",
    "font.size": 10
})

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: #E2E8F0;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    background-color: #111A2B;
    border-right: 1px solid #25334A;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #19263B, #121C2E);
    border: 1px solid #293B55;
    padding: 20px;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC;
    font-weight: 700;
}

h1, h2, h3 {
    color: #F8FAFC;
}

p, label {
    color: #CBD5E1;
}

hr {
    border-color: #293B55;
}

div[data-testid="stDownloadButton"] button {
    background-color: #0284C7;
    color: white;
    border: none;
    border-radius: 8px;
}

div[data-testid="stDownloadButton"] button:hover {
    background-color: #0369A1;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Cleaned dataset not found. Please run main.py first."
    )
    st.stop()


# ==========================================================
# COMMON METRICS
# ==========================================================

total_records = len(df)
missing_total = int(df.isnull().sum().sum())

missing_customer_ids = int(df["CustomerID"].isna().sum())
missing_descriptions = int(df["Description"].isna().sum())

unique_countries = int(df["Country"].nunique())

remaining_duplicates = int(df.duplicated().sum())

cancelled_invoices = int(
    df["InvoiceNo"].str.startswith("C", na=False).sum()
)

negative_quantities = int((df["Quantity"] < 0).sum())
zero_prices = int((df["UnitPrice"] == 0).sum())
negative_prices = int((df["UnitPrice"] < 0).sum())

sales_df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0)
].copy()

sales_df["Revenue"] = (
    sales_df["Quantity"] * sales_df["UnitPrice"]
)

total_revenue = sales_df["Revenue"].sum()


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def show_html_table(dataframe):
    html = dataframe.to_html(
        index=False,
        border=0,
        classes="professional-table"
    )

    st.markdown("""
    <style>
    .professional-table {
        width: 100%;
        border-collapse: collapse;
        color: #E2E8F0;
        font-size: 14px;
    }

    .professional-table th {
        background-color: #1E293B;
        color: #38BDF8;
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #334155;
    }

    .professional-table td {
        padding: 11px;
        border-bottom: 1px solid #263449;
    }

    .professional-table tr:hover {
        background-color: #19263B;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(html, unsafe_allow_html=True)


def chart_style(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, fontsize=14, fontweight="bold", pad=16)

    if xlabel:
        ax.set_xlabel(xlabel)

    if ylabel:
        ax.set_ylabel(ylabel)

    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

st.sidebar.markdown("## 📊 RETAIL ANALYTICS")

st.sidebar.caption("DATA INTELLIGENCE PLATFORM")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Data Quality",
        "Sales Analytics",
        "Dataset Explorer"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### DATASET INFORMATION")
st.sidebar.write("**Dataset:** Online Retail")
st.sidebar.write(f"**Records:** {total_records:,}")
st.sidebar.write(f"**Columns:** {df.shape[1]}")
st.sidebar.write(f"**Countries:** {unique_countries}")

st.sidebar.divider()

st.sidebar.caption(
    "Built with Python · Pandas · Matplotlib · Streamlit"
)


# ==========================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==========================================================

if page == "Executive Overview":

    st.title("📊 Retail Analytics Dashboard")

    st.markdown(
        "Executive overview of retail transactions, "
        "data cleaning performance and data quality."
    )

    st.divider()

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Records",
        f"{total_records:,}"
    )

    c2.metric(
        "Duplicates Removed",
        f"{DUPLICATES_REMOVED:,}"
    )

    c3.metric(
        "Missing Values",
        f"{missing_total:,}"
    )

    c4.metric(
        "Countries",
        f"{unique_countries}"
    )

    st.write("")
    st.divider()

    # Cleaning summary
    st.subheader("Data Cleaning Performance")

    col1, col2 = st.columns([1.5, 1])

    with col1:

        fig, ax = plt.subplots(figsize=(9, 4))

        labels = ["Original", "Final"]
        values = [ORIGINAL_RECORDS, total_records]

        bars = ax.bar(
            labels,
            values,
            color=[ACCENT, GREEN],
            width=0.5
        )

        ax.set_ylim(0, ORIGINAL_RECORDS * 1.12)

        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 5000,
                f"{value:,}",
                ha="center",
                color=TEXT,
                fontweight="bold"
            )

        chart_style(
            ax,
            "Records Before vs After Cleaning",
            ylabel="Number of Records"
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:

        st.markdown("### Cleaning Results")

        st.metric(
            "Duplicate Removal Rate",
            f"{DUPLICATES_REMOVED / ORIGINAL_RECORDS * 100:.2f}%"
        )

        st.metric(
            "Records Preserved",
            f"{total_records / ORIGINAL_RECORDS * 100:.2f}%"
        )

        st.metric(
            "Remaining Duplicates",
            f"{remaining_duplicates:,}"
        )

    st.divider()

    # Dataset overview
    st.subheader("Dataset Overview")

    a, b = st.columns(2)

    with a:
        st.markdown("### Data Quality")
        st.write(f"Missing Customer IDs: **{missing_customer_ids:,}**")
        st.write(f"Missing Descriptions: **{missing_descriptions:,}**")
        st.write(f"Remaining Duplicates: **{remaining_duplicates:,}**")

    with b:
        st.markdown("### Transaction Information")
        st.write(f"Cancelled Invoices: **{cancelled_invoices:,}**")
        st.write(f"Negative Quantities: **{negative_quantities:,}**")
        st.write(f"Unique Countries: **{unique_countries}**")


# ==========================================================
# PAGE 2: DATA QUALITY
# ==========================================================

elif page == "Data Quality":

    st.title("🔍 Data Quality Analysis")

    st.markdown(
        "Understand missing values, validation results "
        "and the quality of the cleaned dataset."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Missing Values", f"{missing_total:,}")
    c2.metric("Missing Customer IDs", f"{missing_customer_ids:,}")
    c3.metric("Remaining Duplicates", f"{remaining_duplicates:,}")

    st.divider()

    st.subheader("Missing Values Distribution")

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values()

    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Records": missing.values,
        "Missing Percentage": (
            missing.values / total_records * 100
        )
    })

    col1, col2 = st.columns([1.4, 1])

    with col1:

        fig, ax = plt.subplots(figsize=(8, 4))

        bars = ax.barh(
            missing.index,
            missing.values,
            color=[ORANGE, RED]
        )

        for bar, value in zip(bars, missing.values):
            percentage = value / total_records * 100

            ax.text(
                bar.get_width(),
                bar.get_y() + bar.get_height() / 2,
                f"  {value:,} ({percentage:.2f}%)",
                va="center",
                color=TEXT
            )

        chart_style(
            ax,
            "Missing Values by Column",
            xlabel="Missing Records"
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.markdown("### Missing Value Report")

        display_missing = missing_df.copy()
        display_missing["Missing Percentage"] = (
            display_missing["Missing Percentage"].map(
                lambda x: f"{x:.2f}%"
            )
        )

        show_html_table(display_missing)

    st.divider()

    st.subheader("Data Validation Report")

    validation_df = pd.DataFrame({
        "Validation Check": [
            "Invalid Dates",
            "Negative Quantities",
            "Zero Prices",
            "Negative Prices",
            "Cancelled Invoices",
            "Remaining Duplicates"
        ],
        "Records": [
            int(df["InvoiceDate"].isna().sum()),
            negative_quantities,
            zero_prices,
            negative_prices,
            cancelled_invoices,
            remaining_duplicates
        ]
    })

    show_html_table(validation_df)

    st.caption(
        "Negative quantities, cancelled invoices and unusual price "
        "records are reported rather than automatically deleted."
    )


# ==========================================================
# PAGE 3: SALES ANALYTICS
# ==========================================================

elif page == "Sales Analytics":

    st.title("💰 Retail Sales Analytics")

    st.markdown(
        "Explore revenue trends and transaction patterns "
        "across different countries."
    )

    st.divider()

    # Date filters
    min_date = sales_df["InvoiceDate"].min().date()
    max_date = sales_df["InvoiceDate"].max().date()

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        st.stop()

    filtered_sales = sales_df[
        (sales_df["InvoiceDate"].dt.date >= start_date) &
        (sales_df["InvoiceDate"].dt.date <= end_date)
    ]

    filtered_revenue = filtered_sales["Revenue"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Gross Line-item Revenue",
        f"£{filtered_revenue:,.2f}"
    )

    c2.metric(
        "Sales Records",
        f"{len(filtered_sales):,}"
    )

    c3.metric(
        "Countries",
        f"{filtered_sales['Country'].nunique()}"
    )

    st.caption(
        "Revenue uses positive quantities and positive unit prices. "
        "It is gross line-item revenue, not net revenue after returns."
    )

    st.divider()

    # Monthly revenue
    st.subheader("Monthly Revenue Trend")

    monthly_revenue = (
        filtered_sales
        .set_index("InvoiceDate")["Revenue"]
        .resample("ME")
        .sum()
    )

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        monthly_revenue.index,
        monthly_revenue.values,
        color=ACCENT,
        marker="o",
        linewidth=2.5,
        markersize=6
    )

    ax.fill_between(
        monthly_revenue.index,
        monthly_revenue.values,
        color=ACCENT,
        alpha=0.12
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, _: f"£{x / 1_000_000:.1f}M")
    )

    chart_style(
        ax,
        "Monthly Revenue",
        xlabel="Month",
        ylabel="Revenue"
    )

    plt.xticks(rotation=30)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.divider()

    # Country transactions
    st.subheader("Country-wise Transaction Analysis")

    country_data = (
        filtered_sales["Country"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(11, 5))

    bars = ax.barh(
        country_data.index,
        country_data.values,
        color=GREEN
    )

    for bar, value in zip(bars, country_data.values):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"  {value:,}",
            va="center",
            color=TEXT
        )

    chart_style(
        ax,
        "Top 10 Countries by Sales Records",
        xlabel="Number of Records"
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.divider()

    # Country selector
    st.subheader("Individual Country Analysis")

    countries = sorted(
        filtered_sales["Country"].dropna().unique()
    )

    selected_country = st.selectbox(
        "Select a Country",
        countries
    )

    selected_data = filtered_sales[
        filtered_sales["Country"] == selected_country
    ]

    st.metric(
        f"{selected_country} Revenue",
        f"£{selected_data['Revenue'].sum():,.2f}"
    )


# ==========================================================
# PAGE 4: DATASET EXPLORER
# ==========================================================

elif page == "Dataset Explorer":

    st.title("📁 Dataset Explorer")

    st.markdown(
        "Search, filter and download records from the cleaned dataset."
    )

    st.divider()

    countries = sorted(df["Country"].dropna().unique())

    selected_countries = st.multiselect(
        "Filter by Country",
        countries,
        placeholder="Select one or more countries"
    )

    search_text = st.text_input(
        "Search Product Description",
        placeholder="Enter a product name..."
    )

    filtered_df = df

    if selected_countries:
        filtered_df = filtered_df[
            filtered_df["Country"].isin(selected_countries)
        ]

    if search_text:
        filtered_df = filtered_df[
            filtered_df["Description"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.divider()

    st.metric(
        "Matching Records",
        f"{len(filtered_df):,}"
    )

    st.markdown("### Filtered Dataset Preview")

    st.caption(
        "Showing the first 100 matching records. "
        "The download contains all matching records."
    )

    preview = filtered_df.head(100)

    show_html_table(preview)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Filtered Dataset",
        data=csv_data,
        file_name="filtered_retail_data.csv",
        mime="text/csv"
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    "<div style='text-align:center; color:#64748B;'>"
    "RETAIL ANALYTICS PLATFORM | "
    "Built with Python, Pandas, Matplotlib and Streamlit"
    "</div>",
    unsafe_allow_html=True
)
