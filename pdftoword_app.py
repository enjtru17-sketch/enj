#!/usr/bin/env python
# coding: utf-8

# In[43]:


import streamlit as st
import PyPDF2
from docx import Document
import io

# 스트림릿 페이지 설정
st.set_page_config(page_title="PDF to Word Converter", page_icon="📄")

st.title("📄 PDF to Word (DOCX) 변환기")
st.write("PDF 파일을 업로드하면 워드(.docx) 파일로 변환하여 다운로드할 수 있습니다.")

# 1. 파일 업로더 생성
uploaded_file = st.file_uploader("PDF 파일을 선택하세요", type=["pdf"])

if uploaded_file is not None:
    st.success("파일이 성공적으로 업로드되었습니다!")

    # 변환 버튼
    if st.button("워드 파일로 변환"):
        try:
            # 2. PDF 읽기 (PyPDF2)
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            document = Document()

            # 페이지별 텍스트 추출 및 워드에 추가
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # 추출한 텍스트를 워드 파일에 paragraph로 추가
                document.add_paragraph(text)
                # 페이지 구분선 추가 (옵션)
                document.add_page_break()

            # 3. 인메모리(Memory)에 Word 파일 생성
            docx_buffer = io.BytesIO()
            document.save(docx_buffer)
            docx_buffer.seek(0)

            # 다운로드 버튼 생성
            st.download_button(
                label="📥 워드 파일 다운로드",
                data=docx_buffer,
                file_name=f"{uploaded_file.name.split('.')[0]}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.success("변환 완료!")

        except Exception as e:
            st.error(f"변환 중 오류가 발생했습니다: {e}")

else:
    st.info("PDF 파일을 업로드해주세요.")



# In[44]:






# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




