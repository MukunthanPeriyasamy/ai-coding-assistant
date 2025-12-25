# Esec AI Assistant

Esec AI Assistant is a production-grade AI-powered tutor designed to help students learn effectively. It leverages large language models (via Groq) and a robust FastAPI backend to provide interactive, level-specific tutoring with real-time streaming responses and conversation memory.

## 🚀 Features

-   **Dual-Level AI Tutoring**: Specialized prompts for `beginner` and `advanced` learners.
-   **Real-time Streaming**: LLM responses are streamed to the frontend for a seamless user experience.
-   **Conversation Memory**: Remembers session history to provide context-aware answers.
-   **Secure Authentication**: JWT-based user registration and login system.
-   **Robust Tech Stack**: Built with FastAPI, LangChain, and Groq.

## 🛠️ Technical Stack

-   **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
-   **AI Framework**: [LangChain](https://python.langchain.com/)
-   **LLM Provider**: [Groq](https://groq.com/)
-   **Database**: SQLite (SQLAlchemy)
-   **Authentication**: JWT (JSON Web Tokens)
-   **Language**: Python 3.9+

## 📁 Project Structure

```text
esec-project/
├── backend/                # Root package (configured via imports)
├── database/               # Database configuration and migrations
│   └── db_config.py        # SQLite/SQLAlchemy setup
├── models/                 # Pydantic models and LLM configuration
│   ├── llm_config.py       # Groq/LangChain integration
│   └── user.py             # User models
├── services/               # Business logic
│   ├── auth_service.py     # User registration and authentication
│   └── tutor.py            # AI Tutor logic and streaming
├── prompts/                # Level-specific system prompts
│   ├── beginner_prompt.py  # Simplified explanations
│   └── advanced_prompt.py  # Technical/Detailed explanations
├── utils/                  # Helper functions
│   └── auth_utils.py       # JWT and password hashing
├── main.py                 # FastAPI application entry point
├── .env                    # Environment variables (ignored by git)
└── requirements.txt        # Project dependencies
```

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd esec-project
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_jwt_secret_key_here
```

### 5. Initialize the Database
The database is automatically initialized when you start the server.

## 🚀 Running the Application

Start the FastAPI server using `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 🔌 API Documentation

### Authentication
-   `POST /register`: Register a new user.
-   `POST /login`: Authenticate and receive a JWT token.

### AI Assistant
-   `POST /ai_tutor`: Interactive tutor endpoint.
    -   **Body**:
        ```json
        {
          "level": "beginner",  // or "advanced"
          "prompt": "What is a Linked List?",
          "session_id": "optional-session-id"
        }
        ```
    -   **Response**: Streaming text.
