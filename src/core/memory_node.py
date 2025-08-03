from typing import TypedDict, List, Dict, Any

class MemoryNodeContent(TypedDict):
    """Defines the structure for the 'content' part of a MemoryNode."""
    entities: List[str]
    relationship: str
    sentiment: str

class MemoryNode(TypedDict):
    """
    Defines the structured representation of a single memory.
    This structure is created by the MemoryEncoder.
    """
    memory_id: str
    type: str  # e.g., "Preference", "Fact", "Insight"
    category: str # e.g., "Software", "Personal", "Work"
    content: MemoryNodeContent
    timestamp: str
    source_text: str
