
import pandas as pd
from pathlib import Path

# Load original dataset
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "data" / "raw" / "OnlineRetail.csv"

df = pd.read_csv(FILE_PATH, encoding="ISO-8859-1")

print("\n========== DEEP DATA QUALITY AUDIT ==========")

# 1. Missing values
print("\n1. MISSING VALUE ANALYSIS")
missing = df.isnull().sum()
missing_percent = (missing / len(df)) * 100

missing_report = pd.DataFrame({
    "Missing Count": missing,
    "Missing Percentage": missing_percent.round(2)
})

print(missing_report)

# 2. Duplicate records
print("\n2. DUPLICATE RECORD ANALYSIS")
print("Exact duplicate rows:", df.duplicated().sum())
print("Duplicate Invoice Numbers:", df["InvoiceNo"].duplicated().sum())

# 3. Cancelled invoices
print("\n3. CANCELLED INVOICES")
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print("Cancelled invoice rows:", cancelled.sum())

# 4. Negative quantities
print("\n4. NEGATIVE QUANTITIES")
print("Negative quantity rows:", (df["Quantity"] < 0).sum())

# 5. Zero or negative prices
print("\n5. PRICE VALIDATION")
print("Zero price rows:", (df["UnitPrice"] == 0).sum())
print("Negative price rows:", (df["UnitPrice"] < 0).sum())

# 6. Date range
print("\n6. INVOICE DATE ANALYSIS")

dates = pd.to_datetime(
    df["InvoiceDate"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

print("Earliest date:", dates.min())
print("Latest date:", dates.max())
print("Invalid dates:", dates.isna().sum())


print("Earliest date:", dates.min())
print("Latest date:", dates.max())
print("Invalid dates:", dates.isna().sum())

# 7. Country distribution
print("\n7. COUNTRY DISTRIBUTION")
print(df["Country"].value_counts().head(10))

# 8. Numeric data overview
print("\n8. NUMERIC DATA ANALYSIS")
print(df[["Quantity", "UnitPrice"]].describe())

print("\n========== AUDIT COMPLETED ==========")


print("\nDATE FORMAT INSPECTION")

print(df["InvoiceDate"].head(15).to_string(index=False))

print("\nUnique date examples:")
print(df["InvoiceDate"].sample(10, random_state=42).to_string(index=False))

