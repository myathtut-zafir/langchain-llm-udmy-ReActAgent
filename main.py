from typing import Union, List
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from dotenv import load_dotenv
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """text by character"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip('"')
    
    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")

if __name__ == "__main__":
    print("hello")
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:
    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=",".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(temperature=0, stop= ["\nObservation", "Observation"])
    agent = ({"input": lambda x: x["input"]} | prompt | llm| ReActSingleInputOutputParser())
    agent_step:Union[AgentAction,AgentFinish] = agent.invoke({"input": "What is the length of 'DOG' in characters?"})
    print(agent_step)
    
    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input
        print("tool_input")
        print(tool_name)
        observation = tool_to_use.func(str(tool_input))
        print(f"{observation=}")
