"""
固收七人組 Team Match — Streamlit 外殼

跟「債速配」是同一套做法：這支程式只負責把 game.html 顯示出來，
並把 Supabase 的網址和金鑰填進去。遊戲本體在 game.html。

排行榜用的是同一張 flip_scores 資料表，但 BOARD_ID 不同
（game.html 裡是 "fi-team-7"），所以成績跟債速配分開算，
Supabase 不用重新建表。
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

PAGE_TITLE = "固收七人組 Team Match"

# 遊戲畫面高度（像素）。內容被切到就調大，下面空白太多就調小。
# 1900 是「七組全對、結語合照展開」之後的高度；還沒解鎖前下面會有一段空白，正常。
FRAME_HEIGHT = 1900

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .block-container { padding: 0 !important; max-width: 100% !important; }
      header[data-testid="stHeader"] { display: none; }
      #MainMenu, footer { visibility: hidden; }
      iframe { border: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_secret(key: str) -> str:
    """從 secrets.toml 讀一個值，沒設定就回空字串（遊戲仍可單機玩）。"""
    try:
        return str(st.secrets[key]).strip()
    except Exception:
        return ""


SUPABASE_URL = get_secret("SUPABASE_URL").rstrip("/")
SUPABASE_ANON_KEY = get_secret("SUPABASE_ANON_KEY")


@st.cache_data(show_spinner=False)
def load_template() -> str:
    return (Path(__file__).parent / "game.html").read_text(encoding="utf-8")


try:
    html = load_template()
except FileNotFoundError:
    st.error("找不到 game.html，請確認它和 app.py 放在同一個資料夾。")
    st.stop()

html = html.replace("__SUPABASE_URL__", SUPABASE_URL)
html = html.replace("__SUPABASE_ANON_KEY__", SUPABASE_ANON_KEY)

if not (SUPABASE_URL and SUPABASE_ANON_KEY):
    st.warning(
        "尚未設定 Supabase，排行榜不會共用（成績只留在自己的裝置）。"
        "請在 App settings → Secrets 填入 SUPABASE_URL 和 SUPABASE_ANON_KEY。",
        icon="⚠️",
    )

components.html(html, height=FRAME_HEIGHT, scrolling=True)
