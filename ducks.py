import os
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from dotenv import load_dotenv

# 🔐 Set your Gemini API key directly here (temporary local use)
os.environ["GOOGLE_API_KEY"] = "AIzaSyC_iRD_Ss1ayBXadgIIrHAoMKu2xoXkTFY"  # <-- Replace this with your real key

# ✅ Load .env if needed (optional now)
load_dotenv()

# ✅ Set page configuration
st.set_page_config(page_title="🔍 Ask Anything App", page_icon="🤖")

# 🎨 UI Elements
st.title("🤖 Ask Anything with Gemini + DuckDuckGo")
st.write("Type a question and get an answer powered by **Google Gemini** and **DuckDuckGo Search** 🌍")

# 💬 Text input
user_question = st.text_input("Ask your question here:", placeholder="e.g., What’s the latest AI news?")
ask_button = st.button("🔎 Search & Answer")

# 🚀 Initialize model and tools
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)
    ddg_tool = DuckDuckGoSearchRun()
    tools = [
        Tool.from_function(
            func=ddg_tool.run,
            name="DuckDuckGo Search",
            description="Useful for answering questions about current events or topics on the web."
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False
    )

    if ask_button and user_question.strip():
        with st.spinner("Thinking... 🤔"):
            try:
                response = agent.run(user_question)
                st.success("✅ Answer:")
                st.write(response)
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")
    elif ask_button:
        st.warning("⚠️ Please enter a question before pressing the button.")

except Exception as e:
    st.error(f"❌ Failed to load the model or tools.\n\n{e}")
    st.stop()
