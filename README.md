# 🤖 Autonomous Task Automation Agent (LangGraph State Machine)

An advanced, production-grade autonomous agent architecture built using **LangGraph**, **LangChain**, and **Streamlit**. Moving beyond standard linear prompt engineering, this application implements a cyclic state machine utilizing a Supervisor-Executor model with conditional routing and self-correction loops to execute complex multi-step tasks end-to-end.

---

## 🛠️ Tech Stack & Architecture Foundations

* **State Machine Orchestration:** LangGraph (Handles explicit state dictionaries, loop boundaries, and conditional graph routing)
* **LLM Cognitive Brain:** Google Gemini (Generative AI reasoning engine via `langchain-google-genai`)
* **User Interface Framework:** Streamlit (Provides real-time interactive user dashboards)
* **Data Validation:** Pydantic v2 (Ensures strictly typed execution logs and runtime schema validation)

                 ┌───────────────────────────┐
                 │     User Input Query      │
                 └─────────────┬─────────────┘
                               ▼
                 ┌───────────────────────────┐
  ┌─────────────>│     Supervisor Agent      │<─────────────┐
  │              │          (Node)           │              │
  │              └─────────────┬─────────────┘              │
  │                            │                            │
  │                    [Conditional Route]                  │
  │                            │                            │
  │             Is Action == 'use_tool'?                    │
  │              ├── Yes ────────────── No ──┐              │
  │              ▼                           ▼              │
┌─────┴──────────────┐                  ┌─────────────────┐ │
│   Tool Executor    │                  │  Final Outcome  │ │
│       (Node)       │                  │     Analysis    │ │
├────────────────────┤                  └─────────────────┘ │
│ Executing:         │                           │          │
│ write_report_to_fi │                           ▼          │
└────────────────────┘                        [ END ]       │
│                                                           │
└─────────────────── [Loop Back] ───────────────────────────┘


---

## 🎯 Key Architectural Features

1. **Supervisor-Worker Topology:** A centralized supervisor node evaluates task states and past execution histories to determine whether to call a tool or finalize execution dynamically.
2. **Deterministic Graph Routing:** Utilizes conditional edges to prevent infinite runtime loops by establishing rigid iteration caps.
3. **Structured Schema Parsing:** Forces the raw LLM output into validated JSON objects mapping directly to tool parameter signatures.
4. **Self-Correction Framework:** Detects runtime exceptions or formatting errors natively, allowing the agent to update its internal context memory and self-correct on the next loop iteration.

---

## 🚀 Setup and Installation

### 1. Clone the Workspace
```bash
git clone [https://github.com/YOUR_USERNAME/langgraph-automation-agent.git](https://github.com/YOUR_USERNAME/langgraph-automation-agent.git)
cd langgraph-automation-agent
2. Configure Python Environment (Python 3.12 Recommended)
To prevent build issues with older system tools, run the application using a stable Python 3.12 environment:

Bash
python -m pip install -r requirements.txt
3. Launch the Application Dashboard
To bind the local application server explicitly to port 8501, execute the following command in your terminal:

Bash
python -m streamlit run agent.py --server.port 8501
Once executed, the secure interface dashboard will become immediately accessible at: http://localhost:8501

🧪 Testing Guide: Verification Case Study
To evaluate the agentic looping system, state context retention, and file-system interaction tools, run the following standardized evaluation case study:

📝 Test Case: Technical Report Generation & File Saving Ability
Open your browser to the local hosting interface (localhost:8501).

Expand the Authentication sidebar on the top-left and enter a valid Gemini API Key.

Copy and paste this complex instruction block directly into the main query input field:

Testing Input Prompt: > "Analyze the main structural differences between monolithic applications and microservices architectures. Compile your findings into a clean Markdown summary report highlighting performance tradeoffs, and save this report to my disk."

Click the "Launch Autonomous Flow" button.

🔍 Verification Breakdown (What to Look For)
Graph Orchestration Logs: The app will output a real-time running log feed. You will observe Iteration 1: Supervisor assessing workflow paths, followed by an explicit log indicating that the agent chose to invoke write_report_to_file.

Autonomous Tool Execution: The system will capture the generated technical analysis and pipe it safely into your local computer directory.

Local File Output Verification: Minimize your browser and open your project folder code layout. You will see a brand-new file instantly generated named agent_output_report.txt containing the formatted microservices breakdown written entirely by the AI agent.

📜 Repository Structure
agent.py - Core compiled graph network containing nodes, edges, tools, and UI layers.

requirements.txt - Strictly pinned micro-dependencies.

README.md - Technical project documentation and system case studies.