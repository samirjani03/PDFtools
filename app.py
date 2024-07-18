import streamlit as st
import os
import tempfile
from utils import pdf_operations, image_operations, office_operations, compression

def main():
    st.title("PDF and Image Tools")

    tool = st.sidebar.selectbox(
        "Select a tool",
        ["PDF to JPG", "JPG to PDF", "Encrypt PDF", "Decrypt PDF", "Compress PDF",
         "PDF to Word", "Word to PDF", "PDF to PPT", "PPT to PDF", "Excel to PDF",
         "Merge PDFs", "Remove Pages from PDF", "Add Pages to PDF", "Split PDF",
         "Unlock PDF", "PDF to HTML", "PNG to PDF", "JPG to PNG", "PNG to JPG"]
    )

    if tool == "PDF to JPG":
        pdf_file = st.file_uploader("Upload PDF file", type="pdf")
        if pdf_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                tmp_file_path = tmp_file.name

            with tempfile.TemporaryDirectory() as output_folder:
                st.info("Converting PDF to JPG...")
                jpg_paths = pdf_operations.pdf_to_jpg(tmp_file_path, output_folder)
                
                st.success("Conversion complete!")
                for i, jpg_path in enumerate(jpg_paths):
                    with open(jpg_path, "rb") as file:
                        st.download_button(
                            label=f"Download Page {i+1}",
                            data=file,
                            file_name=f"page_{i+1}.jpg",
                            mime="image/jpeg"
                        )
            
            os.unlink(tmp_file_path)

    elif tool == "JPG to PDF":
        jpg_files = st.file_uploader("Upload JPG files", type="jpg", accept_multiple_files=True)
        if jpg_files:
            with tempfile.TemporaryDirectory() as tmp_dir:
                jpg_paths = []
                for jpg_file in jpg_files:
                    tmp_path = os.path.join(tmp_dir, jpg_file.name)
                    with open(tmp_path, "wb") as f:
                        f.write(jpg_file.getvalue())
                    jpg_paths.append(tmp_path)
                
                output_path = os.path.join(tmp_dir, "output.pdf")
                st.info("Converting JPG to PDF...")
                pdf_operations.jpg_to_pdf(jpg_paths, output_path)
                
                st.success("Conversion complete!")
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download PDF",
                        data=file,
                        file_name="combined.pdf",
                        mime="application/pdf"
                    )

    elif tool == "Encrypt PDF":
        pdf_file = st.file_uploader("Upload PDF file", type="pdf")
        password = st.text_input("Enter encryption password", type="password")
        if pdf_file and password:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                input_path = tmp_file.name

            output_path = input_path.replace(".pdf", "_encrypted.pdf")
            st.info("Encrypting PDF...")
            pdf_operations.encrypt_pdf(input_path, output_path, password)
            
            st.success("Encryption complete!")
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download Encrypted PDF",
                    data=file,
                    file_name="encrypted.pdf",
                    mime="application/pdf"
                )
            
            os.unlink(input_path)
            os.unlink(output_path)
    elif tool == "PDF to Word":
        pdf_file = st.file_uploader("Upload PDF file", type="pdf")
        if pdf_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                pdf_path = tmp_file.name

            docx_path = pdf_path.replace(".pdf", ".docx")
            st.info("Converting PDF to Word...")
            office_operations.pdf_to_word(pdf_path, docx_path)
            
            st.success("Conversion complete!")
            with open(docx_path, "rb") as file:
                st.download_button(
                    label="Download Word Document",
                    data=file,
                    file_name="converted.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
            os.unlink(pdf_path)
            os.unlink(docx_path)
        # Add more elif blocks for other tools...
        
    elif tool == "Decrypt PDF":
        pdf_file = st.file_uploader("Upload encrypted PDF file", type="pdf")
        password = st.text_input("Enter decryption password", type="password")
        if pdf_file and password:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                input_path = tmp_file.name
    
            output_path = input_path.replace(".pdf", "_decrypted.pdf")
            st.info("Decrypting PDF...")
            try:
                pdf_operations.decrypt_pdf(input_path, output_path, password)
            except ValueError as e:
                st.error(f"Decryption failed: {str(e)}")
            finally:
                os.unlink(input_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)
    elif tool == "Merge PDFs":
        pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True,)
        if pdf_files and len(pdf_files) > 1:
            with tempfile.TemporaryDirectory() as tmp_dir:
                pdf_paths = []
                for pdf_file in pdf_files:
                    tmp_path = os.path.join(tmp_dir, pdf_file.name)
                    with open(tmp_path, "wb") as f:
                        f.write(pdf_file.getvalue())
                    pdf_paths.append(tmp_path)
                
                output_path = os.path.join(tmp_dir, "merged.pdf")
                st.info("Merging PDFs...")
                pdf_operations.merge_pdfs(pdf_paths, output_path)
                
                st.success("Merge complete!")
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Merged PDF",
                        data=file,
                        file_name="merged.pdf",
                        mime="application/pdf"
                    )
        elif pdf_files:
            st.warning("Please upload at least two PDF files to merge.")
        else:
            st.info("Please upload PDF files to merge.")
    # elif tool == "Decrypt PDF":
    #     pdf_file = st.file_uploader("Upload encrypted PDF file", type="pdf")
    #     password = st.text_input("Enter decryption password", type="password")
    #     if pdf_file and password:
    #         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
    #             tmp_file.write(pdf_file.getvalue())
    #             input_path = tmp_file.name

    #         output_path = input_path.replace(".pdf", "_decrypted.pdf")
    #         st.info("Decrypting PDF...")
    #         try:
    #             pdf_operations.decrypt_pdf(input_path, output_path, password)
    #             st.success("Decryption complete!")
    #             with open(output_path, "rb") as file:
    #                 st.download_button(
    #                     label="Download Decrypted PDF",
    #                     data=file,
    #                     file_name="decrypted.pdf",
    #                     mime="application/pdf"
    #                 )
    #         except ValueError as e:
    #             st.error(f"Decryption failed: {str(e)}")
    #         finally:
    #             os.unlink(input_path)
    #             if os.path.exists(output_path):
    #                 os.unlink(output_path)
if __name__ == "__main__":
    main()