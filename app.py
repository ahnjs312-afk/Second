import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="무한 러너", page_icon="🏃", layout="centered")

ASSETS_DIR = Path(__file__).parent / "assets"


def load_b64(filename):
    data = (ASSETS_DIR / filename).read_bytes()
    return base64.b64encode(data).decode("ascii")


def build_game_html():
    # Not cached on purpose: game_template.html and the assets are read fresh
    # every rerun (they're tiny, so this costs nothing) so an edit to the
    # template always shows up without needing to clear a stale cache.
    template = (Path(__file__).parent / "game_template.html").read_text(encoding="utf-8")
    html = template.replace("__TILESET_B64__", load_b64("tilemap.png"))
    html = html.replace("__CHARSET_B64__", load_b64("tilemap-characters.png"))
    return html


st.title("🏃 무한 러너")
st.caption("업로드된 타일셋으로 만든 무한 스크롤 서바이벌 게임이에요. 다가오는 땅을 밟으며 최대한 오래 버텨보세요!")

components.html(build_game_html(), height=560, scrolling=False)

with st.expander("조작법 / 게임 정보"):
    st.markdown(
        """
        - **이동**: 방향키 또는 `A` / `D`
        - **점프**: 스페이스바, `W`, 또는 `↑`
        - **적 처치**: 위에서 밟으면 처치, 옆에서 부딪히면 게임 오버
        - **게임 오버 조건**: 구멍 추락, 가시/적 접촉, 화면 왼쪽으로 밀려남
        - 시간이 지날수록 스크롤 속도와 난이도가 올라가요. 최고 기록은 브라우저에 저장돼요.
        - 화면 하단 버튼으로 모바일에서도 조작할 수 있어요.
        """
    )
