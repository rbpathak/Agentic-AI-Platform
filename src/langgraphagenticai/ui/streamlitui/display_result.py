from typing import Any

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from src.langgraphagenticai.memory.chat_history import ChatHistory


class DisplayResultStreamLit:
    def __init__(self, graph, usecase, user_message):
        self.graph = graph
        self.usecase = usecase
        self.user_message = user_message

    def display_result_on_ui(self):
        print("Hi Rohit Here")
        usecase = self.usecase
        graph = self.graph
        session_id = st.session_state["thread_id"]

        # Load or create chat history
        history = ChatHistory.get_session_history(session_id)

        # Add user message to history
        history.add_message(HumanMessage(content=self.user_message))

        # Build messages from history
        messages = history.messages
        print("Hi Dhruv Here 2")

        final_response = None  # To store only the last message from the assistant

        # Stream through graph events
        for event in graph.stream({"messages": messages}):
            print(event.values())
            for value in event.values():
                messages_data = value.get("messages")
                if messages_data:
                    # Ensure messages_data is a list
                    if not isinstance(messages_data, list):
                        messages_data = [messages_data]

                    # Always take the last message in this batch
                    last_msg = messages_data[-1]
                    final_response = getattr(last_msg, "content", str(last_msg))

                if "is_valid" in value:
                    print(f"Evaluation Result: {value['is_valid']} - {value.get('suggestions', '')}")

        # After the loop finishes, display only the final response
        if final_response:
            history.add_message(AIMessage(content=final_response))
            with st.chat_message("user"):
                st.write(self.user_message)
            with st.chat_message("assistant"):
                st.write(final_response)