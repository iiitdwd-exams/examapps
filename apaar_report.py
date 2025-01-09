import re
import math
from pathlib import Path
from datetime import datetime
import pandas as pd

# from pandas import DataFrame
import streamlit as st


name_pattern = re.compile(r"^[a-z.\s]+$", re.I)
apaar_pattern = re.compile(r"^[0-9]{12}$")


academic_programs = ["CS", "DS", "EC"]
max_number = 175


def get_current_year():
    now = datetime.now()
    year = now.year
    month = now.month
    if month < 8:
        year -= 1
    return int(str(year)[-2:])


def display_df(header: str, df: pd.DataFrame, label="rows"):
    st.markdown(header)
    st.dataframe(df)
    st.write(f"{len(df)} {label}")


def read_data(datafile: str):
    if datafile is not None:
        fpath = Path(datafile)
        suffix = fpath.suffix
        if suffix in [".xlsx", ".xls"]:
            df = pd.read_excel(datafile)
        elif suffix == "csv":
            df = pd.read_csv(datafile)
        else:
            st.write(
                f"Data file {fpath.absolute} must be in one of .xlsx, .xls or .csv format"
            )
            st.stop()

        cols = [
            "timestamp",
            "email",
            "reg_no",
            "name",
            "name_aadhar",
            "aadhar_url",
            "apaar_id",
            "apaar_url",
            "agree",
            "undertaking",
        ]
        df.columns = cols
        return df
    else:
        st.stop()


def check_name(name: str):
    try:
        if math.isnan(float(name)):
            return " -> Name is empty"
    except Exception:
        pass
    s = re.sub(r"\s{2,}", " ", name.strip().lower())
    if len(s) == 0:
        return " -> Name is empty"
    if name_pattern.match(s):
        return ":material/done_outline:"
    else:
        return "Invalid characters, other than alphabets, spaces and . in name"


def compare_names(name1: str, name2: str):
    s1 = re.sub(r"\s{2,}", " ", name1.strip().lower())
    s2 = re.sub(r"\s{2,}", " ", name2.strip().lower())
    if name_pattern.match(s1) and name_pattern.match(s2):
        if s1 == s2:
            return ":material/done_outline:"
        else:
            return " -> Name as per AIMS and Aadhar name differ, but ok"


def validate_apaar_id(apaar_id):
    s = apaar_id.strip().replace("-", "").replace(" ", "")
    if apaar_pattern.match(s):
        return ":material/done_outline:"
    else:
        return "Invalid APAAR ID. Must be a 12 digit number"


def validate_googledrive_url(url: str):
    s = url.strip()
    if s.startswith("https://drive.google.com/open?id="):
        return ":material/done_outline:"
    else:
        return "Invalid URL for uploaded file"


def validate_ug_reg_no(reg_no: str) -> str:
    if len(reg_no) == 0:
        st.stop()
    elif len(reg_no) < 8:
        return "Length must be exactly equal to 8"
    try:
        year = int(reg_no[:2])
        current_year = get_current_year()
        if (year < 15) or (year > current_year):
            return f"Invalid year {year}. Must be between 15 and {current_year}"
    except Exception:
        return f"Invalid year {reg_no[:2]}"
    if reg_no[2].upper() != "B":
        return "Third character must be a 'B'"
    program = reg_no[3:5]
    if program.upper() not in academic_programs:
        return f"Academic program code {program} must be one of {academic_programs}"
    try:
        number = int(reg_no[-3:])
        if number > max_number:
            return f"Number {reg_no[-3:]} > {max_number}"
    except Exception:
        return f"Invalid number {reg_no[-3:]}"
    return "OK"


def report_reg_no(reg_no: str):
    msg = validate_ug_reg_no(reg_no)
    if msg == "OK":
        indx = df[df["reg_no"].str.replace(" ", "").str.lower() == reg_no.lower()].index
        if len(indx):
            st.markdown("#### Analysis Report")
            st.write(f"Registration Number: {reg_no.upper()}")
            name = str(df.loc[indx[0], "name"])
            st.write(f"Name as per AIMS: {name} {check_name(name)}")
            aadhar_name = str(df.loc[indx[0], "name_aadhar"])
            st.write(
                f"Name as per Aadhar: {aadhar_name} {compare_names(name, aadhar_name)}"
            )
            apaar_id = str(df.loc[indx[0], "apaar_id"])
            st.markdown(f"APAAR ID: {apaar_id} {validate_apaar_id(apaar_id)}")
            aadhar_url = str(df.loc[indx[0], "aadhar_url"])
            st.markdown(
                f"Aadhar upload URL: {aadhar_url} {validate_googledrive_url(aadhar_url)}"
            )
            apaar_url = str(df.loc[indx[0], "apaar_url"])
            st.write(
                f"APAAR upload URL: {apaar_url} {validate_googledrive_url(apaar_url)}"
            )
        else:
            st.write(f"{reg_no.upper()} not in responses")
    else:
        st.markdown(f"ERROR in **{reg_no}**: {msg}")
        st.stop()


def prepare_message():
    s = """Dear {name} ({reg_no}),

Following is the verification of the data submitted by you via Google Form:

"""


st.header("APAAR ID Report")

datafile = st.file_uploader(
    "APAAR ID Responses in .xlsx or .csv format", ["xlsx", ".xls", "csv"]
)
if datafile:
    df = read_data(datafile.name)
    display_df("#### Raw Data", df)

    reg_no = st.text_input("Registration Number", max_chars=8)
    report_reg_no(reg_no)
    # df_verified = verify_data(df)
    # display_df(
    #     "### Rows with 'empty' name field",
    #     df_verified[df_verified["valid_name"] == "Empty"],
    # )
    # display_df(
    #     "### Rows with invalid Registration Number",
    #     df_verified[df_verified["valid_reg_no"] == False],
    # )
    # display_df(
    #     "### Rows with 'empty' Aadhar upload",
    #     df_verified[df_verified["valid_aadhar_url"] == "Empty"],
    # )
    # display_df(
    #     "### Rows with 'empty' APAAR upload",
    #     df_verified[df_verified["valid_apaar_url"] == "Empty"],
    # )
    # display_df(
    #     "### Rows with invalid APAAR ID",
    #     df_verified[df_verified["valid_apaar_id"] == False],
    # )
else:
    st.write("Could not read data from file")
    st.stop()
