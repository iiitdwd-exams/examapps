from pathlib import Path
import uuid
import pandas as pd
import streamlit as st


def display_df(header: str, df: pd.DataFrame, label="rows"):
    st.markdown(header)
    st.dataframe(df)
    st.write(f"{len(df)} {label}")


uploaded_file = st.file_uploader("F List in .xlsx or .csv format", ["xlsx", "csv"])
if uploaded_file is not None:
    fname = uploaded_file.name
    suffix = Path(fname).suffix
    if suffix == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
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

st.write(f"{len(unique_df["code"].unique())} unique courses")

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
for index, row in unique_df.iterrows():
    student_df = unique_df[unique_df["roll_no"] == row["roll_no"]]
    name = student_df.iloc[0, 1]
    roll_no = student_df.iloc[0, 0]
    st.write(f"{name} ({roll_no}) {roll_no}_{name.replace(' ', '_')}.xlsx")
    st.dataframe(student_df[["code", "course"]])
