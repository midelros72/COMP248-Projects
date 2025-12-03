# Health Research Agentic System

A multi-agent system for health research and summarization using RAG (Retrieval-Augmented Generation), designed for Research Analysts working in the health enquiries domain.

## 🎯 Project Overview

This system implements a multi-agent architecture with:
- **Controller Layer**: Mediates between UI and agents
- **4 Specialized Agents**: Planner, Search, Summarization, Reflective
- **RAG Integration**: FAISS vector store for document retrieval
- **User Feedback Loop**: Collects ratings and comments for quality improvement
- **Session Management**: Tracks queries and feedback per session

## 🏗️ Architecture

```
User Interface (Streamlit)
        ↓
System Controller (Validation, Session Management)
        ↓
Orchestrator Agent (Task Coordination)
        ↓
    ┌───┴───┬──────────┬────────────┐
    ↓       ↓          ↓            ↓
Planner  Search  Summarizer  Reflective
          ↓
      FAISS (RAG)
```

## 📋 Features

### Core Capabilities
- ✅ Multi-agent query processing
- ✅ RAG-based document retrieval
- ✅ Health-focused summarization with disclaimers
- ✅ Quality evaluation and reflection
- ✅ User feedback collection (ratings + comments)
- ✅ Session tracking and history
- ✅ Input validation and sanitization

### Design Updates (Based on Professor Feedback)
1. ✅ **Controller Layer**: UI no longer communicates directly with Orchestrator
2. ✅ **User Feedback**: Integrated into Reflective Agent for quality improvement
3. ✅ **Class Diagram**: Comprehensive UML diagrams created

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**
```powershell
git clone <repository-url>
cd COMP248-Projects
```

2. **Create virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **⚠️ IMPORTANT: Configure LLM (Ollama or OpenAI)**

