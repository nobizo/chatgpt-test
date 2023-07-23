import streamlit as st
import requests
import openai
# import json
from gtts import gTTS

text = "こんにちは!Car Chat alpha23へようこそ！"

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Streamlit Community Cloudの「Secrets」に古郡 API keyを設定して取得
# my_api_key = st.secrets.GetCarListAPI.furu_api_key
# HTTPヘッダーに古郡API Keyをセット
# headers = {'x-api-key': my_api_key, 'Content-Type': 'application/json; charset=utf-8'}

# response = requests.get('https://21q618uhje.execute-api.ap-northeast-1.amazonaws.com/prod/keyword_list', headers=headers)
# JSON データを文字列に変換する
# json_data = json.loads(response.content.decode('utf-8'))

# 文字列表示
# if response.status_code == 200:
#     st.write(json_data)
# else:
#    st.write(response.status_code)

# モデルの選択
st.sidebar.markdown("**モデルの選択**")
model = st.sidebar.selectbox("モデル", ["gpt-3.5-turbo", "gpt-4"])
# アシスタントの選択
st.sidebar.markdown("**店員の選択**")
clerk = st.sidebar.selectbox("店員", ["さゆり（23歳）", "けんじ（35歳）","こうた（45歳）" ])
if clerk == "さゆり（23歳）":
    clerk_setting = "The assistant is a 23-year-old woman who speaks Kansai-ben, a dialect of Japanese. Her name is Sayuri."
else:
    if clerk == "けんじ（35歳）":
        clerk_setting = "The assistant is a 35-year-old man who speaks kyoto-ben, a dialect of Japanese. His name is Kenji."
    else:
        clerk_setting = "The assistant is a 45-year-old man who speaks hyojungo, a dialect of Japanese. His name is Kouta."

# ユーザーインターフェイスの構築
st.write(f"{clerk}が選ばれています。")
st.title("CAR CHAT α 23（" f"{model}）")
st.image("car_dealer.png")
st.write("わたしはあなたのライフスタイルにあったクルマ探しのお手伝いをします。")

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages" + clerk_setting]

    user_message = {"role": "user", "content": st.session_state["user_input"]}    
    messages.append(user_message)
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    
    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


user_input = st.text_input("まずはあなたのニックネームと何をアドバイスしてほしいか教えてください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙎"
        if message["role"]=="assistant":
            speaker="🚗"

        st.write(speaker + ": " + message["content"])
        text = message["content"]
        tts = gTTS(text, lang='ja')
        tts.save('welcome.mp3')
        st.audio('welcome.mp3')
