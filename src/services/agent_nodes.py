from langchain_core.messages import AIMessage


from src.services.agent_state import FinLensState
from src.components.RagPdf import RagPipeline

class AgentNodes:
    def __init__(self, rag_pipeline: RagPipeline):
        self.rag_pipeline = rag_pipeline

    def retrieve_node(self,state:FinLensState):
        ## Worker 1
        current_attempt = state.get("query_count", 0) + 1
        print(f"\n--- [ATTEMPT {current_attempt}] RETRIEVING FROM CHROMADB ---")

        user_query = state["messages"][-1].content

        ## Fetching the 5 chunks
        retrieved_chunks = self.rag_pipeline._search(user_query)

        if retrieved_chunks:
            print(f"✅ Found {len(retrieved_chunks)} chunks. Preview: {retrieved_chunks[0]['text'][:100]}...")
        else:
            print("⚠️ No chunks found in Vector Store.")

        return{
            "documents": retrieved_chunks,
            "query_Count": state.get("query_count",0) + 1
        }
    
    def grade_node(self, state: FinLensState):

            # Worker 2: The Grader (The Decision Engine)

            print("---CHECKING DOCUMENT RELEVANCE---")
        
            question = state["messages"][-1].content
            docs = state["documents"]

            if not docs:
                print("❌ No docs to grade. Marking as 'no'.")
                return {"is_relevant": "no"}
        
            # 1. Prepare the grading prompt
            prompt = f"""
            You are a grader assessing relevance of a retrieved document to a user question. 
        
            Retrieved Documents: 
            {docs}
        
            User Question: 
            {question}
        
            If the document contains keywords or semantic meaning related to the user question, grade it as relevant. 
            Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.
        
            Respond ONLY with a JSON object: {{"score": "yes"}} or {{"score": "no"}}
            """

            # 2. Call Gemini for the decision
            response = self.rag_pipeline.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )

            # 3. Parse the result safely
            import json
            try:
                # Clean the string in case Gemini adds markdown ```json blocks
                clean_content = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_content)
                grade = data.get("score", "no")
                print(f"⚖️ Grade Result: {grade.upper()}")
            except:
                grade = "no" # Default to 'no' if the LLM output is messy
                print("⚖️ Grade Result: ERROR PARSING (Defaulting to NO)")

            # 4. Update the 'Shared Notebook'
            # We write our decision into the 'is_relevant' field.
            return {"is_relevant": grade}
    

    def generate_node(self, state: FinLensState):
            """
            Worker 3: The Generator
            """
            print("---GENERATING FINAL ANSWER---")

            if state.get("is_relevant") == "no":
                not_found_msg = "I'm sorry, I searched the document but couldn't find relevant information to answer your question accurately."
                print("🛑 Result: Not Found in document.")
                return {"messages": [AIMessage(content=not_found_msg)]}
        
            # 1. Get data from the notebook
            question = state["messages"][-1].content
            docs = state["documents"]
        
            # 2. I am using existing _build_context logic to format the chunks
            context = self.rag_pipeline._build_context(docs)
        
            prompt = f"""
            You are a financial document assistant.
            Answer the question ONLY using the provided context.
            Do NOT use outside knowledge.
            Always include page references like (Page X).

            Context:
            {context}

            Question:
            {question}
        
            Answer:
            """

            # 3. Final generation
            response = self.rag_pipeline.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            # 4. Update the Notebook
            # We return the AI's response as a 'message'. 
            # Because we used 'add_messages' in the State, this appends to the history.
            print("✨ Answer generated successfully.")
            return {"messages": [AIMessage(content=response.text)]}
        
    def rewrite_node(self, state: FinLensState):
        print("--- [REWRITER] OPTIMIZING QUERY FOR BETTER RETRIEVAL ---")
        question = state["messages"][-1].content
    
        prompt = f"Optimize this financial query for a vector database search. Provide ONLY the search string: {question}"
        response = self.rag_pipeline.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

        print(f"Generated Query is: {response.text}")
    
        return {"messages": [AIMessage(content=response.text)]}