import uuid
from datetime import datetime
from src.components.memory_weaver import MemoryWeaver
from src.services.openai_service import get_structured_completion
from src.core.memory_node import MemoryNode

class MemorySynthesizer:
    """
    Analyzes the knowledge graph to find patterns and create new,
    higher-level 'Insight' memories.
    """
    def __init__(self, weaver: MemoryWeaver):
        """
        Initializes the MemorySynthesizer.

        Args:
            weaver (MemoryWeaver): An instance of MemoryWeaver containing the graph.
        """
        self.weaver = weaver
        self.graph = weaver.graph

    def _create_synthesis_prompt(self, facts: list[str]) -> str:
        """Creates the prompt for the LLM to synthesize an insight."""
        fact_list = "\n- ".join(facts)
        prompt = f"""
        Analyze the following facts about a user and generate a single, concise insight.
        The insight should be a logical conclusion drawn from the combination of these facts.
        Your output must be a single JSON object with one key: "insight".

        Facts:
        - {fact_list}

        Example:
        Facts:
        - User uses 'VS Code' for 'Python'.
        - User's job is 'Software Developer'.
        Your JSON output:
        {{
            "insight": "The user is a software developer who likely uses VS Code as their primary editor for Python development."
        }}

        Now, analyze the facts provided at the top and generate the JSON object.
        """
        return prompt

    def synthesize(self) -> MemoryNode | None:
        """
        Runs the synthesis process to find patterns and generate insights.
        
        This is a simple example that looks for multiple entities of the same category.
        A real-world version would have more complex pattern detection logic.
        """
        print("\nSynthesizing insights from the knowledge graph...")
        
        # Simple pattern: Find if the user has multiple tools in the same category
        nodes_by_category = {}
        for node, data in self.graph.nodes(data=True):
            if data.get('type') and data['type'] != 'user':
                category = data['type']
                if category not in nodes_by_category:
                    nodes_by_category[category] = []
                nodes_by_category[category].append(node)

        for category, entities in nodes_by_category.items():
            if len(entities) > 1:
                print(f"Found a pattern: User has multiple entities in the '{category}' category: {entities}")
                
                # We found a pattern, now let's create an insight
                facts = [f"User is associated with '{entity}' ({category})" for entity in entities]
                prompt = self._create_synthesis_prompt(facts)
                
                response = get_structured_completion(prompt)
                insight_text = response.get("insight")

                if insight_text:
                    # Create a new 'Insight' MemoryNode
                    insight_node: MemoryNode = {
                        "memory_id": f"m_insight_{uuid.uuid4()}",
                        "timestamp": datetime.now().isoformat(),
                        "source_text": insight_text,
                        "type": "Insight",
                        "category": category,
                        "content": {
                            "entities": entities,
                            "relationship": "has_pattern",
                            "sentiment": "neutral"
                        }
                    }
                    print(f"Generated Insight: {insight_text}")
                    # We can even weave this new insight back into the graph
                    self.weaver.weave_memory(insight_node)
                    return insight_node
        
        print("No new insights were generated.")
        return None
