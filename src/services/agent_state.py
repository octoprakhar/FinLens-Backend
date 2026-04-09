from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class FinLensState(TypedDict):
    messages :Annotated[List[BaseMessage], add_messages]
    documents: List[dict] ## We will append on it if the first search is bad
    query_count : int ## For a document no more than 3 query
    is_relevant: str ## yes, no, or maybe