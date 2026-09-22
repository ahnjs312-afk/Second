import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from levels import LEVEL_1, LEVEL_2

st.set_page_config(page_title="픽셀 플랫포머", page_icon="🎮", layout="centered")

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
    html = html.replace("__LEVELS_JSON__", json.dumps([LEVEL_1, LEVEL_2]))
    return html


st.title("🎮 픽셀 플랫포머")
st.caption("업로드된 타일셋으로 만든 2단계 사이드스크롤 플랫포머예요. 동전을 모으고 깃발까지 도착해보세요!")

components.html(build_game_html(), height=560, scrolling=False)

with st.expander("조작법 / 게임 정보"):
    st.markdown(
        """
        - **이동**: 방향키 또는 `A` / `D`
        - **점프**: 스페이스바, `W`, 또는 `↑`
        - **적 처치**: 위에서 밟으면 처치, 옆에서 부딪히면 데미지
        - **목숨**: 3개, 가시/적/추락 시 감소
        - 화면 하단 버튼으로 모바일에서도 조작할 수 있어요.
        """
    )
