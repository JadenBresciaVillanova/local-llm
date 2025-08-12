# Local LLM Full-Stack AI Platform

<p align="center">
  <img alt="Project Demo GIF" src="https://i.imgur.com/your-demo-link-here.gif" width="80%">
  <br/>
  <i>A private, full-stack AI platform with advanced RAG and agentic capabilities, designed for absolute privacy.</i>
</p>

<p align="center">
  <img alt="Skill Icons" src="https://skillicons.dev/icons?i=python,fastapi,typescript,nextjs,tailwind,postgres,mongodb,docker,kafka,prometheus,grafana,github" />
</p>

## Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [The Agentic Workflow](#the-agentic-workflow)
- [Observability](#observability)
- [Project Journey & Challenges](#project-journey--challenges)
- [Contributing](#contributing)
- [License](#license)

## About The Project

This project is a self-hosted AI platform that allows you to run open-source large language models locally, leveraging the power of modern tools like Ollama. It provides a complete ecosystem from a sleek Next.js frontend to a robust FastAPI backend, all designed with absolute privacy and advanced functionality in mind.

The core of the platform is its powerful **Retrieval-Augmented Generation (RAG)** and **Agentic Workflow** systems. You can upload your own documents and have the AI use them as a knowledge base. A sophisticated agentic router analyzes your prompts to decide whether to use a single, efficient model for simple tasks or to orchestrate a multi-model pipeline for complex, multi-step queries that require reasoning and tool use.

This platform serves as a powerful sandbox for exploring the capabilities of local LLMs, MLOps, and full-stack AI application development.

## Key Features

-   **🤖 Intelligent Agentic Chat:** Go beyond simple Q&A. An agentic router analyzes prompt complexity and deploys specialized models for multi-step reasoning, summarization, and code generation.
-   **📚 Retrieval-Augmented Generation (RAG):** Upload multiple documents (`.txt`, `.docx`, etc.) and select which ones the AI should use as context for its answers, turning it into a personalized knowledge expert.
-   **🧠 Smart Context Handling:** The system intelligently decides whether to read a small file's full content for perfect accuracy or use a chunked vector search for large documents to ensure scalability.
-   **🔐 Secure & Private:** The entire stack is self-hosted with Docker. Your data and conversations never leave your machine. User access is secured via GitHub OAuth2.
-   **📊 Real-time Observability:** A full MLOps stack featuring Kafka for event logging, Prometheus for metrics, and Grafana for live dashboards provides deep insights into system performance and usage.
-   **✨ Modern Full-Stack UI:** A responsive and intuitive frontend built with Next.js and Tailwind CSS, featuring dedicated pages for Chat, Document Management, Model Viewing, and Chat History.

## Tech Stack

| Category         | Technologies                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------- |
| **Backend**      | Python, FastAPI, SQLAlchemy, Alembic, `asyncpg`, `motor`                                                   |
| **Frontend**     | Next.js, TypeScript, Tailwind CSS, NextAuth.js, Axios                                                    |
| **Databases**    | PostgreSQL (with `pgvector` extension for embeddings), MongoDB (for chat logs & file metadata)           |
| **AI / LangChain** | LangChain, Ollama, `unstructured`, `python-docx`                                                           |
| **Observability**| Kafka, Prometheus, Grafana                                                                               |
| **Auth**         | OAuth2 (GitHub Provider)                                                                                 |
| **Tooling**      | Docker, Docker Compose, Uvicorn, Poetry, Pre-commit                                                      |

## System Architecture

The application is designed with a decoupled front-end and back-end architecture, containerized for easy deployment.

1.  **Frontend:** A Next.js application serves the user interface, handling user interactions, authentication state, and API calls to the backend.
2.  **Backend:** A FastAPI REST API provides endpoints for chat, file management, authentication, and metrics. It uses async practices for high performance.
3.  **Databases:**
    *   **PostgreSQL with `pgvector`** stores the vectorized chunks of uploaded documents, enabling efficient similarity searches for the RAG pipeline.
    *   **MongoDB** stores unstructured data like chat conversation history and file metadata (including raw content for the "Direct Read" strategy).
4.  **Agentic Core:** This is the brain of the backend. When a chat request arrives in "agent mode," a Triage model first classifies its complexity. Simple prompts are routed to an efficient model. Complex prompts trigger the multi-step `run_multi_agent_workflow`, which uses a Planner LLM to orchestrate calls to various worker LLMs based on their strengths.
5.  **Observability Pipeline:** The FastAPI application emits structured logs and events to a **Kafka** topic. A separate consumer (or direct integration) could process these. **Prometheus** scrapes metrics directly from a `/metrics` endpoint on the backend, and **Grafana** visualizes this data in dashboards.
   
<p align="center">
  <img width="491" height="801" alt="image" src="https://github.com/user-attachments/assets/c9f2f9e7-15fb-4c6c-af5b-207afc20866c" />
</p>

## Getting Started

Follow these instructions to get the entire platform up and running on your local machine.

### Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose
-   [Python](https://www.python.org/downloads/) 3.10+ and [Poetry](https://python-poetry.org/docs/#installation) for backend dependency management
-   [Node.js](https://nodejs.org/en) (LTS version) and `npm` for frontend dependency management
-   [Git](https://git-scm.com/downloads)

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/local-llm.git
    cd local-llm
    ```

2.  **Environment Configuration**
    Create a `.env` file in the root directory by copying the example. This file will hold your secrets and configuration.
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and fill in the required values, especially your `GITHUB_ID` and `GITHUB_SECRET` for OAuth to work.

3.  **Launch Docker Services**
    This command will start PostgreSQL, MongoDB, Kafka, Prometheus, and Grafana.
    ```bash
    docker-compose up -d
    ```

4.  **Setup the Backend**
    ```bash
    cd backend

    # Install Python dependencies using Poetry
    poetry install

    # Apply database migrations
    poetry run alembic upgrade head

    # Start the backend server
    poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The backend API will be available at `http://localhost:8000`.

5.  **Setup the Frontend**
    Open a new terminal window.
    ```bash
    cd frontend

    # Install Node.js dependencies
    npm install

    # Start the frontend development server
    npm run dev
    ```

6.  **Access the Application**
    Open your browser and navigate to **`http://localhost:3000`**. You should be greeted by the sign-in page.

## Usage

1.  **Sign In:** Click the "Sign In" button and authenticate using your GitHub account.
2.  **Upload Documents:** Navigate to the "Docs" page to upload your files.
3.  **Chat with your AI:** Go to the "Chat" page. You can type a prompt and select a specific model to use, or choose "Agent Mode" to let the system decide.
4.  **Use RAG:** When chatting, select one or more of your uploaded documents from the sidebar to provide them as context to the agent.
5.  **View History & Metrics:** Explore the "History" and "Metrics" pages to review past conversations and see live system performance.

## The Agentic Workflow

The "Agent Mode" is powered by a sophisticated multi-step process:

1.  **Triage:** A fast `llama3.1:8b` model first classifies the user's prompt as `Simple` or `Complex`. It considers a prompt complex if it requires using file context, has multiple parts, or needs chat history.
2.  **Simple Path:** Simple prompts are sent to a `Performance-Aware Router` that chooses the most efficient model for a quick, single-shot answer.
3.  **Complex Path (`run_multi_agent_workflow`):**
    *   **Smart Context Retrieval:** The system checks the size of the selected files. Small files are read entirely ("Direct Read") for maximum accuracy. Large files are processed via a vector search ("Chunked RAG") for scalability.
    *   **Goal-Oriented Planning:** A Planner LLM deconstructs the user's request into a checklist of goals.
    *   **Iterative Execution:** The Planner loops, checking its progress against the checklist. In each loop, it picks the next unfinished task and selects the best "Worker" LLM for that job (e.g., `codellama` for code, `gemma` for simple extraction).
    *   **Completion:** Once all items on the checklist are satisfied by observations in its history, the agent synthesizes the results into a final answer and stops.

## Observability

-   **Prometheus:** Scrapes metrics from the backend at `http://localhost:8000/metrics`.
-   **Grafana:** Visualizes the Prometheus data. Access it at `http://localhost:3001` (default user/pass: `admin`/`admin`). You can build dashboards to track API latency, error rates, LLM response times, etc.
-   **Kafka:** The backend logs structured events to Kafka, providing a stream for real-time monitoring, alerting, or further analysis.

## Project Journey & Challenges

The inspiration for this project came from discovering Ollama and a curiosity to compare local open-source LLMs against cloud giants like ChatGPT and Claude. I wanted to understand the full stack, from hardware to a custom UI.

This initial curiosity quickly evolved into building a private, full-stack AI platform. I started with the RAG concept, allowing users to select specific files as context. Next, I added the agentic workflow with its router model to handle varying prompt complexity. The frontend was built with Next.js and TypeScript, and secure GitHub OAuth2 was added for access control. Finally, to understand performance, I integrated a full observability stack with Kafka, Prometheus, and Grafana.

Along the way, I faced several challenges:
-   **Docker & `pgvector`:** Correctly initializing the PostgreSQL database with the `pgvector` extension inside Docker was an early hurdle.
-   **Race Conditions:** In the file upload system, the chat request would sometimes arrive before the file embedding process was complete, leading to incorrect AI responses.
-   **Prompt Engineering:** My initial system prompts were over-constrained, preventing the LLMs from using their full reasoning abilities. Fine-tuning the agent's "meta-prompts" was key to making the workflow functional.
-   **Agentic Loops:** The agent would often get stuck in loops or perform unnecessary work. This was solved by designing a more "goal-oriented" prompt that forced the agent to create and follow a checklist based on the user's request.

Overcoming these challenges resulted in a powerful, self-hosted AI platform and provided immense experience in agentic AI design, MLOps, and architecting a complete system with a modern tech stack.

## Contributing

Contributions are welcome! Please follow the standard fork-and-pull-request workflow.

-   For frontend changes, please refer to the `frontend/README.md`.
-   For backend changes, ensure code is formatted with `black` and `isort`, and passes any pre-commit hooks.

## License

This project is licensed under the **GNU AGPL v3.0**. Please see the `LICENSE` file for full details. Note that some plugins or dependencies may have their own licenses.
