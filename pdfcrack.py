from pathlib import Path
import uuid
import streamlit as st
import pikepdf


uploaded_pdf = st.file_uploader("Password protected PDF file", type="pdf")
password = st.text_input("Password to open PDF file", value="ACWPA7045H")
tmp_pdf_name = f"{str(uuid.uuid4())}.pdf"
tmp_pdf_path = f"{tmp_pdf_name}"
if st.button("Remove password"):
    if uploaded_pdf is not None and password:
        try:
            # Open the uploaded file object in pikepdf
            decrypted_pdf = pikepdf.open(uploaded_pdf, password=password)
            # Save the decrypted PDF to a temporary file
            decrypted_pdf.save(tmp_pdf_path)
            st.success("Password removed successfully")
            # Download the saved decrypted file to local filesystem
            with open(tmp_pdf_path, "rb") as data:
                btn = st.download_button(
                    label="Download decrypted PDF file",
                    data=data,
                    file_name=uploaded_pdf.name,
                    mime="application/pdf",
                )
            fpath = Path(tmp_pdf_path)
            if fpath.exists():
                fpath.unlink()

        except Exception as e:
            st.error(f"Failed to remove password: {e}")
