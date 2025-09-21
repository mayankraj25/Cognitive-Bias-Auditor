# 🧠 Cognitive Bias Auditor

An AI-powered, private journaling application designed to act as a thinking coach. This tool helps you practice metacognition by analyzing your written reflections and gently highlighting potential cognitive biases in your reasoning.

## What It Does

The Cognitive Bias Auditor provides a secure space for you to explore your own thought processes. The workflow is simple but powerful:

1.  **Write a Reflection:** You write a journal entry about a decision you're struggling with, a recent argument, or a strongly held belief.
2.  **Analyze Your Thinking:** With a click of a button, your text is sent to a secure backend where a local Large Language Model (LLM) analyzes it.
3.  **Receive AI Feedback:** The AI compares your reasoning against a comprehensive knowledge base of common cognitive biases. It then provides non-judgmental feedback, quoting your own words as evidence and explaining how a particular bias might be influencing your perspective.
4.  **Review and Grow:** All reflections and their analyses are saved privately, allowing you to track patterns in your thinking over time.

## Key Features

* **Full-Stack Architecture:** A modern web application with a distinct frontend and backend.
* **Secure User Authentication:** Uses JWT tokens to ensure all user reflections are completely private and secure.
* **AI-Powered Text Analysis:** Leverages a local LLM (Llama 3) via LangChain to perform nuanced analysis of user input.
* **Dynamic Knowledge Base:** The AI's knowledge is populated from a simple CSV file, making it easy to expand and customize.
* **Dockerized for Portability:** The entire application is containerized with Docker, allowing it to be run on any machine with a single command.
* **Multi-Platform Image:** The Docker image is built for both AMD64 (Windows/Intel Macs) and ARM64 (Apple Silicon Macs) architectures, ensuring cross-platform compatibility.

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **Database** | SQLite with SQLAlchemy ORM |
| **AI Framework** | LangChain |
| **LLM** | Ollama (with Llama 3) |
| **Containerization**| Docker & Docker Hub |
| **Data Handling** | Pandas |

## How to Run This Project

There are two ways to run this application: the easy way using Docker, or the developer way by running the servers manually.

### Option 1: Run with Docker (Recommended)

This is the simplest method and will work on any machine with Docker installed, regardless of whether you have Python set up.

1.  **Install Docker Desktop:** Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop/).
2.  **Run the Application:** Open your terminal (or PowerShell on Windows) and run the following single command:

    ```bash
    docker run -p 8501:8501 -p 8000:8000 mayankraj25/cognitive-bias-auditor:latest
    ```
3.  **Open the App:** Once the download is complete and the servers start, open your web browser and navigate to:
    **[http://localhost:8501](http://localhost:8501)**

### Option 2: Run Locally (For Developers)

Use this method if you want to modify the code.

1.  **Prerequisites:**
    * Python 3.10+
    * An Ollama instance running with the Llama 3 model pulled (`ollama pull llama3`).

2.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-github-username/CognitiveBiasAuditor.git](https://github.com/your-github-username/CognitiveBiasAuditor.git)
    cd CognitiveBiasAuditor
    ```

3.  **Set Up the Environment:**
    * Create and activate a virtual environment:
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        ```
    * Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Run the Backend Server:**
    * Open a terminal window and run the following command to start the FastAPI server. It will automatically create and seed the database on its first run.
        ```bash
        uvicorn backend.main:app --host 0.0.0.0 --port 8000
        ```
    * Leave this terminal running.

5.  **Run the Frontend Server:**
    * **Open a new, separate terminal window.**
    * Activate the virtual environment again (`source .venv/bin/activate`).
    * Run the Streamlit app:
        ```bash
        streamlit run app.py
        ```
6.  **Open the App:** Your browser should open to the application automatically. If not, navigate to the local URL provided in the terminal (usually `http://localhost:8501`).

## Project Structure

The project is organized into a clean, modular structure:

```text
CognitiveBiasAuditor/
├── app.py                # The Streamlit frontend application
├── backend/              # The FastAPI backend application
│   ├── auth.py           # Authentication and JWT logic
│   ├── crud.py           # Database create, read, update, delete functions
│   ├── database.py       # Database connection and seeding logic
│   ├── main.py           # API endpoints
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic data validation schemas
│   └── utils.py          # Utility functions (e.g., password hashing)
├── data/
│   └── biases.csv        # The AI's knowledge base of cognitive biases
├── utils/
│   ├── analysis_chain.py # LangChain prompt and chain definition
│   └── config.py         # Configuration loader
├── .env                  # Environment variables (e.g., OLLAMA_MODEL)
├── Dockerfile            # Docker configuration for building the image
└── requirements.txt      # Python package dependencies
