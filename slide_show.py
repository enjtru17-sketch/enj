#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import time

st.set_page_config(page_title="사진 슬라이드쇼", layout="wide")
st.title("📸 사진 슬라이드쇼 및 보관함")

# 1. 세션 상태 초기화 (사진 보관용)
if "uploaded_photos" not in st.session_state:
    st.session_state.uploaded_photos = []

# 2. 사진 업로드 위젯
uploaded_files = st.file_uploader(
    "사진을 업로드하세요 (여러 개 선택 가능)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

# 업로드된 파일이 있으면 세션 상태에 추가 (중복 방지)
if uploaded_files:
    for file in uploaded_files:
        if file not in st.session_state.uploaded_photos:
            st.session_state.uploaded_photos.append(file)

# 3. 보관된 사진 관리 및 삭제 UI
if st.session_state.uploaded_photos:
    st.markdown("### 📂 보관된 사진 목록")

    # 3칸 그리드로 사진과 삭제 버튼 배치
    cols = st.columns(3)
    photos_to_remove = []

    for idx, photo in enumerate(st.session_state.uploaded_photos):
        with cols[idx % 3]:
            st.image(photo, use_column_width=True)
            if st.button("삭제", key=f"delete_{idx}"):
                photos_to_remove.append(photo)

    # 삭제 목록에 있는 사진 제거
    for photo in photos_to_remove:
        st.session_state.uploaded_photos.remove(photo)
        if "current_slide" in st.session_state:
            del st.session_state["current_slide"]
        st.rerun()

# 4. 슬라이드쇼 기능
if st.session_state.uploaded_photos:
    if st.button("▶️ 슬라이드 보여주기"):
        slide_placeholder = st.empty() # 슬라이드가 표시될 빈 공간

        # 세션 상태에 슬라이드 인덱스 저장 (순차 재생)
        if "current_slide" not in st.session_state:
            st.session_state.current_slide = 0

        for _ in range(len(st.session_state.uploaded_photos)):
            idx = st.session_state.current_slide
            photo = st.session_state.uploaded_photos[idx]

            with slide_placeholder.container():
                st.subheader(f"슬라이드 {idx + 1} / {len(st.session_state.uploaded_photos)}")
                st.image(photo, use_column_width=True)

            time.sleep(2) # 2초 대기 (숫자를 조정하여 속도 변경 가능)

            # 다음 슬라이드로 이동
            st.session_state.current_slide = (idx + 1) % len(st.session_state.uploaded_photos)
else:
    st.info("현재 보관된 사진이 없습니다. 사진을 업로드해 주세요!")

