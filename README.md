# Agentic AI Platform

An intelligent, multi-use case chatbot application built with **LangGraph** and **Streamlit**, featuring modular LLM support and agentic workflows for conversational AI and content generation.

## Overview

This project demonstrates end-to-end agentic AI capabilities using LangGraph's state graph architecture. It supports multiple use cases through different workflow configurations, allowing users to interact with various LLM providers through an intuitive web interface.

## Features

### Supported Use Cases

1. **Basic Chatbot**
   - Simple conversational AI interface
   - Maintains conversation history with thread-based memory
   - Multi-turn dialogue support

2. **News Content Writer**
   - Intent-based routing to validate content writing queries
   - Generates professional news articles following journalism principles (5W1H)
   - Supports multiple input modes:
     - Text description only
     - URL reference with description
     - Multiple URL references
   - Web scraping for reference article content
   - Ensures accuracy, respectful tone, and proper structure

### LLM Provider Support

- **OpenAI** (GPT models)
- **Groq** (High-speed inference)
- **Ollama** (Local models)

All providers support temperature control and model selection through the UI.

## Architecture

### Project Structure

```
Agentic-AI-Platform/
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── src/
│   └── langgraphagenticai/
│       ├── main.py                 # Main application logic
│       ├── LLMs/
│       │   └── loadllms.py        # LLM provider factory
│       ├── graph/
│       │   └── graph_builder.py   # LangGraph workflow builder
│       ├── nodes/
│       │   ├── chatbot_nodes.py   # Chatbot workflow nodes
│       │   └── news_writer_nodes.py # News writer workflow nodes
│       ├── state/
│       │   └── graph_state.py     # Graph state definitions
│       ├── models/
│       │   ├── intent_result.py   # Intent classification model
│       │   └── ArticleEvaluationResult.py # Article evaluation model
│       ├── memory/
│       │   └── chat_history.py    # Conversation memory management
│       ├── tools/
│       │   └── news_articles.py   # News article tools
│       ├── ui/
│       │   └── streamlitui/       # Streamlit UI components
│       └── commonconstants/
│           └── constants.py       # Application constants
```

### Workflow Architecture

#### Basic Chatbot Workflow
```
START → chatbot → END
```

#### News Content Writer Workflow
```
START → intent_checker → [conditional routing]
                         ├─ generate → END (valid request)
                         └─ END (invalid request)
```

### Key Components

- **GraphBuilder**: Orchestrates LangGraph state machines for different use cases
- **State Management**: TypedDict-based state with message annotations
- **Memory**: Thread-based conversation history using LangGraph's MemorySaver
- **Nodes**: Modular, reusable graph nodes for different operations
- **Structured Output**: Uses Pydantic models for LLM response validation

## Installation

### Prerequisites

- Python 3.10+
- pip or conda package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Agentic-AI-Platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys** (if using OpenAI or Groq)
   - You'll provide API keys through the Streamlit UI
   - Alternatively, set environment variables:
     ```bash
     export OPENAI_API_KEY="your-key-here"
     export GROQ_API_KEY="your-key-here"
     ```

4. **For Ollama (local models)**
   ```bash
   # Install Ollama from https://ollama.ai
   # Pull desired model
   ollama pull llama2
   ```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Interface

1. **Select Use Case**: Choose between "Basic Chatbot" or "News Content Writer"
2. **Select LLM Provider**: Choose OpenAI, Groq, or Ollama
3. **Configure Model**: Select the specific model you want to use
4. **Enter API Key**: Required for OpenAI and Groq (not needed for Ollama)
5. **Start Chatting**: Type your message in the chat input

### Features in Action

**Basic Chatbot**:
- Ask any question or have a conversation
- History is maintained within the session
- Click "Reset Conversation" to start fresh

**News Content Writer**:
- Request: "Write an article about AI advancements"
- With URL: "Write an article about https://example.com/ai-news based on this source"
- The system will validate your intent and generate professional content

### Thread Management

Each conversation session has a unique thread ID displayed in the sidebar. Use the "Reset Conversation" button to clear history and start a new thread.

## Dependencies

Core libraries:
- `langchain` - LangChain framework
- `langgraph ~=0.5.4` - Graph-based agent orchestration
- `streamlit ~=1.47.1` - Web UI framework
- `langchain_openai ~=0.3.28` - OpenAI integration
- `langchain_groq` - Groq integration
- `langchain_community ~=0.3.27` - Community integrations (Ollama)
- `pydantic ~=2.11.7` - Data validation
- `beautifulsoup4 ~=4.13.4` - Web scraping
- `requests ~=2.32.4` - HTTP requests

See `requirements.txt` for complete list.

## Configuration

### Adding New Use Cases

1. Create a new node class in `src/langgraphagenticai/nodes/`
2. Define the workflow in `graph_builder.py`
3. Add conditional routing logic if needed
4. Update the UI to include the new use case option

### Customizing News Writer

Edit `src/langgraphagenticai/nodes/news_writer_nodes.py`:
- Modify prompts for different writing styles
- Adjust article evaluation criteria
- Configure web scraping parameters

## Development

### Code Organization

- **Nodes**: Self-contained units of work that process state
- **State**: Immutable state passed between nodes
- **Edges**: Define flow between nodes (conditional or direct)
- **LLM Integration**: Factory pattern for multiple providers

### Adding New LLM Providers

1. Add provider to `loadllms.py`
2. Implement loading method
3. Update UI selection options
4. Add to constants

## Troubleshooting

**API Key Errors**:
- Verify your API key is correct
- Ensure the selected LLM matches your API key
- Check environment variables if using that method

**Model Not Found**:
- For Ollama: Ensure the model is pulled locally
- For OpenAI/Groq: Verify model name spelling

**Memory Issues**:
- Click "Reset Conversation" to clear the thread
- Check that thread_id is being maintained in session state

## Roadmap

- [ ] Add article evaluation loop (currently commented out)
- [ ] Support for more LLM providers (Anthropic, Cohere, etc.)
- [ ] Enhanced web scraping with better content extraction
- [ ] Multi-language support for news writing
- [ ] Export conversation history
- [ ] Custom system prompts via UI
- [ ] Fact-checking integration
- [ ] SEO optimization for generated content

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license information here]

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Streamlit](https://streamlit.io/)
