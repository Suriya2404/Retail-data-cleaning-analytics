
import pandas as pd
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def format_excel_report(excel_file):
    """Apply professional formatting to the Excel workbook."""

    wb = load_workbook(excel_file)

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="17365D"
    )

    header_font = Font(
        bold=True,
        color="FFFFFF",
        size=11
    )

    thin_border = Border(
        bottom=Side(style="thin", color="D9E2F3")
    )

    for ws in wb.worksheets:

        # Freeze header
        ws.freeze_panes = "A2"

        # Enable filters
        ws.auto_filter.ref = ws.dimensions

        # Format header cells
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )
            cell.border = thin_border

        # Calculate readable column widths
        # Inspect only the first 1000 rows for performance
        sample_rows = min(ws.max_row, 1000)

        for col_index in range(1, ws.max_column + 1):

            max_length = 0

            for row in ws.iter_rows(
                min_row=1,
                max_row=sample_rows,
                min_col=col_index,
                max_col=col_index,
                values_only=True
            ):
                value = row[0]

                if value is not None:
                    max_length = max(
                        max_length,
                        len(str(value))
                    )

            column_letter = get_column_letter(col_index)

            ws.column_dimensions[column_letter].width = min(
                max(max_length + 3, 14),
                35
            )

        ws.row_dimensions[1].height = 25

    # Worksheet tab colours
    wb["Cleaned Data"].sheet_properties.tabColor = "4472C4"
    wb["Data Quality Summary"].sheet_properties.tabColor = "70AD47"
    wb["Validation Report"].sheet_properties.tabColor = "ED7D31"

    wb.save(excel_file)
    wb.close()

    print("Professional Excel formatting applied!")


def generate_reports(cleaned_df, summary, validation):

    base_dir = Path(__file__).resolve().parent.parent

    report_dir = base_dir / "reports"
    output_dir = base_dir / "data" / "processed"

    report_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    excel_file = output_dir / "OnlineRetail_Cleaned.xlsx"
    report_file = report_dir / "data_quality_report.txt"
    summary_file = report_dir / "cleaning_summary.csv"

    print("\n========== GENERATING REPORTS ==========")

    # Create summary tables
    summary_df = pd.DataFrame(
        list(summary.items()),
        columns=["Metric", "Value"]
    )

    validation_df = pd.DataFrame(
        list(validation.items()),
        columns=["Validation Check", "Records"]
    )

    # Export Excel workbook
    print("Creating Excel workbook...")

    with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
    ) as writer:

        cleaned_df.to_excel(
            writer,
            sheet_name="Cleaned Data",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Data Quality Summary",
            index=False
        )

        validation_df.to_excel(
            writer,
            sheet_name="Validation Report",
            index=False
        )

    print("Excel workbook created.")

    # Format Excel workbook
    format_excel_report(excel_file)

    # Export summary CSV
    summary_df.to_csv(
        summary_file,
        index=False
    )

    print("Cleaning summary CSV created.")

    # Generate text report
    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("ONLINE RETAIL DATA QUALITY REPORT\n")
        file.write("=" * 45 + "\n\n")

        file.write("CLEANING SUMMARY\n")
        file.write("-" * 25 + "\n")

        for key, value in summary.items():
            file.write(f"{key}: {value}\n")

        file.write("\nVALIDATION RESULTS\n")
        file.write("-" * 25 + "\n")

        for key, value in validation.items():
            file.write(f"{key}: {value}\n")

        file.write("\nReport generated successfully.\n")

    print("Text report created.")

    print("\n========== REPORT GENERATION COMPLETED ==========")
    print("Excel:", excel_file)
    print("Summary CSV:", summary_file)
    print("Text report:", report_file)
