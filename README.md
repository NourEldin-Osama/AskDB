# AskDB: AI-Powered Database Chatbot

**AskDB** is a full-stack application featuring an AI chatbot that allows users to interact with and query database content through a natural language interface. The backend is built with FastAPI and leverages LangChain with Google Generative AI, while the frontend uses Next.js, TypeScript, and Tailwind CSS.

---

## Features

- **User Authentication & Authorization**: Secure JWT-based login, registration, password management, and token handling.
- **Conversation Threads**: Users can create, manage (rename, delete), and switch between different conversation threads.
- **AI Chatbot**: Powered by LangChain and Google Generative AI (Gemini models), the chatbot can understand user queries, interact with the database (via SQL agent tools), and provide relevant answers.
- **Chat History**: Conversation history is persisted per thread using LangGraph's checkpointing with SQLite.
- **Database Integration**: Uses SQLModel for ORM interactions with a primary SQLite database for application data (users, threads) and allows the AI agent to query a separate specified database (e.g., `realestate.db`).
- **Web Search Capability**: Integrates Tavily Search for queries requiring external information.
- **Responsive UI**: A clean, modern chat interface built with Next.js, Tailwind CSS, and Shadcn UI components, suitable for desktop and mobile use.

---

## Tech Stack

### **Backend**

- Python 3.11+
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite (for application data and chat memory)
- LangChain & LangGraph
- `langchain-google-genai` (for Google AI models)
- `uv` (for package management)
- Alembic (for database migrations - *optional, currently using `SQLModel.metadata.create_all`*)
- Tavily Search API

### **Frontend**

- Next.js (React 18)
- TypeScript
- Tailwind CSS
- Shadcn UI
- `pnpm` (or `npm`/`yarn`)

---

## Prerequisites

- Node.js >= 18
- `pnpm` (recommended), `npm`, or `yarn`
- Python >= 3.11
- `uv` (Python package manager, install via `pip install uv`)
- Google AI API Key
- Tavily Search API Key

---

## Setup & Installation

### 1. Backend

```powershell
# Navigate to the backend directory
cd n:\AskDB\backend

# Create a .env file in the backend directory (n:\AskDB\backend\.env)
# Add the following required environment variables:
# GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
# TAVILY_API_KEY=YOUR_TAVILY_API_KEY
# SECRET_KEY=YOUR_STRONG_SECRET_KEY # Generate a strong random key


# (Optional) Place your target database (e.g., realestate.db)
# The chatbot tools are  configurable to use any SQLite file via the `chatbot_db_file` setting.

# run the following command to create a virtual environment and install dependencies and run the app
uv run askdb
```

The backend API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

### 2. Frontend

```powershell
# Navigate to the frontend directory
cd n:\AskDB\frontend

# Install dependencies
pnpm install

# (Optional) Create a .env.local file if you need to override the default API URL

# Start the Next.js development server
pnpm dev
```

The frontend application will be running at `http://localhost:3000`.

---

## Usage

1. Open `http://localhost:3000` in your browser.
2. If it's your first time, you might need to register a new user or log in using the default superuser credentials (Email: `admin@askdb.com`, Password: `admin1234` - defined in `app/core/config.py`).
3. Use the sidebar to create a "New Conversation" or select an existing one.
4. Type your questions about the data in the `realestate.db` (or the configured database) into the chat input and press Enter.
5. The chatbot will process your request, potentially querying the database or searching the web, and display the response.
6. You can rename or delete threads using the icons next to the thread title in the sidebar (hover to reveal).

---

## Environment Variables (Backend `.env` file)

| Variable                    | Description                                                                 | Default (if any)        |
| :-------------------------- | :-------------------------------------------------------------------------- | :---------------------- |
| `GOOGLE_API_KEY`            | **Required.** Your API key for Google Generative AI services.               | -                       |
| `TAVILY_API_KEY`            | **Required.** Your API key for the Tavily search tool.                      | -                       |
| `SECRET_KEY`                | **Required.** A strong secret key for signing JWT tokens.                   | -                       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiry time for JWT access tokens in minutes.                               | `11520` (8 days)       |
| `EMAIL_RESET_TOKEN_EXPIRE_HOURS` | Expiry time for password reset tokens in hours.                          | `24` (1 day)            |
| `SQLALCHEMY_DATABASE_URI`   | Connection string for the main application database.                        | `sqlite:///.../.askdb/askdb.db` |
| `memory_db_path`            | Path for the LangGraph checkpoint (chat memory) database.                   | `.../.askdb/checkpoints.sqlite` |
| `model_name`                | The Google Generative AI model to use for the chatbot.                      | `gemini-2.5-pro-exp-03-25` |
| `chatbot_db_file`           | Path to the SQLite database file used by the chatbot tools.                  | `./realestate.db`     |
| `FIRST_SUPERUSER`           | Email for the initial superuser created by `init_db`.                       | `admin@askdb.com`       |
| `FIRST_SUPERUSER_PASSWORD`  | Password for the initial superuser.                                         | `admin1234`             |
| `SERVER_HOST`               | Host address for the FastAPI server.                                        | `127.0.0.1`             |
| `SERVER_PORT`               | Port for the FastAPI server.                                                | `8000`                  |
| `all_cors_origins`          | Comma-separated list of allowed origins for CORS.                           | `http://localhost:3000,...` |

---

## Contributing

Contributions are welcome! Please follow standard fork-and-pull-request workflows.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Ensure tests pass.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details (if one exists).
