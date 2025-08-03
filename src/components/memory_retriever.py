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

        This method finds nodes in the graph that match keywords in the query,
        then gathers all connected memories from the user to those nodes.

        Args:
            query (str): The user's query or topic of interest.

        Returns:
            list[str]: A list of source texts from relevant memories.
        """
        query_words = set(query.lower().split())
        relevant_nodes = set()

        # Find all nodes in the graph that match words in the query
        for node in self.graph.nodes():
            if node != self.user_id and node.lower() in query_words:
                relevant_nodes.add(node)
        
        if not relevant_nodes:
            return []

        # Gather all unique memories (source_text) connected to these nodes
        retrieved_memories = set()
        for node in relevant_nodes:
            if self.graph.has_edge(self.user_id, node):
                # The edge data contains the original memory information
                edge_data = self.graph.get_edge_data(self.user_id, node)
                if edge_data and 'source_text' in edge_data:
                    retrieved_memories.add(edge_data['source_text'])

        return list(retrieved_memories)
