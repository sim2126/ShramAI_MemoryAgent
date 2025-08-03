import uuid
from datetime import datetime
from src.services.openai_service import get_structured_completion
from src.core.memory_node import MemoryNode

class MemoryEncoder:
    """
    This component is responsible for taking raw text and converting it
    into a structured MemoryNode using a large language model.
    """

    def _create_encoder_prompt(self, text: str) -> str:
        """Creates the specific prompt for the LLM to encode the memory."""
        prompt = f"""
        Analyze the following user statement to extract a memory.
        Your output must be a single JSON object.

        User statement: "{text}"

        From this statement, extract the following information:
        1. "type": Classify the memory. Is it a "Preference", a "Fact", an "Objective", or a "PersonalDetail"?
        2. "category": What is the general topic? Examples: "Software", "Food", "Work", "LifeGoal", "Hobby".
        3. "subcategory": A more specific category if available. Examples: "Productivity Tool", "Programming Language", "Restaurant". If not applicable, use an empty string.
        4. "content": This must be a JSON object with three keys:
           - "entities": A list of key nouns or subjects.
           - "relationship": How the user relates to the entities (e.g., "uses", "likes", "is", "wants_to_learn").
           - "sentiment": The user's sentiment. "positive", "negative", or "neutral".
        
        Example:
        User statement: "I use Shram and Magnet as productivity tools."
        Your JSON output:
        {{
            "type": "Fact",
            "category": "Software",
            "subcategory": "Productivity Tool",
            "content": {{
                "entities": ["Shram", "Magnet"],
                "relationship": "uses",
                "sentiment": "neutral"
            }}
        }}

        Now, analyze the user statement provided at the top and generate the JSON object.
        """
        return prompt

    def encode(self, text: str) -> MemoryNode | None:
        """
        Encodes a raw text string into a structured MemoryNode.
        """
        prompt = self._create_encoder_prompt(text)
        encoded_data = get_structured_completion(prompt)

        if not encoded_data:
            print("Failed to get a structured response from the LLM.")
            return None

        try:
            content_data = encoded_data.get("content", {})
            
            memory_node: MemoryNode = {
                "memory_id": f"m_{uuid.uuid4()}",
                "timestamp": datetime.now().isoformat(),
                "source_text": text,
                "type": encoded_data.get("type", "Unknown"),
                "category": encoded_data.get("category", "Unknown"),
                "subcategory": encoded_data.get("subcategory", ""), # Add the new field
                "content": {
                    "entities": content_data.get("entities", []),
                    "relationship": content_data.get("relationship", "unknown"),
                    "sentiment": content_data.get("sentiment", "neutral")
                }
            }
            return memory_node
        except (KeyError, TypeError) as e:
            print(f"Error constructing MemoryNode from LLM response: {e}")
            return None
