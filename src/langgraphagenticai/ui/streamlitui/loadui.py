from src.langgraphagenticai.commonconstants.constants import SELECTED_LLM, LLM_API_KEY, SELECTED_MODEL, SELECTED_USECASE
from src.langgraphagenticai.ui.streamlitui.uiconfigfile import Config
import streamlit as st
import os


class LoadStreamLitUi:
    def __init__(self):
        self.config= Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title= self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_use_case_options()


            self.user_controls[SELECTED_LLM]=st.selectbox("Select LLM", llm_options)
            model_options=[]
            match self.user_controls[SELECTED_LLM]:
                case "Groq":
                    model_options=self.config.get_groq_model_options()
                    self.user_controls[LLM_API_KEY]=st.text_input("API Key", type="password")
                    if not self.user_controls[LLM_API_KEY]:
                        st.warning("Please set your Groq API key to proceed. Don't have please refer : https://console.groq.com/keys")
                case "OpenAI":
                    model_options=self.config.get_openai_model_options()
                    self.user_controls[LLM_API_KEY]=st.text_input("API Key", type="password")
                    if not self.user_controls[LLM_API_KEY]:
                        st.warning("Please set your Open API key to proceed. Don't have please refer : https://platform.openai.com/api-keys")
                case _:
                    model_options=self.config.get_ollama_model_options()

            self.user_controls[SELECTED_MODEL]=st.selectbox("Select Model", model_options)
            self.user_controls[SELECTED_USECASE]=st.selectbox("Select Usecase", usecase_options)

        return self.user_controls
