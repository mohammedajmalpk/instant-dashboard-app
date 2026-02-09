# Instant Dashboard App

A fast application that generates professional, interactive dashboards from JSON data using AI. The project consists of a backend API and a static frontend interface.

## AI API Used

This application uses the **[Groq API](https://groq.com/)** with the **`llama-3.3-70b-versatile`** model.

### Why Groq and Llama-3.3-70B?

- **Groq API:** Delivers exceptional speed through its LPU (Language Processing Unit) inference engine, providing extremely low latency for near-instantaneous dashboard generation. This ensures a responsive user experience.

- **Llama-3.3-70B Model:** A powerful 70-billion-parameter large language model that understands complex instructions and generates high-quality, well-structured HTML and CSS. Its versatility handles a wide variety of data formats and user requirements.

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Groq API Key (get one at [console.groq.com](https://console.groq.com))

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd instant-dashboard-app
```

### 2. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install dependencies:
```bash
uv sync
```

Create a `.env` file in the `backend` directory:
```bash
cp .env.example .env
```

Add your Groq API key to `.env`:
```
GROQ_API_KEY=your-groq-api-key-here
```

### 3. Run the Backend
```bash
uv run python main.py
```

The backend server will start at `http://localhost:8000`.

### 4. Run the Frontend

simply open `frontend/index.html` directly in your browser.

### 5. Access the Application

- **Frontend Interface:** https://instant-dashboard-app.vercel.app/
- **API Documentation:** https://instant-dashboard-app.onrender.com/docs
- **Health Check:** https://instant-dashboard-app.onrender.com/health

## Running with Docker

### Backend Only

Navigate to the backend directory:
```bash
cd backend
```

Build the image:
```bash
docker build -t instant-dashboard-backend .
```

Run the container:
```bash
docker run -p 8000:8000 -e GROQ_API_KEY=your-key-here instant-dashboard-backend
```

Or use an environment file:
```bash
docker run -p 8000:8000 --env-file .env instant-dashboard-backend
```




## Features

- ✨ Generate professional HTML dashboards from JSON data
- ⚡ Fast response times powered by Groq's LPU
- 🎨 Customizable outputs via natural language prompts
- ✅ Built-in JSON validation
- 🏥 Health check endpoint
- 📚 Interactive API documentation (Swagger UI)
- 🎯 Clean separation of frontend and backend

## Project Structure
```
.
├── backend/
│   ├── app/                # Application code
│   ├── main.py             # Application entry point
│   ├── pyproject.toml      # Python dependencies
│   ├── uv.lock             # Locked dependencies
│   ├── requirements.txt    # Pip requirements
│   └── Dockerfile          # Backend Docker configuration
├── frontend/
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── index.html          # Main HTML page
├── LICENSE                 # License file
└── README.md               # This file
```

## Development

### Backend Development
```bash
cd backend
uv sync
uv run python main.py
```

### Frontend Development

The frontend is a static web application. Any changes to HTML, CSS, or JavaScript files will be reflected immediately when you refresh the browser.

## Support

For issues or questions, please open an issue in the repository.