import streamlit as st
import os
from typing import Annotated, TypedDict, Dict, Any
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

st.set_page_config(page_title="Autonomous LangGraph Agent", page_icon="🤖", layout="wide")
st.title("🤖 Autonomous Task Automation Agent")
st.write("An orchestrated LangGraph agent with tool-execution loops and conditional self-correction.")

with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Gemini API Key", type="password")
    if not api_key:
        st.warning("Please enter your Gemini API Key to run the agent.")

@tool
def write_report_to_file(content: str) -> str:
    """Writes a generated final text analysis or report to a local storage file."""
    try:
        filename = "agent_output_report.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: Content written safely to '{filename}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"

tools = {"write_report_to_file": write_report_to_file}

class AgentState(TypedDict):
    input_query: str
    agent_outcome: Dict[str, Any]
    iterations: int
    execution_logs: list

def supervisor_agent_node(state: AgentState) -> Dict[str, Any]:
    """Evaluates the task state and decides on taking actions or finishing."""
    logs = state.get("execution_logs", [])
    current_iteration = state.get("iterations", 0) + 1
    
    logs.append(f"Iteration {current_iteration}: Supervisor assessing workflow paths.")
    
    os.environ["GOOGLE_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    system_prompt = (
        "You are an autonomous supervisor managing an automation workflow.\n"
        "Analyze the user's objective and past execution logs to decide the next step.\n\n"
        f"User Objective: {state['input_query']}\n"
        f"Execution History: {logs}\n\n"
        "You have access to a tool named: 'write_report_to_file' if data preservation is needed.\n"
        "Respond strictly in JSON format matching this schema:\n"
        '{"action": "use_tool" or "finalize", "tool_name": "write_report_to_file" or null, "content": "arguments or final message text"}'
    )
    
    try:
        response = llm.invoke([HumanMessage(content=system_prompt)])
        clean_json = response.content.replace("```json", "").replace("```", "").strip()
        import json
        outcome = json.loads(clean_json)
    except Exception as e:
        outcome = {"action": "finalize", "tool_name": None, "content": f"Self-Correction trigger due to parsing error: {str(e)}"}
        
    return {
        "agent_outcome": outcome,
        "iterations": current_iteration,
        "execution_logs": logs
    }

def action_executor_node(state: AgentState) -> Dict[str, Any]:
    """Executes selected tools autonomously when requested by the supervisor."""
    outcome = state["agent_outcome"]
    logs = state["execution_logs"]
    
    tool_name = outcome.get("tool_name")
    tool_args = outcome.get("content", "")
    
    logs.append(f"Executing tool '{tool_name}' with requested parameters.")
    
    if tool_name in tools:
        tool_to_call = tools[tool_name]
        execution_result = tool_to_call.invoke({"content": tool_args})
        logs.append(f"Tool execution response output: {execution_result}")
    else:
        logs.append(f"Execution Error: Tool '{tool_name}' not found in runtime registry.")
        
    return {"execution_logs": logs}

def route_workflow_edge(state: AgentState) -> str:
    """Inspects state variables to calculate the next processing routing direction."""
    outcome = state["agent_outcome"]
    
    if state.get("iterations", 0) >= 5:
        return "stop_workflow"
        
    if outcome.get("action") == "use_tool":
        return "continue_to_tools"
    return "stop_workflow"

workflow_builder = StateGraph(AgentState)


workflow_builder.add_node("supervisor", supervisor_agent_node)
workflow_builder.add_node("executor", action_executor_node)

workflow_builder.set_entry_point("supervisor")


workflow_builder.add_conditional_edges(
    "supervisor",
    route_workflow_edge,
    {
        "continue_to_tools": "executor",
        "stop_workflow": END
    }
)


workflow_builder.add_edge("executor", "supervisor")

compiled_agent_graph = workflow_builder.compile()


user_input = st.text_input("Enter a complex automation instruction:", 
                           placeholder="Create a comprehensive executive summary report about DevOps architectures and save it to disk.")

if st.button("Launch Autonomous Flow") and api_key:
    if not user_input.strip():
        st.warning("Please type an input query first.")
    else:
        initial_input_state = {
            "input_query": user_input,
            "agent_outcome": {},
            "iterations": 0,
            "execution_logs": []
        }
        
        with st.spinner("Agent state machine running autonomously..."):
            final_output_state = compiled_agent_graph.invoke(initial_input_state)
            
        st.success("Workflow completed successfully!")
        
        st.subheader("📋 Step-by-Step Execution Journey")
        for log in final_output_state["execution_logs"]:
            st.info(log)
            
        st.subheader("🎯 Final Outcome Analysis")
        st.write(final_output_state["agent_outcome"].get("content")