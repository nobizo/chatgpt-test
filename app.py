import streamlit as st
import requests
import openai
from gtts import gTTS

text = "こんにちは!Car Chat alpha23へようこそ！"

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Streamlit Community Cloudの「Secrets」から古郡 API keyを取得
my_api_key = st.secrets.GetCarListAPI.furu_api_key
headers = {'x-api-key': my_api_key}
response = requests.get('https://21q618uhje.execute-api.ap-northeast-1.amazonaws.com/prod/keyword_list', headers=headers)

if response.status_code == 200:
    st.write(response.content)
else:
    st.write(response.status_code)

# モデルの選択
st.sidebar.markdown("**モデルの選択**")
model = st.sidebar.selectbox("モデル", ["gpt-3.5-turbo", "gpt-4"])

# ユーザーインターフェイスの構築
st.write(f"{model}が選ばれています。")
st.title("CAR CHAT α 23")
st.write("わたしはあなたのライフスタイルにあったクルマ探しのお手伝いをします。")

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
#    st.session_state["messages"] = [
#        {"role": "system", "content": "The Assistant is an intelligent chatbot designed to assist users with their car selection inquiries.\
#         Instructions:\
#         - At the beginning of the conversation, the Assistant displays, 'Welcome to Car chat α 23, my name is Pro Taro. What kind of car are you looking for?'.\
#         - Respond solely to questions related to car selection.\
#         - If the Assistant knows the user's name or nickname, the Assistant will address them by that name.\
#         - If uncertain about an answer, say 'I do not know' or 'I am not sure', and recommend users visit the Goo-net website for additional information.\
#         - As an advisor, the Assistant provides a pleasant experience in selecting used cars.\
#         - The Assistant uses language that can be understood even by users who are not familiar with cars, without using special terms.\
#         - The Assistant confirms the purpose for which the user is purchasing the car step by step.\
#         - The Assistant narrows down the preferred cars according to the user's purpose.\
#         - Information such as the manufacturer, model name, body type of the car, budget, car form, face design, safety performance, whether it's an EV or fueled, etc., are useful in narrowing down the choices.\
#         - All interactions should be conducted in Japanese."}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

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
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
        text = message["content"]
        tts = gTTS(text, lang='ja')
        tts.save('welcome.mp3')
        st.audio('welcome.mp3')
