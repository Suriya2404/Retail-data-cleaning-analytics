
import pandas as pd


def remove_duplicates(df):
    """Remove exact duplicate records."""

    before = len(df)

    df = df.drop_duplicates().copy()

    removed = before - len(df)

    print(f"Exact duplicate records removed: {removed}")

    return df, removed


def clean_text_columns(df):
    """Standardize text columns without changing business meaning."""

    text_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Country"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # Treat empty descriptions as missing
    df["Description"] = df["Description"].replace("", pd.NA)

    print("Text columns standardized.")

    return df


def convert_data_types(df):
    """Convert columns to appropriate data types."""

    # Invoice and stock codes remain strings
    df["InvoiceNo"] = df["InvoiceNo"].astype("string")
    df["StockCode"] = df["StockCode"].astype("string")

    # Convert invoice dates
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    # Convert CustomerID to nullable integer
    df["CustomerID"] = pd.to_numeric(
        df["CustomerID"],
        errors="coerce"
    ).astype("Int64")

    # Ensure numeric columns are numeric
    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    ).astype("Int64")

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    print("Data types converted successfully.")

    return df


def validate_data(df):
    """Identify potential data-quality issues."""

    validation_report = {
        "missing_descriptions": int(
            df["Description"].isna().sum()
        ),

        "missing_customer_ids": int(
            df["CustomerID"].isna().sum()
        ),

        "invalid_dates": int(
            df["InvoiceDate"].isna().sum()
        ),

        "negative_quantities": int(
            (df["Quantity"] < 0).sum()
        ),

        "zero_prices": int(
            (df["UnitPrice"] == 0).sum()
        ),

        "negative_prices": int(
            (df["UnitPrice"] < 0).sum()
        ),

        "cancelled_invoices": int(
            df["InvoiceNo"].str.startswith(
                "C", na=False
            ).sum()
        ),

        "remaining_duplicates": int(
            df.duplicated().sum()
        )
    }

    print("\n========== VALIDATION REPORT ==========")

    for issue, count in validation_report.items():
        print(f"{issue}: {count}")

    return validation_report


def clean_dataset(df):
    """Execute the complete cleaning workflow."""

    print("\n========== STARTING DATA CLEANING ==========")

    original_rows = len(df)

    # Work on a copy
    df = df.copy()

    # Step 1: Remove exact duplicates
    df, duplicates_removed = remove_duplicates(df)

    # Step 2: Standardize text
    df = clean_text_columns(df)

    # Step 3: Convert data types
    df = convert_data_types(df)

    # Step 4: Validate data
    validation_report = validate_data(df)

    cleaning_summary = {
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicates_removed": duplicates_removed,
        "rows_preserved": len(df)
    }

    print("\n========== CLEANING SUMMARY ==========")
    print(cleaning_summary)

    return df, cleaning_summary, validation_report
