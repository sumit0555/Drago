import streamlit as st
import requests
import pyttsx3
import openai
import os

# Setup page
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 AI Assistant")
st.markdown("Type your command below (e.g., `news`, `joke`, `hello`, `weather in delhi`, or any question)")

# Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_latest_news():
    api_key = os.getenv("NEWSAPI_KEY")  # Environment variable
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])[:5]
    return [article["title"] for article in articles]

def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode"
    response = requests.get(url)
    joke_data = response.json()
    if joke_data["type"] == "single":
        return joke_data["joke"]
    else:
        return joke_data["setup"] + " ... " + joke_data["delivery"]

def chat_with_gpt(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Environment variable
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Input box
command = st.text_input("Your Command:", "")

if command:
    command = command.lower()
    if 'hello' in command:
        response = "Hi dost! What can I do for you?"
    elif 'news' in command:
        st.subheader("📰 Top News Headlines:")
        news_list = get_latest_news()
        for news in news_list:
            st.write("-", news)
        response = "Here are the top headlines."
    elif 'joke' in command:
        joke = get_joke()
        st.success(joke)
        response = joke
    elif 'bye' in command or 'exit' in command:
        response = "Goodbye dost! See you soon."
    else:
        response = chat_with_gpt(command)

    st.markdown(f"**Assistant:** {response}")
    speak(response)
  
