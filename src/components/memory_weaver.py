import networkx as nx
from networkx.readwrite import json_graph
import json
import os
from src.core.memory_node import MemoryNode

class MemoryWeaver:
    """
    Manages the knowledge graph, weaving new memories into it.
    The graph connects the user to entities via relationships.
    """
    def __init__(self, user_id: str = "user_main", graph_path: str = "data/memory_graph.json"):
        """
        Initializes the MemoryWeaver.

        Args:
            user_id (str): A unique identifier for the current user.
            graph_path (str): The file path to store the knowledge graph.
        """
        self.user_id = user_id
        self.graph_path = graph_path
        self.graph = self._load_graph()
        self._ensure_user_node()

    def _load_graph(self) -> nx.Graph:
        """Loads the knowledge graph from a file, or creates a new one."""
        if os.path.exists(self.graph_path):
            try:
                with open(self.graph_path, 'r') as f:
                    data = json.load(f)
                    return json_graph.node_link_graph(data)
            except (json.JSONDecodeError, nx.NetworkXError) as e:
                print(f"Could not load or parse graph file, creating a new one. Error: {e}")
                return nx.Graph()
        return nx.Graph()

    def _save_graph(self):
        """Saves the current knowledge graph to a file."""
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.graph_path), exist_ok=True)
        
        data = json_graph.node_link_data(self.graph)
        with open(self.graph_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _ensure_user_node(self):
        """Ensures the central user node exists in the graph."""
        if not self.graph.has_node(self.user_id):
            self.graph.add_node(self.user_id, type="user", label="User")
            print(f"User node '{self.user_id}' created in the knowledge graph.")

    def weave_memory(self, node: MemoryNode):
        """
        Adds a MemoryNode's information to the knowledge graph.

        This method connects the user node to entity nodes based on the
        information in the memory node.
        """
        content = node.get("content", {})
        entities = content.get("entities", [])
        relationship = content.get("relationship", "related_to")
        
        for entity in entities:
            # Add the entity as a node if it doesn't exist
            if not self.graph.has_node(entity):
                self.graph.add_node(entity, type=node.get("category"), label=entity)

            # Add an edge (a relationship) between the user and the entity
            self.graph.add_edge(
                self.user_id,
                entity,
                relationship=relationship,
                sentiment=content.get("sentiment"),
                source_text=node.get("source_text"),
                timestamp=node.get("timestamp")
            )
        
        print(f"Wove memory '{node['source_text']}' into the graph.")
        self._save_graph()

    def get_graph_info(self) -> dict:
        """Returns basic information about the current graph."""
        return {
            "nodes": list(self.graph.nodes()),
            "edges": list(self.graph.edges(data=True)) # data=True includes attributes
        }
