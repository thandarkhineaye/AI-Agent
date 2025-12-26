import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from tools import search_tool, wiki_tool, save_tool

load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


def run_agent(query: str):
    """
    True AI Agent that decides which tools to use and when.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)

    # Bind all tools to the LLM so it can choose
    llm_with_tools = llm.bind_tools([search_tool, wiki_tool, save_tool])

    # Initial prompt - Agent decides what to do
    system_message = f"""You are a research agent. You have access to these tools:
                        1. tavily_search_results_json - for web search
                        2. WikipediaQueryRun - for Wikipedia articles  
                        3. save_research - to save results to a file

                        Your task: Research "{query}"

                        Decide which tools to use, in what order, and how many times. You can:
                        - Use one tool or multiple tools
                        - Use tools in any order
                        - Skip tools if not needed
                        - Use a tool multiple times with different queries

                        After gathering information, save it using the save_research tool."""

    messages = [HumanMessage(content=system_message)]

    # Agent reasoning loop
    max_iterations = 10
    iteration = 0
    tools_used = []

    print("\n" + "="*50)
    print("AGENT STARTING - IT WILL DECIDE WHAT TO DO")
    print("="*50)

    response = llm_with_tools.invoke(messages)
    messages.append(response)

    # Loop while agent wants to use tools
    while response.tool_calls and iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")

        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call.get('args', {})
            print(f"🤖 Agent decided to use: {tool_name}")
            print(f"   Arguments: {tool_args}")
            tools_used.append(tool_name)

            try:
                # Agent decides which tool to execute
                if tool_name == 'search':
                    result = search_tool.invoke(tool_args)
                    print(f"   ✓ Tavily search completed")
                elif tool_name == 'wiki_search':
                    result = wiki_tool.invoke(tool_args)
                    print(f"   ✓ Wikipedia search completed")
                elif tool_name == 'save_text_to_file':
                    result = save_tool.invoke(tool_args)
                    print(f"   ✓ Results saved to file")
                else:
                    result = f"Unknown tool: {tool_name}"
                    print(f"   ✗ Unknown tool")

                # Add result back to agent's context
                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call['id']
                    )
                )
            except Exception as e:
                print(f"   ✗ Error: {e}")
                messages.append(
                    ToolMessage(
                        content=f"Error: {str(e)}",
                        tool_call_id=tool_call['id']
                    )
                )

        # Agent decides next action
        response = llm_with_tools.invoke(messages)
        messages.append(response)

    print(f"\n{'='*50}")
    print(f"AGENT FINISHED")
    print(f"Tools used: {list(set(tools_used))}")
    print(f"Total iterations: {iteration}")
    print(f"{'='*50}")

    # Get structured output
    final_prompt = f"""Based on your research, provide a summary in this JSON format:{parser.get_format_instructions()}"""

    messages.append(HumanMessage(content=final_prompt))
    final_response = llm.invoke(messages)

    return final_response.content, tools_used


# Main execution
query = input("What can I help you research? ")

if not query or query.strip() == "":
    print("Error: Please provide a valid query")
    exit()

try:
    final_content, tools_used = run_agent(query)

    print("\n" + "="*50)
    print("AGENT'S FINAL RESPONSE:")
    print("="*50)
    print(final_content)

    # Parse structured output
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    try:
        clean_content = final_content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content.replace(
                "```json", "").replace("```", "").strip()

        structured_response = parser.parse(clean_content)
        print("\n" + "="*50)
        print("STRUCTURED OUTPUT:")
        print("="*50)
        print(f"Topic: {structured_response.topic}")
        print(f"Summary: {structured_response.summary}")
        print(f"Sources: {structured_response.sources}")
        print(f"Tools Used: {structured_response.tools_used}")
    except Exception as e:
        print(f"\nCould not parse as structured data: {e}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
