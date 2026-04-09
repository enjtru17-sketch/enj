#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
from PIL import Image
import io

# 앱 제목 설정
st.title("🖼️ 이미지 압축 및 다운로드 앱")
st.write("이미지를 업로드하고 원하는 퀄리티를 선택하여 최적화하세요.")

# 1. 파일 업로더 생성
uploaded_file = st.file_uploader("이미지 파일 선택 (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

# 2. 압축 퀄리티 선택 슬라이더 (추가된 부분)
# 1~100 사이의 값을 선택하며, 기본값은 50으로 설정했습니다.
quality = st.sidebar.slider("이미지 퀄리티 선택", min_value=1, max_value=100, value=50)
st.sidebar.info(f"현재 설정된 퀄리티: {quality} (낮을수록 용량 감소)")

if uploaded_file is not None:
    # 3. 업로드된 파일 열기
    image = Image.open(uploaded_file)

    # 4. 이미지 모드 변환 (PNG(RGBA) -> JPEG(RGB))
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    st.image(image, caption='원본 이미지', use_container_width=True)
    st.write(f"퀄리티 {quality}로 압축 중...")

    # 5. 이미지 압축 처리 (선택한 quality 값 적용)
    buf = io.BytesIO()
    # 유저가 선택한 quality 변수를 여기에 적용합니다.
    image.save(buf, format="JPEG", optimize=True, quality=quality)
    byte_im = buf.getvalue()

    st.success(f"압축 완료! (예상 용량: {len(byte_im) / 1024:.2f} KB)")

    # 6. 다운로드 버튼 생성
    st.download_button(
        label="📥 압축 이미지 다운로드",
        data=byte_im,
        file_name=f"compressed_q{quality}.jpg",
        mime="image/jpeg")



# In[9]:





# In[10]:





# In[ ]:





# In[ ]:




