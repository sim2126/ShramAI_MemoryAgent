# ShramAI Cognitive Memory Agent

This project is a sophisticated, proof-of-concept memory system designed to give Large Language Models (LLMs) like GPT or Gemini a form of long-term, structured memory. It goes beyond simple chat history by creating an intelligent, evolving knowledge base for each user.

## The Problem: LLMs are Forgetful

Standard LLMs are stateless. They have no memory of past conversations. While you can feed chat history back into the prompt, this approach is inefficient, lacks contextual understanding, and quickly hits token limits. The model doesn't *understand* the user's history, it just reads it.

## Our Solution: The Cognitive Memory Architecture

We designed a more intelligent solution that mimics aspects of human cognition. Instead of storing a flat list of sentences, our agent transforms conversations into a dynamic **knowledge graph**. This allows the agent not just to recall facts, but to understand relationships, infer context, and even generate new insights on its own.

### Core Components

The agent is built on four key components that work in a pipeline:

**1. The Memory Encoder**

* **Purpose:** To transform raw, unstructured user text into a structured `MemoryNode`.
* **How it Works:** It uses a call to the Google Gemini API with a carefully crafted prompt, instructing the LLM to analyze the user's statement and extract key information: the type of memory (e.g., a Preference, a Fact), a general `category`, a specific `subcategory`, and the core `content` (entities, relationship, sentiment).

**2. The Memory Weaver**

* **Purpose:** To build and manage the user's "brain" or knowledge graph.
* **How it Works:** Using the `networkx` library, this component takes the structured `MemoryNode` from the Encoder and "weaves" it into a `MultiGraph`. It creates nodes for entities (like "Shram" or "blue") and connects them to the central user node with edges that represent the relationship (e.g., "uses," "likes"). Using a `MultiGraph` is a key decision, as it allows the agent to store multiple, parallel memories about the same entity.

**3. The Memory Synthesizer**

* **Purpose:** To allow the agent to "think" and form new conclusions.
* **How it Works:** This component runs in the background, scanning the knowledge graph for patterns. For example, if it finds multiple entities belonging to the same category (like two "Software" nodes), it uses another LLM call to generate a new, higher-level "Insight" memory. This insight is then woven back into the graph, enriching the agent's understanding.

**4. The Memory Retriever**

* **Purpose:** To intelligently search the knowledge graph based on a user's query.
* **How it Works:** This is far more advanced than keyword search. The retriever parses the user's query, filters out common "stop words," and then searches the graph for matches against an entity's name, its general category, and its specific subcategory. This allows it to find contextually relevant information even if the query doesn't use the exact same words as the original memory.

### Demonstration: A Walkthrough

To see the agent in action, we run the `main.py` script. Here is a breakdown of the final output, demonstrating the full pipeline.

**1. Ingestion:**
The agent processes three user statements:

* `"I use Shram and Magnet as productivity tools."`
* `"My favorite color is blue."`
* `"I am a project manager at a tech company."`

The **Encoder** and **Weaver** work together to build the following knowledge graph:

```json
{
  "nodes": [
    ["user_main", {"type": "user", "label": "User"}],
    ["Shram", {"type": "Software", "subcategory": "Productivity Tool", "label": "Shram"}],
    ["Magnet", {"type": "Software", "subcategory": "Productivity Tool", "label": "Magnet"}],
    ["blue", {"type": "PersonalDetail", "subcategory": "", "label": "blue"}],
    ["project manager", {"type": "Work", "subcategory": "JobTitle", "label": "project manager"}],
    ["tech company", {"type": "Work", "subcategory": "JobTitle", "label": "tech company"}]
  ],
  "edges": [
    ["user_main", "Shram", {"relationship": "uses", "source_text": "..."}],
    ["user_main", "Magnet", {"relationship": "uses", "source_text": "..."}],
    ["user_main", "blue", {"relationship": "likes", "source_text": "..."}],
    ["user_main", "project manager", {"relationship": "is", "source_text": "..."}],
    ["user_main", "tech company", {"relationship": "is", "source_text": "..."}]
  ]
}
```

**2. Synthesis:**
The **Synthesizer** runs, detects a pattern (multiple nodes in the "Software" category), and generates a new insight:

> "Generated Insight: The user is involved with both Shram and Magnet software."

This new insight is then woven back into the graph as a new memory.

**3. Retrieval:**
Finally, the user asks a query: `"What do you know about my productivity tools?"`
The **Retriever** correctly finds the relevant memories by matching the query words "productivity" and "tools" to the `subcategory` of the "Shram" and "Magnet" nodes.

The final retrieved context is:

```
- I use Shram and Magnet as productivity tools.
- The user is involved with both Shram and Magnet software.
```

This rich, relevant context can then be passed to an LLM to generate a highly accurate and informed final answer for the user.

### Technical Stack

* **Language:** Python 3
* **Core Logic:**
    * **LLM Interaction:** `google-generativeai` (for the Gemini API)
    * **Knowledge Graph:** `networkx`
* **Configuration:** `python-dotenv`

### How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/sim2126/ShramAI_MemoryAgent.git](https://github.com/sim2126/ShramAI_MemoryAgent.git)
    cd ShramAI_MemoryAgent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key:**
    * Create a file named `.env` in the root of the project.
    * Get a free API key from [Google AI Studio](https://aistudio.google.com/).
    * Add your key to the `.env` file:
        ```
        GEMINI_API_KEY=your_api_key_here
        ```

4.  **Run the demo:**
    ```bash
    python -m src.main
    ```
