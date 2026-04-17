from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.langgraphagenticai.nodes.chatbot_nodes import ChatbotNodes
from src.langgraphagenticai.nodes.news_writer_nodes import NewsWriterNodes
from src.langgraphagenticai.state.graph_state import State


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder=StateGraph(State)

    def chatbot_workflow(self):
        self.chatbotnodes=ChatbotNodes(self.llm)
        self.graph_builder.add_node("chatbot",self.chatbotnodes.chatbot)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)


    def get_graph_by_usecase(self,usecase:str):
        if usecase=="Basic Chatbot":
            self.chatbot_workflow()
            return self.graph_builder.compile()
        elif usecase=="News Content Writer":
            print("Inside News Content Writer usecase")
            self.news_content_workflow()
            return self.graph_builder.compile()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")

    def news_content_workflow(self):
        newswriternodes=NewsWriterNodes(self.llm)
        self.graph_builder.add_node("intent_checker",newswriternodes.intent_checker)
        self.graph_builder.add_node("generate",newswriternodes.news_writer)
        #self.graph_builder.add_node("evaluator",newswriternodes.evaluate_article)
        self.graph_builder.add_edge(START,"intent_checker")
        #self.graph_builder.add_edge("generate","evaluator")
        self.graph_builder.add_conditional_edges("intent_checker",newswriternodes.intent_tool)
        #self.graph_builder.add_conditional_edges("evaluator",newswriternodes.route)
        self.graph_builder.add_edge("generate",END)

