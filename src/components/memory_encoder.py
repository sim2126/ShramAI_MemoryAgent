import uuid
from datetime import datetime
from src.services.openai_service import get_structured_completion
from src.core.memory_node import MemoryNode, MemoryNodeContent

class MemoryEncoder:
    """
    This component is responsible for taking raw text and converting it
    into a structured MemoryNode using a large language model.
    """

    def _create_encoder_prompt(self, text: str) -> str:
        """Creates the specific prompt for the LLM to encode the memory."""
        # This prompt is the "secret sauce". It instructs the LLM on how to
        # analyze the text and what structure to return.
        prompt = f"""
        Analyze the following user statement to extract a memory.
        Your output must be a single JSON object.

        User statement: "{text}"

        From this statement, extract the following information:
        1. "type": Classify the memory. Is it a "Preference" (like/dislike), a "Fact" (a statement of fact), an "Objective" (a goal), or a "PersonalDetail"?
        2. "category": What is the general topic? Examples: "Software", "Food", "Work", "LifeGoal", "Hobby".
        3. "content": This must be a JSON object with three keys:
           - "entities": A list of key nouns or subjects.
           - "relationship": How the user relates to the entities (e.g., "uses", "likes", "is", "wants_to_learn").
           - "sentiment": The user's sentiment. "positive", "negative", or "neutral".
        
        Example:
        User statement: "I love using VS Code for Python development."
        Your JSON output:
        {{
            "type": "Preference",
            "category": "Software",
            "content": {{
                "entities": ["VS Code", "Python"],
                "relationship": "uses_for",
                "sentiment": "positive"
            }}
        }}

        Now, analyze the user statement provided at the top and generate the JSON object.
        """
        return prompt

    def encode(self, text: str) -> MemoryNode | None:
        """
        Encodes a raw text string into a structured MemoryNode.

        Args:
            text (str): The raw text from the user.

        Returns:
            MemoryNode | None: A structured MemoryNode if encoding is successful, otherwise None.
        """
        prompt = self._create_encoder_prompt(text)
        encoded_data = get_structured_completion(prompt)

        if not encoded_data:
            print("Failed to get a structured response from the LLM.")
            return None

        try:
            # We construct the full MemoryNode object with the data from the LLM
            # and add our own metadata (id, timestamp, etc.).
            content_data = encoded_data.get("content", {})
            
            memory_node: MemoryNode = {
                "memory_id": f"m_{uuid.uuid4()}",
                "timestamp": datetime.now().isoformat(),
                "source_text": text,
                "type": encoded_data.get("type", "Unknown"),
                "category": encoded_data.get("category", "Unknown"),
                "content": {
                    "entities": content_data.get("entities", []),
                    "relationship": content_data.get("relationship", "unknown"),
                    "sentiment": content_data.get("sentiment", "neutral")
                }
            }
            return memory_node
        except (KeyError, TypeError) as e:
            print(f"Error constructing MemoryNode from LLM response: {e}")
            print(f"Received data: {encoded_data}")
            return None