**Option A: Use Local Ollama (Recommended)**
1. Install [Ollama](https://ollama.com/)
2. Pull the model: `ollama pull llama3.2`
3. Create `.env` file:
```properties
USE_OLLAMA=true
OLLAMA_MODEL=llama3.2
```

**Option B: Use OpenAI**
```powershell
# Copy the example environment file
Copy-Item .env.example .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/account/api-keys
# Replace: OPENAI_API_KEY=sk-your-actual-api-key-here
```

5. **Initialize FAISS** (if needed)
```powershell
python kb\load_data.py
```

6. **Run tests** (optional but recommended)
```powershell
python test_system.py
```

7. **Start the Streamlit UI**
```powershell
streamlit run ui.py
```

8. **Access the application**
Open your browser to `http://localhost:8501`

**📖 See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions and troubleshooting.**

## 📖 Usage

1. **Submit a Query**: Enter your health-related question
2. **View Results**: See the multi-agent pipeline results
3. **Provide Feedback**: Rate the summary and add comments
4. **Request Improvements**: Check the box to request a revised summary
5. **View History**: Expand session history to see past queries

### Example Queries
- "What are the symptoms of diabetes?"
- "How is heart disease prevented?"
- "What causes high blood pressure?"
- "How does sleep affect mental health?"
- "What is antibiotic resistance?"
- "Why is a balanced diet important?"

## 🧪 Testing

Run the comprehensive test suite:
```powershell
python test_system.py
```

**Test Coverage:**
- ✅ Data Models (Query, Summary, Feedback, etc.)
- ✅ Input Validator (sanitization, validation)
- ✅ Session Manager (tracking, expiration)
- ✅ Agent Classes (all 4 agents)
- ✅ System Controller (end-to-end workflow)

**Current Status:** 5/5 tests passing ✅

## 📁 Project Structure

```
COMP248-Projects/
├── base_agent.py              # Abstract base agent class
├── models.py                  # Data models (Query, Summary, etc.)
├── controller.py              # System controller
├── validator.py               # Input validation
├── session_manager.py         # Session management
├── ui.py                      # Streamlit UI
├── app.py                     # Legacy orchestration
├── test_system.py            # Test suite
├── agents/
│   ├── planner_agent.py      # Research planning
│   ├── search_agent.py       # RAG retrieval
│   ├── summarize_agent.py    # Summary generation
│   └── reflective_agent.py   # Quality evaluation
├── tools/
│   └── rag_tool.py           # FAISS integration
├── kb/
│   ├── load_data.py          # Data loading
│   └── faiss_store/          # Vector database
├── diagrams/                  # UML diagrams
│   ├── component_diagram.puml
│   ├── sequence_diagram.puml
│   ├── class_diagram.puml
│   └── README.md
├── UPDATED_DESIGN.md         # Design documentation
├── DESIGN_CHANGES_SUMMARY.md # Implementation roadmap
├── IMPLEMENTATION_SUMMARY.md # What was built
└── requirements.txt          # Dependencies
```

## 🎨 Design Documents

- **[UPDATED_DESIGN.md](UPDATED_DESIGN.md)**: Complete design with diagrams
- **[DESIGN_CHANGES_SUMMARY.md](DESIGN_CHANGES_SUMMARY.md)**: Professor feedback responses
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**: What was implemented
- **[diagrams/README.md](diagrams/README.md)**: How to view UML diagrams

## 🔧 Components

### Agents

#### 1. Planner Agent
- **Role**: Task decomposition and planning
- **Input**: User query
- **Output**: Structured research plan

#### 2. Search Agent
- **Role**: Document retrieval from RAG store
- **Input**: Query text
- **Output**: Relevant document chunks
- **Tool**: FAISS vector search

#### 3. Summarization Agent
- **Role**: Generate accessible summaries
- **Input**: Retrieved documents
- **Output**: Health summary with disclaimers
- **Features**: Re-summarization based on feedback

#### 4. Reflective Agent
- **Role**: Quality evaluation
- **Input**: Summary + optional user feedback
- **Output**: Reflection report with scores
- **Metrics**: Coherence, completeness, factuality

### Controller Layer

**SystemController** manages:
- Input validation (length, safety)
- Query routing to agents
- Feedback processing
- Session state
- Response formatting

## 📊 Data Models

### Query
- Unique ID, text, timestamp
- Session ID, user context

### Summary
- Content, source docs, confidence
- Version tracking

### UserFeedback
- Rating (1-5), comments
- Improvement requested flag
- Timestamp

### ReflectionReport
- Coherence, completeness, factuality scores
- Suggestions for improvement
- Revision needed flag

## 🔒 Responsible AI

### Privacy
- No personal health data stored
- Only public medical sources used
- Local-only FAISS storage

### Disclaimers
- All summaries include medical disclaimers
- Explicitly not medical advice
- Recommends consulting healthcare professionals

### Fairness
- Multi-source retrieval to reduce bias
- User feedback integration for quality

## 📈 Performance

From test results:
- **Query Processing**: ~0.19s (excluding LLM calls)
- **Vector Search**: Sub-second response
- **Session Operations**: Near-instant
- **UI**: Responsive and interactive

## 🛠️ Development

### Adding a New Agent

1. Create new file in `agents/`
2. Inherit from `BaseAgent`
3. Implement `process()` method
4. Add to orchestrator workflow

```python
from base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="my_001",
            name="My Agent",
            role="My Role"
        )
    
    def process(self, input_data):
        # Your logic here
        return result
```

## 🚧 Known Limitations

- Re-summarization flow exists but not fully wired
- No persistent feedback storage yet

## 📝 Future Enhancements

- [x] LLM integration for smarter summaries (Ollama/OpenAI)
- [ ] Complete re-summarization workflow
- [ ] Feedback analytics dashboard
- [ ] Web search capability
- [ ] User authentication
- [ ] Persistent database
- [ ] Production deployment

## 👥 Team

Team #1 - Health Enquiries Research  
COMP248 - AI Systems Design  
Centennial College, Fall 2025

## 📄 License

Educational project for Centennial College

## 🙏 Acknowledgments

- CDC, WHO, Health Canada for public health data
- FAISS for vector database
- Streamlit for UI framework
- CrewAI for multi-agent orchestration
