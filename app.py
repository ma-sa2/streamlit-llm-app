import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# ── アプリタイトル＆説明 ─────────────────────────────────────
st.set_page_config(page_title="LLM Expert Q&A アプリ", page_icon="🤖")
st.title("🤖 LLM Expert Q&A アプリ")
st.write("""
このアプリでは、自由にテキストを入力し、ラジオボタンで選んだ専門家の視点で
LLM からの回答を得ることができます。
- 専門家 A: 経営コンサルタント
- 専門家 B: マーケティングスペシャリスト

""")

# ── LLM 呼び出し用関数 ─────────────────────────────────────
def generate_response(user_input: str, expert: str) -> str:
    """
    user_input: ユーザーが入力したテキスト
    expert: ラジオボタンで選択された専門家の名前
    戻り値: LLM からの回答文字列
    """
    # ChatOpenAI インスタンス（temperature や model_name は必要に応じて調整）
    llm = ChatOpenAI(temperature=0.7)

    # 専門家ごとのシステムプロンプトを切り替え
    if expert == "経営コンサルタント":
        system_prompt = (
            "あなたは経験豊富な経営コンサルタントです。"
            "与えられた情報を分析し、論理的かつ実践的なアドバイスを提供してください。"
        )
    elif expert == "マーケティングスペシャリスト":
        system_prompt = (
            "あなたは優秀なマーケティングスペシャリストです。"
            "ターゲット市場やプロモーション戦略に関して具体的かつ創造的な提案をしてください。"
        )
    else:
        system_prompt = "あなたは有能な専門家です。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    # LLM にメッセージを投げて回答を取得
    response = llm(messages)
    return response.content

# ── UI: 専門家選択＆入力フォーム ─────────────────────────────
expert = st.radio(
    "専門家を選択してください",
    ["経営コンサルタント", "マーケティングスペシャリスト"]
)

user_input = st.text_area("質問を入力してください", height=150)

# ── 送信ボタン ────────────────────────────────────────────
if st.button("送信"):
    if not user_input.strip():
        st.warning("❗ 質問を入力してください。")
    else:
        with st.spinner("回答を生成中…"):
            answer = generate_response(user_input, expert)
        st.subheader("💡 回答")
        st.write(answer)
