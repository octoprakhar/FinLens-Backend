from langgraph.graph import StateGraph,END
from src.services.agent_state import FinLensState
from src.services.agent_nodes import AgentNodes
from langgraph.prebuilt import ToolNode, tools_condition

def create_workflow(nodes: AgentNodes):
    workflow = StateGraph(FinLensState)

    workflow.add_node("assistant", nodes.assistant_node)

    workflow.add_node("tools", ToolNode(nodes.get_tools()))

    workflow.set_entry_point("assistant")

    workflow.add_conditional_edges(
        "assistant",
        tools_condition, # If LLM calls a tool -> "tools", else -> END
    )

    workflow.add_edge("tools", "assistant")

    return workflow.compile()