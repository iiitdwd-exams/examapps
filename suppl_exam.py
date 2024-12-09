from pathlib import Path
import uuid
import pandas as pd
import streamlit as st
from excel_protectcell import protect_cells
import zipfile


def display_df(header: str, df: pd.DataFrame, label="rows"):
    st.markdown(header)
    st.dataframe(df)
    st.write(f"{len(df)} {label}")


uploaded_file = st.file_uploader("F List in .xlsx or .csv format", ["xlsx", "csv"])
if uploaded_file is not None:
    fname = uploaded_file.name
    suffix = Path(fname).suffix
    cols = [
        "Roll No.",
        "Name",
        "Acad Period",
        "Code",
        "Course",
        "Credits",
        "Grade",
        "Degree",
        "Remarks",
    ]
    if suffix == ".xlsx":
        df = pd.read_excel(uploaded_file, usecols=cols)
    else:
        df = pd.read_csv(uploaded_file, usecols=cols)
    display_df("#### Raw Data", df)
else:
    st.stop()

# Map of month abbreviations to integers
month_map = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def split_acad_period(df):
    # Rename columns
    df.columns = [
        "roll_no",
        "name",
        "acad_period",
        "code",
        "course",
        "credits",
        "grade",
        "degree",
        "remarks",
    ]
    # Regular expression to extract the data (accounting for optional spaces around the hyphen)
    pattern = r"(\w+)(?:\s+(\d{4}))?\s*-\s*(\w+)\s+(\d{4})"
    # Extract the start month, start year, end month, and end year
    df[["start_month", "start_year", "end_month", "end_year"]] = df[
        "acad_period"
    ].str.extract(pattern)

    # Consider only the first three letters of the month and map to integers
    df["start_month"] = df["start_month"].str[:3].map(month_map)
    df["end_month"] = df["end_month"].str[:3].map(month_map)

    # Handle missing start years by replacing them with the corresponding end years
    df["start_year"] = df["start_year"].fillna(df["end_year"]).copy()

    # Convert year columns to integer
    df["start_year"] = df["start_year"].astype(int)
    df["end_year"] = df["end_year"].astype(int)

    # Drop the original academic_period column
    df = df.drop(columns=["acad_period"])

    return df


df1 = split_acad_period(df).copy()
display_df("#### Data with cleaned Academic Period", df1)


duplicate_rows_specific = df1[
    df1.duplicated(subset=["roll_no", "code", "end_month", "end_year"], keep=False)
]
display_df("#### Duplicate Rows", duplicate_rows_specific)

# Sort the DataFrame by roll_number, course_code, end_year, end_month
sorted_df = df.sort_values(by=["roll_no", "code", "end_year", "end_month"])

# Display the sorted DataFrame
# Drop duplicates, keeping only the last occurrence
unique_df = sorted_df.drop_duplicates(subset=["roll_no", "code"], keep="last")

# Display the resulting DataFrame
display_df("#### Data with only the last attempt", unique_df)


pivot_table = unique_df.pivot_table(
    index=["roll_no", "name"],
    values=["code", "credits"],
    aggfunc={"code": "count", "credits": "sum"},
).reset_index()

pivot_table.columns = ["roll_no", "name", "course_count", "total_credits"]
pivot_table = pivot_table.sort_values(
    by=["total_credits", "course_count"], ascending=False
).reset_index(drop=True)
display_df("#### Pivot Table", pivot_table, "students")

unique_courses = unique_df.drop_duplicates(
    subset=["code", "end_year", "end_month"]
).sort_values(by=["code", "end_year", "end_month"])
unique_courses[["code", "course", "acad_period"]].to_excel(
    "suppl_exam_course_list.xlsx", index=False
)
st.write(f"{len(unique_courses)} unique course and academic periods")

tmp_fname = f"{str(uuid.uuid4())}.csv"
unique_df.to_csv(tmp_fname, index=False)
with open(tmp_fname, "rb") as csv_file:
    btn = st.download_button(
        label="Download processed file",
        data=csv_file,
        file_name=f"{Path(uploaded_file.name).stem}.csv",
        mime="text/csv",
    )
tmp_fpath = Path(tmp_fname)
if tmp_fpath.exists():
    tmp_fpath.unlink()

students = unique_df["roll_no"].unique()
grouped = unique_df.groupby("roll_no")
chunks = [group for _, group in grouped]
xlsx_file_list = []
for student_df in chunks:
    student_df = student_df.sort_values(by=["end_year", "end_month", "code"])
    xlsx_df = student_df[
        ["roll_no", "name", "code", "course", "credits", "acad_period"]
    ].copy()
    xlsx_df["register"] = 0
    name = student_df.iloc[0, 1]
    roll_no = student_df.iloc[0, 0]
    xlsx_fname = f"{roll_no.lower()}.xlsx"
    st.write(f"{name} ({roll_no}) {xlsx_fname}")
    st.dataframe(xlsx_df)
    xlsx_df.to_excel(xlsx_fname, index=False)
    xlsx_file_list.append(xlsx_fname)
    protect_cells(xlsx_fname)

zip_fname = Path(uploaded_file.name).with_suffix(".zip").name
with zipfile.ZipFile(zip_fname, mode="w") as archive:
    for fname in xlsx_file_list:
        archive.write(fname)

with open(zip_fname, "rb") as f:
    st.download_button(
        label="Download Zip archive",
        data=f,
        file_name=zip_fname,
        mime="application/zip",
    )
for fname in xlsx_file_list:
    Path(fname).unlink()