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
        Retrieves memories by checking the query against the entity's name,
        category, and specific subcategory for a much more accurate search.
        """
        stop_words = {
            'a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 
            'how', 'i', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this', 
            'to', 'was', 'what', 'when', 'where', 'who', 'will', 'with', 'the', 
            'my', 'do', 'you', 'know', 'am'
        }
        query_words = {word.strip(".,?!") for word in query.lower().split()} - stop_words
        relevant_memories = set()

        # Iterate through all memories (edges) connected to the user
        for u, v, edge_data in self.graph.edges(self.user_id, data=True):
            entity_node_data = self.graph.nodes[v]
            
            # Check 1: Entity Name
            if v.lower() in query_words:
                relevant_memories.add(edge_data['source_text'])
                continue

            # Check 2: General Category
            entity_type = entity_node_data.get('type', '').lower()
            if entity_type and entity_type in query_words:
                relevant_memories.add(edge_data['source_text'])
                continue
            
            # Check 3: Specific Subcategory (This is the key fix)
            node_subcategory = entity_node_data.get('subcategory', '').lower()
            if node_subcategory:
                # We split the subcategory in case it has multiple words like "Productivity Tool"
                subcategory_words = set(node_subcategory.split())
                # isdisjoint() is a fast way to check for any common items between two sets
                if not query_words.isdisjoint(subcategory_words):
                    relevant_memories.add(edge_data['source_text'])
                    continue

        return list(relevant_memories)
