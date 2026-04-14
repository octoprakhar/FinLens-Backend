from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

import os
import json


from src.services.agent_state import FinLensState
from src.components.RagPdf import RagPipeline

class AgentNodes:
    def __init__(self, rag_pipeline: RagPipeline):
        self.rag_pipeline = rag_pipeline

        # self.llm = ChatGoogleGenerativeAI(
        #      model="gemini-2.5-flash",
        #      google_api_key=rag_pipeline.config.gemini_api_key,
        #      temperature=0
        # )
        self.llm = ChatOllama(
            model="qwen2.5-coder:7b",
            temperature=0,
            # This ensures the model uses your Nvidia GPU
            num_gpu=1,
            verbose=True
        )

    def get_tools(self):
         @tool
         def search_pdf(query:str):
              
              """Search the financial PDF for factual data and numbers."""
              return self.rag_pipeline._search(query=query)
    
         return [search_pdf]

    
    def assistant_node(self, state: FinLensState):
        count = state.get("query_count", 0)
        if count >= 5:
            print("⚠️ [SAFE EXIT] MAX SEARCHES REACHED. STOPPING.")
            return {"messages": [AIMessage(content="I have searched the document multiple times but cannot find more specific data. Based on what I found...")]}

        print(f"\n--- [AGENT] THINKING (Attempt {count + 1}) ---")
        
        # Re-initialize tools to ensure proper context
        tools = self.get_tools()
        model_with_tools = self.llm.bind_tools(tools)

        sys_msg = SystemMessage(content=(
            "You are a strict financial auditor. Your goal is to find exact data. "
            "1. Use the search_pdf tool to find information. "
            "2. If the search results are empty or irrelevant, REWRITE your query and try again. "
            "3. Once you have the data, provide a final answer with page references."
        ))

        # The LLM looks at the history and decides: "Should I call a tool or answer?"
        response = model_with_tools.invoke([sys_msg] + state["messages"])

        if not response.tool_calls and '{"name":' in response.content:
            try:
                # Try to extract and parse the JSON from the text
                tool_data = json.loads(response.content)
                # Manually inject it into tool_calls so the graph continues
                response.tool_calls = [{
                    "name": tool_data["name"],
                    "args": tool_data["arguments"],
                    "id": "manual_call_" + os.urandom(4).hex() # Give it a random ID
                }]
                print(f"🛠️  [REPAIRED TOOL CALL]: {response.tool_calls[0]['name']}")
            except:
                print(f"💬 [RAW RESPONSE]: {response.content}")
    
        elif response.tool_calls:
            print(f"🛠️  [NATIVE TOOL CALL]: {response.tool_calls[0]['name']}")
        else:
            print(f"✅ [FINAL ANSWER GENERATED]")
        
        return {"messages": [response]}
    
    def generate_final_answer(self, state: FinLensState):
        """Optional: A dedicated node to clean up the final answer if needed."""
        print("--- GENERATING FINAL AUDIT REPORT ---")
        return {"messages": [AIMessage(content=state["messages"][-1].content)]}
         
        

