#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import hashlib
import json
import time
import pandas as pd

# 1. 블록체인 구조 설계
class SimpleBlockchain:
    def __init__(self):
        # 세션 상태를 이용해 앱이 재실행되어도 데이터 유지
        if 'chain' not in st.session_state:
            st.session_state.chain = []
            self.create_block(proof=1, previous_hash='0', data="Genesis Block (시작 블록)")

    def create_block(self, proof, previous_hash, data):
        block = {
            'index': len(st.session_state.chain) + 1,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': data
        }
        st.session_state.chain.append(block)
        return block

    def get_last_block(self):
        return st.session_state.chain[-1]

    def hash(self, block):
        # 블록을 JSON으로 변환 후 해싱
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# 2. 스트림릿 UI 구성
def main():
    st.set_page_config(page_title="Blockchain Notepad", layout="wide")
    st.title("🔗 블록체인 변경불가 메모장")
    st.markdown("---")

    blockchain = SimpleBlockchain()

    # 왼쪽 사이드바: 메모 입력
    st.sidebar.header("📝 새 메모 작성")
    memo_content = st.sidebar.text_area("내용을 입력하세요", height=200)

    if st.sidebar.button("블록체인에 영구 기록"):
        if memo_content:
            last_block = blockchain.get_last_block()
            previous_hash = blockchain.hash(last_block)
            blockchain.create_block(proof=100, previous_hash=previous_hash, data=memo_content)
            st.sidebar.success(f"메모가 #{len(st.session_state.chain)}번 블록에 저장되었습니다!")
        else:
            st.sidebar.warning("내용을 입력해주세요.")

    # 메인 화면: 레이아웃 분할 (목록 | 상세내용)
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("📋 저장된 메모 목록")
        # Genesis 블록을 제외한 메모들 표시
        memos = st.session_state.chain[1:] 
        if memos:
            for i, block in enumerate(memos):
                # 클릭 시 해당 메모를 '상세 보기' 상태로 설정
                if st.button(f"📄 메모 #{block['index']} ({block['timestamp']})", key=f"memo_{i}", use_container_width=True):
                    st.session_state.current_view = block
        else:
            st.info("아직 기록된 메모가 없습니다.")

    with col2:
        st.subheader("🔍 메모 상세 정보")
        if 'current_view' in st.session_state:
            memo = st.session_state.current_view

            with st.container(border=True):
                st.write(f"**🔢 블록 번호:** {memo['index']}")
                st.write(f"**⏰ 기록 시간:** {memo['timestamp']}")
                st.write("**📄 메모 내용:**")
                st.info(memo['data'])
                st.caption(f"**🔗 이전 블록 해시:** `{memo['previous_hash']}`")

            # 선택된 특정 메모 다운로드
            single_memo_json = json.dumps(memo, indent=4, ensure_ascii=False)
            st.download_button(
                label="📥 현재 메모 다운로드 (JSON)",
                data=single_memo_json,
                file_name=f"memo_block_{memo['index']}.json",
                mime="application/json"
            )
        else:
            st.write("왼쪽 목록에서 메모를 선택해 주세요.")

    # 하단부: 전체 데이터 다운로드 섹션
    st.markdown("---")
    st.subheader("💾 전체 데이터 내보내기")

    if len(st.session_state.chain) > 1:
        c1, c2 = st.columns(2)

        # 전체 JSON 다운로드
        all_json = json.dumps(st.session_state.chain, indent=4, ensure_ascii=False)
        c1.download_button(
            label="📂 전체 기록 다운로드 (JSON)",
            data=all_json,
            file_name="blockchain_full_backup.json",
            mime="application/json",
            use_container_width=True
        )

        # 전체 CSV 다운로드
        df = pd.DataFrame(st.session_state.chain)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        c2.download_button(
            label="📊 전체 기록 다운로드 (CSV)",
            data=csv,
            file_name="blockchain_memos.csv",
            mime="text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




