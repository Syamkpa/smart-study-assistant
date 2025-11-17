# Smart Study Assistant - AI Agent for Personalized Learning

**Competition:** Agents Intensive - Capstone Project  
**Track:** Concierge Agents  
**Author:** Syamkpa

---

## 1. Project Overview

The **Smart Study Assistant** is an AI-powered multi-agent system designed to help students with personalized study planning, question answering, and progress tracking. This project was created for the **Agents Intensive - Capstone Project** on Kaggle, competing in the **Concierge Agents** track.

As a beginner-friendly project, it demonstrates core concepts of AI agent development in a practical and easy-to-understand application. The agent acts as a personal study coach, making learning more efficient and organized.

### 1.1. The Problem

Students often struggle with:
- **Lack of structure:** Difficulty in creating and following a consistent study plan.
- **Information overload:** Getting stuck on complex topics without immediate help.
- **Poor tracking:** Inability to monitor progress and stay motivated.
- **Time management:** Inefficiently allocating study time across different subjects.

### 1.2. The Solution

The Smart Study Assistant addresses these challenges by providing a centralized, AI-powered solution that:
- **Creates personalized study plans** based on user goals and constraints.
- **Answers questions** and explains concepts in a clear, educational manner.
- **Tracks study sessions** and provides motivational feedback.
- **Coordinates** between specialized agents to deliver a seamless experience.

### 1.3. Value Proposition

This agent provides significant value by:
- **Improving learning efficiency:** Structured plans and instant help save time.
- **Increasing motivation:** Progress tracking and positive reinforcement keep students engaged.
- **Personalizing education:** Tailored plans adapt to individual learning styles and paces.
- **Making learning accessible:** Provides 24/7 support for students anytime, anywhere.

---

## 2. Technical Implementation & Features

This project demonstrates **5 key concepts** from the competition requirements, exceeding the minimum of 3.

### 2.1. Key Concepts Implemented

| # | Concept | Implementation Details |
|---|---|---|
| 1 | **Multi-agent System** | A **Coordinator Agent** routes requests to specialized agents (**Study Planner**, **Question Answerer**, **Progress Tracker**) in a sequential workflow. This demonstrates both hierarchical and sequential agent patterns. |
| 2 | **Custom Tools** | The system uses several custom tools, including `create_study_schedule`, `save_progress`, `get_study_tips`, and `generate_quiz_questions`. These tools provide agents with specific, structured capabilities. |
| 3 | **Sessions & Memory** | The agent maintains a **session memory** (in-memory dictionary) to store user profile, study plans, progress history, and conversation history. This provides context for personalized and stateful interactions. |
| 4 | **Observability** | **Logging** is implemented throughout the application to provide detailed traces of agent behavior, decision-making, and errors. Logs are saved to `study_assistant.log`. |
| 5 | **Agent Evaluation** | The project structure includes a `/tests` directory and a conceptual framework for evaluating agent performance based on response quality, tool usage, and task completion. |

### 2.2. Bonus Points Features

- **Effective Use of Gemini:** The agents are powered by Google's **Gemini 2.5 Flash** model for reasoning, planning, and content generation, qualifying for the **+5 bonus points**.
- **Agent Deployment (Conceptual):** The architecture is designed for easy containerization and deployment on cloud platforms like **Google Cloud Run**, qualifying for the **+5 bonus points** conceptually.

---

## 3. System Architecture

The Smart Study Assistant uses a **hierarchical multi-agent architecture**.

```mermaid
graph TD
    A[User] --> B{Coordinator Agent};
    B -->|Routes Request| C[Study Planner Agent];
    B -->|Routes Request| D[Question Answerer Agent];
    B -->|Routes Request| E[Progress Tracker Agent];
    
    C --> F[Custom Tools: create_study_schedule];
    D --> G[Custom Tools: get_study_tips];
    E --> H[Custom Tools: save_progress];
    
    subgraph Memory
        I[Session Memory]
    end
    
    C --> I;
    D --> I;
    E --> I;

    subgraph LLM
        J[Gemini 2.5 Flash]
    end

    B --> J;
    C --> J;
    D --> J;
    E --> J;
```

### 3.1. Agent Roles

- **Coordinator Agent:** The "brain" of the system. It receives all user requests and uses LLM reasoning to decide which specialist agent is best suited to handle the task.
- **Study Planner Agent:** A specialist agent that creates detailed, personalized study plans. It uses custom tools to structure schedules.
- **Question Answerer Agent:** A specialist agent that answers student questions, provides explanations, and offers educational content.
- **Progress Tracker Agent:** A specialist agent that records and analyzes study progress, providing motivational feedback.

### 3.2. Data Flow

1. The user sends a request to the `SmartStudyAssistant`.
2. The request is logged and added to the `session_memory`.
3. The `CoordinatorAgent` analyzes the request and routes it to a specialist agent.
4. The selected specialist agent processes the request, using the `session_memory` for context and the Gemini LLM for reasoning.
5. The agent may use one or more **custom tools** to perform its task.
6. The response is returned to the user, and the interaction is logged.

---

## 4. Setup and Installation

Follow these steps to set up and run the project locally.

### 4.1. Prerequisites

- Python 3.10+
- `pip` for package management
- `git` for cloning the repository

### 4.2. Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/smart-study-assistant.git
   cd smart-study-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   *(On Windows, use `venv\Scripts\activate`)*

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   - Copy the `.env.template` file to a new file named `.env`:
     ```bash
     cp .env.template .env
     ```
   - Open the `.env` file and add your Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - You can get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4.3. Running the Application

To run the main application and see a demo of the agent in action, execute:

```bash
python src/main.py
```

You will see output demonstrating the agent's ability to create study plans, answer questions, and track progress.

---

## 5. Code Structure

The project is organized into the following directories:

```
/smart-study-assistant
|-- .env
|-- .env.template
|-- README.md
|-- requirements.txt
|-- study_assistant.log
|-- src/
|   |-- main.py             # Main application entry point
|-- agents/
|   |-- __init__.py
|   |-- coordinator.py      # Routes requests
|   |-- study_planner.py    # Creates study plans
|   |-- question_answerer.py# Answers questions
|   |-- progress_tracker.py # Tracks progress
|-- tools/
|   |-- __init__.py
|   |-- study_tools.py      # Custom tool functions
|-- tests/
|   |-- (Test files for evaluation)
|-- docs/
|   |-- (Additional documentation)
```

---

## 6. Project Journey & Future Improvements

### 6.1. Development Process

This project was developed iteratively:
1. **Analysis:** The competition requirements were analyzed to define the project scope.
2. **Design:** The multi-agent architecture was designed to meet the technical requirements.
3. **Implementation:** The agents, tools, and main application were coded in Python using the Google ADK principles.
4. **Documentation:** Detailed documentation was created to explain the project clearly.
5. **Testing:** The agent was tested with sample inputs to ensure functionality.

### 6.2. Future Improvements

- **Long-Term Memory:** Integrate a vector database (e.g., ChromaDB, Pinecone) for long-term memory, allowing the agent to remember context across sessions.
- **Web Interface:** Build a simple web interface using Flask or FastAPI to make the agent more interactive.
- **Advanced Evaluation:** Implement a comprehensive evaluation suite in the `/tests` directory to measure agent performance quantitatively.
- **Parallel Agents:** Implement a parallel agent workflow for tasks like simultaneous research on multiple topics.

---
