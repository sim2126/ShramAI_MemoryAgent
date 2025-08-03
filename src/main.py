from src.components.memory_encoder import MemoryEncoder
from src.components.memory_weaver import MemoryWeaver
from src.components.memory_retriever import MemoryRetriever
from src.components.memory_synthesizer import MemorySynthesizer
import json

def run_demo():
    """Runs a full demonstration of all agent components."""
    print("--- ShramAI Memory Agent: Full Demo ---")

    # --- Setup ---
    # Initialize all our components. The weaver holds the graph state.
    weaver = MemoryWeaver()
    encoder = MemoryEncoder()
    retriever = MemoryRetriever(weaver)
    synthesizer = MemorySynthesizer(weaver)

    # --- Ingestion Phase ---
    # We add a few memories to the graph.
    statements = [
        "I use Shram and Magnet as productivity tools.",
        "My favorite color is blue.",
        "I am a project manager at a tech company."
    ]

    for stmt in statements:
        print(f"\nProcessing statement: '{stmt}'")
        node = encoder.encode(stmt)
        if node:
            weaver.weave_memory(node)

    print("\n--- Ingestion Complete. Current Graph State ---")
    graph_info = weaver.get_graph_info()
    print(json.dumps(graph_info, indent=2))

    # --- Synthesis Phase ---
    # The agent "thinks" and creates new knowledge.
    synthesizer.synthesize()

    # --- Retrieval Phase ---
    # Now, the user asks a question.
    user_query = "What do you know about my productivity tools?"
    print(f"\n--- User Query: '{user_query}' ---")

    # Retrieve relevant memories using the graph.
    relevant_memories = retriever.retrieve(user_query)

    print("\n[1] Retrieved relevant memories:")
    if relevant_memories:
        for mem in relevant_memories:
            print(f"- {mem}")
        
        # This context would then be passed to an LLM to generate a final answer.
        context = ". ".join(relevant_memories)
        final_prompt = f"Based on this context: '{context}'. Answer the user's question: '{user_query}'"
        print("\n[2] This is the final context-rich prompt we would send to the LLM:")
        print(final_prompt)
    else:
        print("No relevant memories found for the query.")


if __name__ == "__main__":
    run_demo()
