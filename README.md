# LangGraph Learning Project

This repository is a project to learn and explore the features of the `langgraph` library. It demonstrates how to use `langgraph` to design and manage the flow of tasks in your application using a graph structure.

## Types Used in LangGraph

LangGraph relies heavily on Python's type annotations to define states and edges. Below are some commonly used types and how they can be utilized:

### `Dict` and `TypedDict`
- `Dict` is a generic mapping type, but `TypedDict` is preferred for defining structured states in LangGraph.

Example:
```python
from typing import TypedDict

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str
```

### `Union`
- Use `Union` to allow multiple types for a state field.

Example:
```python
from typing import Union

class AgentState(TypedDict):
    data: Union[int, str]
```

### `Optional`
- Use `Optional` for fields that may or may not be present.

Example:
```python
from typing import Optional

class AgentState(TypedDict):
    optional_field: Optional[str]
```

### `Any`
- Use `Any` for fields where the type is not known or can vary.

Example:
```python
from typing import Any

class AgentState(TypedDict):
    dynamic_field: Any
```

### Lambda Functions
- Lambda functions can be used in conditional edges to define transitions based on state values.

Example:
```python
graph.add_conditional_edge("node1", "node2", lambda state: state["value"] > 10)
```

## Components of LangGraph

LangGraph consists of several components that work together to define and execute workflows:

### State
- A shared data structure that keeps track of information as the application runs.

Example:
```python
class AgentState(TypedDict):
    message: str
```

### Nodes
- Functions that process or transform the state.

Example:
```python
def greeting_node(state: AgentState) -> AgentState:
    state["message"] = "Hello " + state["message"]
    return state
```

### Graph
- A collection of nodes and edges that define the workflow.

### Edges
- Connections between nodes that define the flow of execution.

### Conditional Edges
- Edges that are executed based on a condition.

Example:
```python
graph.add_conditional_edge("node1", "node2", lambda state: state["value"] > 10)
```

### Tools and Tool Nodes
- External tools or APIs that can be integrated into the graph.

### StateGraph
- The main class used to define and compile the graph.

### Runnables
- Compiled graphs that can be executed with an initial state.

## Messages in LangGraph

LangGraph supports different types of messages for communication:

### `HumanMessage`
- Represents a message from a human user.

### `SystemMessage`
- Represents a system-level message.

### `FunctionMessage`
- Represents a message from a function.

### `AIMessage`
- Represents a message from an AI model.

### `ToolMessage`
- Represents a message from an external tool.

Example:
```python
from langgraph.messages import HumanMessage, AIMessage

human_msg = HumanMessage(content="Hello!")
ai_msg = AIMessage(content="Hi there!")
```

## Setting Up the Environment

### 1. Creating a Virtual Environment
Run the following command to create a virtual environment:
```sh
python -m venv venv
```

### 2. Activating the Virtual Environment
- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### 3. Installing Dependencies
Install the required dependencies from `requirements.txt`:
```sh
pip install -r requirements.txt
```

## Running Examples

### 1. Running the `Hello_world` Example
run:
```sh
python 01_hello_world/main.py
```

### 2. Running the `Multi Input` Example
run:
```sh
python 02_multiple_input_graph/main.py
```

### 3. Running the `Sequential Graph` Example
run:
```sh
python 03_sequential_graph/main.py
```

### 4. Running the `Conditional Graph` Example
run:
```sh
python 04_conditional_graph/main.py
```

### 5. Running the `Looping Graph` Example
run:
```sh
python 05_looping_graph/main.py
```

### 6. Running the `06_simple_bot` Example
run:
```sh
python 06_simple_bot/main.py
```

### 7. Running the `07_memory_agent` Example
run:
```sh
python 07_memory_agent/main.py
```

### 8. Running the `08_react_agent` Example
run:
```sh
python 08_react_agent/main.py
```

### 9. Running the `09_drafter_agent` Example
run:
```sh
python 09_drafter_agent/main.py
```

### 10. Running the `10_RAG` Example
run:
```sh
python 10_RAG/main.py
```

### 11. Running the `11_langgraph_simple_bot` Example
run:
```sh
python 11_langgraph_simple_bot/main.py
```

### 12. Running the `12_agentic_serach` Example
run:
```sh
python 12_agentic_serach/main.py
```

### 13. Running the `13_research_agent` Example
run:
```sh
python 13_research_agent/main.py
```

## Contributions

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```sh
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```sh
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```sh
   git push origin feature-name
   ```
5. Open a pull request.

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

```
MIT License

Copyright (c) [Year] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining