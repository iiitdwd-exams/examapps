import streamlit as st

home_page = st.Page(
    "suppl_home.py",
    title="IIIT Dharwad Streamlit Apps",
    icon=":material/home:",
    default=True,
)

suppl_exam_page = st.Page(
    "suppl_exam.py",
    title="Supplementary Exam Stats",
    icon=":material/book:",
)

pdfcrack_page = st.Page(
    "pdfcrack.py",
    title="Remove PDF password",
    icon=":material/no_encryption:",
)

apaar_page = st.Page(
    "apaar_report.py", title="Prepare APAAR ID Report", icon=":material/summarize:"
)

pages = [home_page, suppl_exam_page, pdfcrack_page, apaar_page]
page_dict = {"IIIT Dharwad": pages}
pg = st.navigation(page_dict)
pg.run()
