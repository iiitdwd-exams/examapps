import streamlit as st

home_page = st.Page(
    "suppl_home.py",
    title="IIIT Dharwad Streamlit Apps",
    icon=":material/home:",
    default=True,
)

suppl_exam_page = st.Page(
    "suppl_exam.py",
    title="Supplementary Exam Statistics",
    icon=":material/book:",
)

pages = [home_page, suppl_exam_page]
page_dict = {"IIIT Dharwad": pages}
pg = st.navigation(page_dict)
pg.run()
