# from pathlib import Path
import streamlit as st
import pikepdf


def remove_password_from_pdf(fname: str, password: str, output_fname: str = ""):
    if not output_fname:
        output_fname = fname
        allow = True
    else:
        allow = False
    pdf = pikepdf.open(fname, password=password, allow_overwriting_input=allow)
    pdf.save(output_fname)


def overwrite_onchange():
    if overwrite:
        output_file = st.text_input("Name of cracked PDF file", fname, disabled=True)
    else:
        output_file = st.text_input("Name of cracked PDF file", fname, disabled=False)
    return output_file


if "pdf_overwrite" not in st.session_state:
    st.session_state.pdf_overwrite = True
if "pdf_input" not in st.session_state:
    pdf_input = ""


uploaded_file = st.file_uploader("Password protected PDF file", "pdf")
if uploaded_file is not None:
    fname = st.session_state.pdf_input = uploaded_file.name
    password = st.text_input("Password")
    overwrite = st.checkbox("Overwrite file", value=st.session_state.pdf_overwrite)
    pdf_output = st.text_input(
        "Name of cracked PDF file",
        fname,
        disabled=st.session_state.pdf_overwrite,
    )
else:
    st.stop()
