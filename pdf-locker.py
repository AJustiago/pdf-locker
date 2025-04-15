import streamlit as st
from PyPDF2 import PdfReader, PdfWriter

def lock_pdf(input_pdf, output_pdf, password):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(output_pdf, "wb") as f:
        writer.write(f)

st.title("PDF Locker")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
password = st.text_input("Enter a password to lock the PDF", type="password")
output_filename = st.text_input("Enter the output filename (e.g., locked)")

if st.button("Lock PDF"):
    if uploaded_file and password and output_filename:
        try:
            with open("temp_uploaded.pdf", "wb") as temp_file:
                temp_file.write(uploaded_file.read())
            
            lock_pdf("temp_uploaded.pdf", output_filename, password)
            st.success(f"PDF locked successfully! Download: {output_filename}")
            with open(output_filename, "rb") as file:
                if not output_filename.endswith(".pdf"):
                    output_filename += ".pdf"
                st.download_button("Download Locked PDF", file, file_name=output_filename, mime="application/pdf")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a PDF, enter a password, and specify an output filename.")