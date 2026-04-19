#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code(url, fill_color, back_color):
    """URL을 QR 코드 이미지로 변환하는 함수"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

# --- 앱 UI 구성 ---
st.set_page_config(page_title="URL QR 생성기", page_icon="📱")

st.title("📱 URL QR 코드 생성기")
st.write("URL을 입력하면 자동으로 QR 코드를 생성해 줍니다.")

# 1. URL 입력
url = st.text_input("QR코드로 변환할 URL을 붙여넣으세요", placeholder="https://example.com")

# 2. 색상 설정 (선택 사항)
with st.expander("색상 설정"):
    fill_color = st.color_picker("QR 코드 색상", "#000000")
    back_color = st.color_picker("배경 색상", "#FFFFFF")

# 3. QR 코드 생성 버튼
if st.button("QR 코드 생성"):
    if url:
        try:
            # QR 코드 생성
            img = generate_qr_code(url, fill_color, back_color)

            # 이미지를 스트림릿에서 표시하기 위해 바이트 변환
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # 이미지 표시
            st.image(byte_im, caption="생성된 QR 코드", width=300)

            # 다운로드 버튼
            st.download_button(
                label="QR 코드 다운로드",
                data=byte_im,
                file_name="qrcode.png",
                mime="image/png"
            )
            st.success("QR 코드가 생성되었습니다!")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("URL을 입력해주세요.")

# 하단 푸터
st.markdown("---")
st.caption("Streamlit으로 만든 간단한 QR 생성기")

