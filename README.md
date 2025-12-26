# AI Research Assistant

An intelligent research automation tool that combines multiple data sources (web search and Wikipedia) with LLM-powered analysis to generate comprehensive, structured research reports.

## 🌟 Features

- **Multi-Source Research**: Automatically queries both Tavily search API and Wikipedia
- **Structured Output**: Generates well-formatted research summaries with proper citations
- **Automatic Saving**: Saves research results to file for future reference
- **LLM-Powered Analysis**: Uses Google's Gemini to synthesize and format information
- **Clean JSON Output**: Provides structured data in Pydantic models for easy integration

## 🏗️ Architecture

This project implements a **research automation pipeline** with the following workflow:
```
User Query → Tavily Search → Wikipedia Search → Combine Results → LLM Processing → Structured Output → Save to File
```

### Components:

1. **Search Tools**
   - `search_tool`: Tavily API integration for current web search
   - `wiki_tool`: Wikipedia API for encyclopedic information
   - `save_tool`: File system integration for persisting results

2. **LLM Integration**
   - Google Gemini 2.0 Flash for content synthesis
   - Pydantic models for structured output validation
   - JSON parsing with error handling

3. **Data Model**
```python
   class ResearchResponse(BaseModel):
       topic: str
       summary: str
       sources: list[str]
       tools_used: list[str]
```

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.8
langchain
langchain-google-genai
pydantic
python-dotenv
tavily-python  # for search_tool
wikipedia-api  # for wiki_tool
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-research-assistant.git
cd ai-research-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
GOOGLE_API_KEY=your_gemini_api_key
```

4. Run the application:
```bash
python main.py
```

## 📖 Usage

### Basic Usage
```python
python main.py
```

When prompted, enter your research query:
```
What can I help you research? Machine Learning in Healthcare
```

The tool will:
1. Search Tavily for current information
2. Query Wikipedia for encyclopedic context
3. Combine and analyze results using Gemini
4. Generate structured output
5. Save results to file

### Example Output
```json
{
  "topic": "Machine Learning in Healthcare",
  "summary": "Machine learning is revolutionizing healthcare through...",
  "sources": [
    "https://example.com/ml-healthcare",
    "https://en.wikipedia.org/wiki/Machine_learning_in_healthcare"
  ],
  "tools_used": ["tavily_search_results_json", "WikipediaQueryRun", "save_research"]
}
```

## 🛠️ Project Structure
```
ai-research-assistant/
│
├── main.py                # Main application script
├── tools.py               # Tool definitions (search, wiki, save)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | Yes |

### Customization

**Change LLM Model:**
```python
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
```

**Modify Output Format:**
Edit the `ResearchResponse` Pydantic model in `main.py`

**Add More Tools:**
Create new tools in `tools.py` and add to the workflow

## 🎯 Use Cases

- **Academic Research**: Quickly gather information from multiple sources
- **Market Research**: Combine current news with background information
- **Content Creation**: Generate well-sourced article summaries
- **Due Diligence**: Research companies, products, or technologies
- **Learning**: Deep dive into new topics with curated information

## 🔄 Workflow vs Agent

**Current Implementation**: Sequential Tool Execution Pipeline
- Fixed workflow: Always executes Tavily → Wikipedia → Save
- Predictable and reliable
- Best for consistent research patterns

**Future Enhancement**: True AI Agent
- LLM decides which tools to use and when
- Adaptive to query complexity
- Can skip unnecessary steps
- See `agent_version.py` for implementation

## 🐛 Troubleshooting

**Issue**: `ValueError: contents are required`
- **Solution**: Ensure query is not empty and API keys are valid

**Issue**: JSON parsing errors
- **Solution**: Check LLM output format, adjust temperature to 0

**Issue**: API rate limits
- **Solution**: Implement retry logic or use different API keys

## 📝 Future Enhancements

- [ ] Convert to true agentic system with autonomous decision-making
- [ ] Add more data sources (arXiv, PubMed, Google Scholar)
- [ ] Implement caching to avoid redundant API calls
- [ ] Add web interface using Streamlit or Gradio
- [ ] Support for multiple output formats (PDF, Markdown, HTML)
- [ ] Conversation history and follow-up questions
- [ ] Multi-language support


## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the LLM framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) for the language model
- [Tavily](https://tavily.com/) for search API
- [Wikipedia](https://www.wikipedia.org/) for encyclopedic data
