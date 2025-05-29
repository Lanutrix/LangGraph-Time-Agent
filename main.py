from datetime import datetime
from typing import Annotated, Literal
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


@tool
def get_current_time() -> dict:
    """Return the current UTC time in ISO-8601 format.
    Example → {"utc": "2025-05-21T06:42:00Z"}"""
    current_utc = datetime.utcnow()
    return {"utc": current_utc.strftime("%Y-%m-%dT%H:%M:%SZ")}


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def create_agent():
    # Настройка модели Ollama
    model = ChatOllama(
        model="qwen2.5:7b-instruct",
        base_url="http://localhost:11434"
    )
    
    # Привязка инструментов к модели
    tools = [get_current_time]
    model_with_tools = model.bind_tools(tools)
    
    def call_model(state: State):
        messages = state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def should_continue(state: State) -> Literal["tools", "end"]:
        messages = state["messages"]
        last_message = messages[-1]
        
        if last_message.tool_calls:
            return "tools"
        return "end"
    
    # Создание узла для инструментов
    tool_node = ToolNode(tools)
    
    # Построение графа
    workflow = StateGraph(State)
    
    # Добавление узлов
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    # Добавление переходов
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()


# Создание и экспорт графа
graph = create_agent()
