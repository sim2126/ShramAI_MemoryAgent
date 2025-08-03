import networkx as nx
from src.components.memory_weaver import MemoryWeaver

class MemoryRetriever:
    """
    Retrieves relevant memories from the knowledge graph based on a query.
    """
    def __init__(self, weaver: MemoryWeaver):
        """
        Initializes the MemoryRetriever.

        Args:
            weaver (MemoryWeaver): An instance of MemoryWeaver containing the graph.
        """
        self.graph = weaver.graph
        self.user_id = weaver.user_id

    def retrieve(self, query: str) -> list[str]:
        """
        Retrieves memories contextually relevant to the query.

        This more robust method checks for matches in the query against:
        1. The name of a connected entity.
        2. The category of a connected entity.
        3. The original source text of the memory itself.

        Args:
            query (str): The user's query or topic of interest.

        Returns:
            list[str]: A list of source texts from relevant memories.
        """
        query_words = set(word.strip(".,?!") for word in query.lower().split())
        retrieved_memories = set()

        # We iterate through all edges connected to the user, as edges represent memories.
        for u, v, data in self.graph.edges(self.user_id, data=True):
            # u is the user_id, v is the entity node (e.g., "Shram")
            entity_node = self.graph.nodes[v]
            
            # 1. Check the entity's name
            if v.lower() in query_words:
                retrieved_memories.add(data['source_text'])
                continue # Move to the next memory to avoid duplicates

            # 2. Check the entity's category (type)
            entity_type = entity_node.get('type', '').lower()
            if entity_type and entity_type in query_words:
                retrieved_memories.add(data['source_text'])
                continue

            # 3. Check the original source text of the memory
            source_text_words = set(word.strip(".,?!") for word in data.get('source_text', '').lower().split())
            if query_words.intersection(source_text_words):
                retrieved_memories.add(data['source_text'])
        
        return list(retrieved_memories)
