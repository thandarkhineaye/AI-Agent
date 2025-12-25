from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from google import genai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from langchain_core.messages import AIMessage

# Load all values from .env file (Like crediential data)
load_dotenv()

# 2. Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
tools = []

class ResearchResponse(BaseModel):
    topic : str
    summary : str
    sources : list[str]
    tools_used : list[str]

# 2. Setup Parser and Model
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# 3. Create the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
        """
        You are a content creator that will help generate a content video and posts.
        Answer the user query and use neccessary tools.
        Wrap the output in this format and provide no other text\n{format_instructions}
        """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions())

# 4. Construct the Agent
agent = create_agent(llm, tools, prompt)
#agent_executor = agent.invoke(agent=agent, tools=[], verbose=True)

# 5. Run
raw_response = agent.invoke({"messages" : [("user", "What is the capital of Japan?")]})
# The final result from the agent is stored in the 'messages' list as the last AIMessage
final_message = raw_response['messages'][-1]

if isinstance(final_message, AIMessage):
    try:
        # We parse only the FINAL string from the agent
        structured_response = parser.parse(final_message.content)
        print("--- Parsed Successfully ---")
        print(f"Topic: {structured_response.topic}")
        print(f"Summary: {structured_response.summary}")
    except Exception as e:
        print(f"Parsing Failed. Gemini sent: {final_message.content}")
        print(f"Error: {e}")

