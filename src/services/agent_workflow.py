from langgraph.graph import StateGraph,END
from src.services.agent_state import FinLensState
from src.services.agent_nodes import AgentNodes

def create_workflow(nodes: AgentNodes):
    workflow = StateGraph(FinLensState)

    ## FIrst we are adding all our three nodes
    workflow.add_node("retrieve",nodes.retrieve_node)
    workflow.add_node("grade", nodes.grade_node)
    workflow.add_node("rewrite", nodes.rewrite_node)
    workflow.add_node("generate", nodes.generate_node)

    ## Let's Start deffining the flow
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve","grade")

    ## Now let's decide whether from grade to generate or not
    def decide_to_generate(state:FinLensState):
        if state["is_relevant"] == "yes":
            return "generate"
        
        if state.get("query_count",0) < 1:
            return "rewrite"
        
        return "stop"
    
    workflow.add_conditional_edges(
        "grade",
        decide_to_generate,
        {
            "generate": "generate",
            "rewrite": "rewrite",
            "stop": END
        }
    )
    ## REwrite will be connected to retrieve
    workflow.add_edge("rewrite", "retrieve")

    workflow.add_edge("generate", END)

    return workflow.compile()