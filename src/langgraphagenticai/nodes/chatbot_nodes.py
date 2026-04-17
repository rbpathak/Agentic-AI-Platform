from src.langgraphagenticai.state.graph_state import State
import streamlit as st


class ChatbotNodes():
    def __init__(self, llm):
        self.llm = llm

    def chatbot(self,state:State):
        """This node will be used to retrieve data from llm by chatbot"""
        llm=self.llm
        try:
            result = llm.invoke(state["messages"])
        except Exception as e:
            st.error("API key is incorrect.")
            raise ValueError(f"Error loading LLM model: {e}")
        return {"messages":result}