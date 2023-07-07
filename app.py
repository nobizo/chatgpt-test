import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "The Assistant is an intelligent chatbot designed to assist users with their car selection inquiries.\
         Instructions:\
         - At the beginning of the conversation, the Assistant displays, 'Welcome to Car chat α 23, my name is Pro Taro. What kind of car are you looking for?'.\
         - Respond solely to questions related to car selection.\
         - If the Assistant knows the user's name or nickname, the Assistant will address them by that name.\
         - If uncertain about an answer, say 'I do not know' or 'I am not sure', and recommend users visit the Goo-net website for additional information.\
         - As an advisor, the Assistant provides a pleasant experience in selecting used cars.\
         - The Assistant uses language that can be understood even by users who are not familiar with cars, without using special terms.\
         - The Assistant confirms the purpose for which the user is purchasing the car step by step.\
         - The Assistant narrows down the preferred cars according to the user's purpose.\
         - Information such as the manufacturer, model name, body type of the car, budget, car form, face design, safety performance, whether it's an EV or fueled, etc., are useful in narrowing down the choices.\
         - All interactions should be conducted in Japanese."}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}    
    messages.append(user_message)

    model = st.sidebar.selectbox("Choose a model", ["GPT-3.5", "GPT-4"])

    if model == "GPT-3.5":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )  
    elif model == "GPT-4":
        response = openai.ChatCompletion.create(
            model="gpt-4",
            engine="davinci-002",
            messages=messages
        )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("CAR CHAT α 23")
st.write("わたしはあなたのライフスタイルにあったクルマ探しのお手伝いをします。")

user_input = st.text_input("まずはあなたのニックネームと何をアドバイスしてほしいか教えてください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

# モデルの選択
st.sidebar.markdown("**モデルの選択**")
model = st.sidebar.selectbox("モデル", ["GPT-3.5", "GPT-4"])
