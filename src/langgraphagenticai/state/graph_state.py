from typing import TypedDict, Annotated, Optional

from langgraph.graph import add_messages


class State(TypedDict):
    messages: Annotated[list,add_messages]
    is_valid: Optional[str]
    suggestions: Optional[str]