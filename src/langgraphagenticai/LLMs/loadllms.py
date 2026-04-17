import os

import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from src.langgraphagenticai.commonconstants.constants import SELECTED_LLM, LLM_API_KEY, SELECTED_MODEL


class LoadLLMs():
    def __init__(self, user_control_input):
        self.user_controls_input = user_control_input

    def load_llms(self):
        try:
            match self.user_controls_input[SELECTED_LLM]:
                case "Groq":
                    model = self.load_groq_model()
                case "OpenAI":
                    model = self.load_openai_model()
                case _:
                    model = self.load_ollama_model()
            return model
        except Exception as e:
            st.error("Please re-check your API key with your selected LLM")
            raise ValueError(f"Error loading LLM model: {e}")

    def load_groq_model(self):
        os.environ["GROQ_API_KEY"] = self.user_controls_input[LLM_API_KEY]
        return ChatGroq(model=self.user_controls_input[SELECTED_MODEL], temperature=0)

    def load_openai_model(self):
        os.environ["OPENAI_API_KEY"] = self.user_controls_input[LLM_API_KEY]
        return ChatOpenAI(model=self.user_controls_input[SELECTED_MODEL], temperature=0)

    def load_ollama_model(self):
        return ChatOllama(model=self.user_controls_input[SELECTED_MODEL], temperature=0)
