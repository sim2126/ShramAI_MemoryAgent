from src.components.memory_encoder import MemoryEncoder
from src.components.memory_weaver import MemoryWeaver
import json

def run_demo():
    """Runs a demonstration of the full encoding and weaving pipeline."""
    print("--- ShramAI Memory Agent: Weaver Demo ---")

    # --- Memory 1 ---
    user_statement_1 = "I use Shram and Magnet as productivity tools."
    print(f"\n[Input 1] User statement: '{user_statement_1}'")

    # Initialize our components
    encoder = MemoryEncoder()
    weaver = MemoryWeaver() # This will load the existing graph or create a new one

    # Encode the first statement
    print("\n[Step 1a] Encoding statement into a structured MemoryNode...")
    memory_node_1 = encoder.encode(user_statement_1)

    if memory_node_1:
        # Weave the memory into the graph
        print("\n[Step 1b] Weaving MemoryNode into the Knowledge Graph...")
        weaver.weave_memory(memory_node_1)
    else:
        print("Failed to create MemoryNode 1.")

    # --- Memory 2 ---
    user_statement_2 = "My favorite color is blue."
    print(f"\n[Input 2] User statement: '{user_statement_2}'")

    # Encode the second statement
    print("\n[Step 2a] Encoding statement into a structured MemoryNode...")
    memory_node_2 = encoder.encode(user_statement_2)
    
    if memory_node_2:
        # Weave the second memory into the same graph
        print("\n[Step 2b] Weaving MemoryNode into the Knowledge Graph...")
        weaver.weave_memory(memory_node_2)
    else:
        print("Failed to create MemoryNode 2.")

    # --- Display Graph Info ---
    print("\n--- Final Knowledge Graph State ---")
    graph_info = weaver.get_graph_info()
    print(json.dumps(graph_info, indent=2))
    print("\nGraph data saved to 'data/memory_graph.json'")


if __name__ == "__main__":
    run_demo()
