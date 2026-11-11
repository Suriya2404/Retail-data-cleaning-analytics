
import pandas as pd
from pathlib import Path

from src.clean_data import clean_dataset
from src.generate_report import generate_reports

# Project paths
BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "OnlineRetail.csv"

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "OnlineRetail_Cleaned.csv"

# Load original dataset
print("Loading original dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="ISO-8859-1"
)

print("Original dataset shape:", df.shape)

# Run cleaning pipeline
cleaned_df, summary, validation = clean_dataset(df)

# Export cleaned dataset
cleaned_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nCleaned dataset exported successfully!")
print("Output location:", OUTPUT_FILE)

print("\nFinal dataset shape:", cleaned_df.shape)

# Generate professional reports
generate_reports(
    cleaned_df,
    summary,
    validation
)