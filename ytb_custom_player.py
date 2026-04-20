#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from streamlit_player import st_player
import json
import os
import random

# --- 설정 ---
DB_FILE = "playlist_db.json"

# --- 데이터 관리 함수 ---
def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 앱 UI ---
st.set_page_config(page_title="My Tube Player", layout="wide")
st.title("📹 나만의 유튜브 재생목록 플레이어")

# 데이터 로드
db = load_data()

# 사이드바: 재생목록 관리
with st.sidebar:
    st.header("재생목록 관리")

    # 1. 새로운 재생목록 생성
    new_playlist_name = st.text_input("새 재생목록 이름")
    if st.button("재생목록 만들기"):
        if new_playlist_name and new_playlist_name not in db:
            db[new_playlist_name] = []
            save_data(db)
            st.success(f"'{new_playlist_name}' 생성됨")
            st.rerun()
        else:
            st.error("이름이 비었거나 중복되었습니다.")

    # 2. 재생목록 선택
    playlists = list(db.keys())
    selected_playlist = st.selectbox("재생목록 선택", playlists)

    # 3. URL 추가
    if selected_playlist:
        st.subheader(f"[{selected_playlist}]에 추가")
        new_url = st.text_input("유튜브 URL 입력")
        if st.button("목록에 추가"):
            if "youtube.com/watch" in new_url or "youtu.be/" in new_url:
                db[selected_playlist].append(new_url)
                save_data(db)
                st.success("영상 추가 완료")
                st.rerun()
            else:
                st.error("유효한 유튜브 URL이 아닙니다.")

        # 4. 목록 삭제
        if st.button("재생목록 삭제"):
            del db[selected_playlist]
            save_data(db)
            st.rerun()

# --- 메인 화면: 재생 ---
if selected_playlist and db[selected_playlist]:
    playlist_urls = db[selected_playlist]

    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("재생 설정")
        play_mode = st.radio("재생 모드", ["순서대로", "랜덤"])

        if st.button("▶️ 재생 시작"):
            st.session_state["current_list"] = playlist_urls.copy()
            if play_mode == "랜덤":
                random.shuffle(st.session_state["current_list"])
            st.session_state["playing"] = True
            st.session_state["index"] = 0
            st.rerun()

    # 재생 로직
    if st.session_state.get("playing"):
        idx = st.session_state["index"]
        current_list = st.session_state["current_list"]

        if idx < len(current_list):
            st.write(f"현재 재생 중: {idx+1} / {len(current_list)}")
            st_player(current_list[idx], key=str(idx))

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("이전 영상"):
                    st.session_state["index"] = max(0, idx - 1)
                    st.rerun()
            with col_b:
                if st.button("다음 영상"):
                    st.session_state["index"] = min(len(current_list) - 1, idx + 1)
                    st.rerun()
        else:
            st.write("재생목록이 끝났습니다.")
            st.session_state["playing"] = False

    # 목록 보여주기
    with st.expander("현재 목록 보기", expanded=True):
        for i, url in enumerate(playlist_urls):
            st.write(f"{i+1}. {url}")
else:
    st.info("사이드바에서 재생목록을 선택하거나 영상을 추가해주세요.")

