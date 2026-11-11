
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "OnlineRetail_Cleaned.csv"
OUTPUT_DIR = BASE_DIR / "reports" / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    print("Loading cleaned dataset...")

    df = pd.read_csv(DATA_PATH)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df


# 1. Missing Values Analysis
def plot_missing_values(df):
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values()

    percentages = (missing / len(df)) * 100

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(missing.index, missing.values)

    for bar, count, percentage in zip(
        bars, missing.values, percentages.values
    ):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {count:,} ({percentage:.2f}%)",
            va="center"
        )

    ax.set_title("Missing Values by Column", fontsize=15, fontweight="bold")
    ax.set_xlabel("Number of Missing Records")
    ax.set_ylabel("Column")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "missing_values.png", dpi=300)
    plt.close()


# 2. Data Cleaning Summary
def plot_cleaning_summary():
    original_rows = 541909
    duplicates_removed = 5268
    final_rows = 536641

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Overall dataset comparison
    categories = ["Original Records", "Final Records"]
    values = [original_rows, final_rows]

    bars = axes[0].bar(categories, values)

    axes[0].set_title("Dataset Before and After Cleaning")
    axes[0].set_ylabel("Number of Records")
    axes[0].ticklabel_format(axis="y", style="plain")

    for bar, value in zip(bars, values):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,}",
            ha="center",
            va="bottom"
        )

    # Duplicate removal shown separately
    axes[1].bar(
        ["Duplicates Removed"],
        [duplicates_removed]
    )

    axes[1].set_title("Duplicate Records Removed")
    axes[1].set_ylabel("Number of Records")

    axes[1].text(
        0,
        duplicates_removed,
        f"{duplicates_removed:,}\n({duplicates_removed / original_rows * 100:.2f}%)",
        ha="center",
        va="bottom"
    )

    fig.suptitle("Data Cleaning Summary", fontsize=16, fontweight="bold")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "cleaning_summary.png", dpi=300)
    plt.close()


# 3. Country-wise Transaction Analysis
def plot_country_transactions(df):
    country_counts = (
        df["Country"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    bars = ax.barh(country_counts.index, country_counts.values)

    for bar, value in zip(bars, country_counts.values):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {value:,}",
            va="center"
        )

    ax.set_title(
        "Top 10 Countries by Transaction Records",
        fontsize=15,
        fontweight="bold"
    )
    ax.set_xlabel("Number of Records")
    ax.set_ylabel("Country")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "country_transactions.png", dpi=300)
    plt.close()


# 4. Monthly Revenue Trend
def plot_monthly_revenue(df):
    sales_df = df[
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0)
    ].copy()

    sales_df["Revenue"] = (
        sales_df["Quantity"] * sales_df["UnitPrice"]
    )

    monthly_revenue = (
        sales_df.set_index("InvoiceDate")["Revenue"]
        .resample("ME")
        .sum()
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        monthly_revenue.index,
        monthly_revenue.values,
        marker="o",
        linewidth=2
    )

    ax.set_title(
        "Monthly Revenue Trend",
        fontsize=15,
        fontweight="bold"
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (£)")

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"£{value:,.0f}")
    )

    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=300)
    plt.close()


# Main function
def generate_visualizations():
    df = load_data()

    print("Generating professional visualizations...")

    plot_missing_values(df)
    plot_cleaning_summary()
    plot_country_transactions(df)
    plot_monthly_revenue(df)

    print("\nAll visualizations generated successfully!")
    print(f"Output folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_visualizations()
