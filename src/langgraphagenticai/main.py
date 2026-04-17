import pathlib
import uuid

import streamlit as st

from src.langgraphagenticai.LLMs.loadllms import LoadLLMs
from src.langgraphagenticai.commonconstants.constants import SELECTED_USECASE, LLM_API_KEY, SELECTED_LLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.memory.chat_history import ChatHistory
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamLit
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamLitUi


def load_langgraph_agentic_app():
    ui = LoadStreamLitUi()

    #create thread id for in memorySaver()
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = str(uuid.uuid4())

    #reset thread to start a new conversation
    if st.button("Reset Conversation"):
        ChatHistory.clear_history(st.session_state["thread_id"])
        st.session_state["thread_id"] = str(uuid.uuid4())
        st.success("Conversation reset. A new thread has been created.")

    st.sidebar.write(f"Current Thread ID: {st.session_state['thread_id']}")

    user_input=ui.load_streamlit_ui()
    if user_input[SELECTED_LLM] !="Ollama":
        if not user_input[LLM_API_KEY]:
            st.error("API key is Required.")


    user_message = st.chat_input("Enter you message:")

    if user_message:
        print(user_message)
        load_llm = LoadLLMs(user_input)
        llm = load_llm.load_llms()
        print(llm)
        graph_builder = GraphBuilder(llm)
        usecase = user_input[SELECTED_USECASE]
        print(usecase)
        graph = graph_builder.get_graph_by_usecase(usecase)
        print(graph)
        #png_data = graph.get_graph().draw_mermaid_png()

        # Save it to a file
        #output_path = pathlib.Path("news_content_writer.png")
        #output_path.write_bytes(png_data)
        DisplayResultStreamLit(graph, usecase, user_message).display_result_on_ui()
    else:
        return
