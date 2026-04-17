import re
from typing import Literal
import streamlit as st

import requests
from bs4 import BeautifulSoup
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from src.langgraphagenticai.models.ArticleEvaluationResult import ArticleEvaluationResult
from src.langgraphagenticai.models.intent_result import IntentResult
from src.langgraphagenticai.state.graph_state import State


class NewsWriterNodes:
    def __init__(self, llm):
        self.llm = llm

    def intent_checker(self, state: State):
        """
        Check if the user query is related to content writing (article/blog/news).
        If not, inform the user and set is_relevant=False.
        """
        user_input = state["messages"][-1].content

        # Classification prompt
        prompt = PromptTemplate(
            template="""
                You are an intent classification assistant.
                Determine if the following user request is asking you to write, draft, or assist with
                an article/blog/content, OR if it is unrelated.

                USER INPUT:
                {query}

                Respond with:
                - is_relevant: Yes or No
                - response_message: 
                - If is_relevant is Yes, just say "Proceed".
                - If No, provide a polite single-paragraph message that can be directly shown to the user
                  and which clearly states that you can only write content and are only equipped with knowledge
                  about writing. For anything else please chat with the basic chatbot.
                """,
            input_variables=["query"]
        )

        # Use LLM with structured output
        structured_llm = self.llm.with_structured_output(IntentResult)
        chain = prompt | structured_llm

        try:
            result = chain.invoke({"query": user_input})
        except Exception as e:
            st.error("API key is incorrect.")
            raise ValueError(f"Error in LLM intent checker: {e}")

        print("intent_checker result")
        print(result)
        if result.is_relevant == "No":
            return {
                "messages": [AIMessage(content=result.response_message)],
                "is_valid": result.is_relevant
            }

        return {"messages": state["messages"], "is_valid": result.is_relevant}

    def intent_tool(self, state: State) -> Literal["generate", "__end__"]:
        """This tool will determine whether based on user query user needs to be redirected to another node or
        we need to end the graph."""
        if state["is_valid"] == "No":
            return "__end__"
        else:
            return "generate"

    def news_writer(self, state: State):
        """Generate a news article from either a short story description or a URL + description."""
        user_messages = state["messages"]
        print("inside news_writer")
        input_text = user_messages[-1].content

        urls = re.findall(r'https?://\S+', input_text)
        description = re.sub(r'https?://\S+', '', input_text).strip()

        user_input = ""

        if description:
            user_input += f"\n[User Description]\n{description}\n"

        if urls:
            user_input += "\n[Reference Articles]\n"
            for url in urls:
                article_text = self.fetch_article_from_url(url)
                user_input += f"\n--- Content from {url} ---\n{article_text}\n"

        if not user_input.strip():
            user_input = "No valid description or article URLs were provided."
        print("user_input inside news_writer")
        prompt = PromptTemplate(
            template="""
                You are an experienced news content writer.

                TASK:
                Based on the USER INPUT below and SUGGESTIONS if it exists, draft a clear, factual, and respectful news article.

                USER INPUT:
                {user_input}
                SUGGESTIONS:
                {suggestions}

                GUIDELINES:
                1. Accuracy:
                   - Do NOT invent facts.
                   - Only use details from the user description or the referenced URL.
                   - If a claim comes from an external source, attribute it explicitly
                     (e.g., "According to X, ...").
                2. Respect:
                   - Use respectful, neutral, and professional tone.
                   - Avoid disrespectful statements except when describing convicted criminals,
                     terrorists, or fraudsters.
                3. 5W1H Principles:
                   - Ensure the article answers:
                     - What happened?
                     - Who is involved?
                     - When did it happen?
                     - Where did it happen?
                     - Why did it happen?
                     - How did it happen?
                4. Structure:
                   - Write like a professional journalist.
                   - Include a headline, a short lead paragraph, and the body.

                Now draft the article:
                """,
            input_variables=["user_input", "suggestions"]
        )
        chain_news = prompt | self.llm
        suggestions = state.get("suggestions", "")
        try:
            result = chain_news.invoke({"user_input": user_input, "suggestions": suggestions})
        except Exception as e:
            st.error("API key is incorrect.")
            raise ValueError(f"Error loading LLM model: {e}")
        print("news_writer result")
        print(result)
        return {"messages": AIMessage(content=result.content)}

    # def evaluate_article(self, state: State):
    #     """Evaluate the generated article against accuracy, respect and 5W1H principles."""
    #     text = state["messages"][-1].content.strip()
    #     prompt = PromptTemplate(
    #         template="""
    #             You are an editor evaluating a draft news article for correctness, fairness, and structure.
    #
    #             **Article to evaluate:**
    #             {article_text}
    #
    #             Please evaluate the article against these criteria:
    #
    #             1. **Accuracy:**
    #                - Ensure the article does not make unverified claims on its own.
    #                - It may attribute statements correctly (e.g., "X said to Y"), but must not invent facts.
    #
    #             2. **Respect:**
    #                - Ensure the language is respectful and neutral, except in cases involving convicted criminals, terrorists, or fraudsters.
    #
    #             3. **5W1H Principles:**
    #                - Does the article clearly answer: What, Who, When, Where, Why, and How?
    #
    #             **Output:**
    #             - List any issues found, or say "No issues found".
    #             - Give a pass/fail status.
    #
    #             Respond in the format:
    #             is_valid: Valid/Not Valid
    #             suggestions: Suggestion why the article failed, empty if valid.
    #             """,
    #         input_variables=["article_text"]
    #     )
    #     llm = self.llm
    #     llm_with_structured_output = llm.with_structured_output(ArticleEvaluationResult)
    #     chain = prompt | llm_with_structured_output
    #     try:
    #         result = chain.invoke({"article_text": text})
    #     except Exception as e:
    #         st.error("API key is incorrect.")
    #         raise ValueError(f"Error loading LLM model: {e}")
    #
    #     print("evaluator result")
    #     print(result)
    #     return {"messages": state['messages'], "is_valid": result.is_valid, "suggestions": result.suggestions}
    #
    # def route(self, state: State) -> Literal["generate", "__end__"]:
    #     """Route the graph to either end or re-generate node based on validity."""
    #     if state["is_valid"] == "Valid":
    #         print("Enters valid route")
    #         return "__end__"
    #     else:
    #         print("Enters generate route")
    #         return "generate"

    def fetch_article_from_url(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            paragraphs = [p.get_text() for p in soup.find_all("p")]
            print(paragraphs)
            return "\n".join(paragraphs[:20])  # take first 20 paragraphs
        except Exception as e:
            return f"Error fetching article from URL: {e}"
