# 🤖 SmartAgent — Azure AI Travel Agent

A production-grade AI agent portfolio project built with **Django REST Framework**, **Azure OpenAI**, and a clean dark frontend.

## ✨ Features

- 🧠 **AI Agent** with real tool calling via Azure OpenAI
- 🔧 **5 Tools** — flights, hotels, weather, booking, destination info
- 💾 **Persistent Sessions** — chat history saved to SQLite database
- 🌐 **REST API** — clean DRF endpoints for all operations
- 💬 **Chat UI** — dark minimal frontend with sidebar suggestions
- 🔐 **Azure CLI Auth** — secure credential handling

## 🛠️ Tech Stack

| Layer    | Technology                  |
|----------|-----------------------------|
| Backend  | Django 5 + Django REST Framework |
| AI       | Azure OpenAI (gpt-5.4-nano) |
| Auth     | Azure CLI Credential        |
| Database | SQLite                      |
| Frontend | Vanilla HTML/CSS/JS         |
| Language | Python 3.12                 |

## 📁 Project Structure

```
smartagent/
├── smartagent/         # Django project settings
├── agent/
│   ├── models.py       # ChatSession + Message models
│   ├── views.py        # REST API + page views
│   ├── tools.py        # 5 AI tools + schemas
│   ├── serializers.py  # DRF serializers
│   ├── urls.py         # URL routing
│   └── templates/      # Frontend HTML
├── manage.py
├── requirements.txt
└── .env.example
```

## 🚀 Setup

### 1. Clone
```bash
git clone https://github.com/yourusername/smartagent
cd smartagent
```

### 2. Virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment variables
```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

### 5. Azure login
```bash
az login
```

### 6. Run
```bash
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/chat/` | Send message to agent |
| GET    | `/api/session/<id>/` | Get chat history |
| DELETE | `/api/session/<id>/clear/` | Clear session |
| GET    | `/api/health/` | Health check |

### Example API call
```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Find flights from Sydney to Tokyo", "session_id": "test123"}'
```

## 🤖 Available Tools

| Tool | Description |
|------|-------------|
| `search_flights` | Search flights between cities |
| `search_hotels` | Find hotels at destination |
| `get_weather` | Current weather for any city |
| `book_flight` | Book a flight with confirmation |
| `get_destination_info` | Visa, currency, travel tips |

## 📸 Screenshots

- **Home page** — Landing with tools and API docs
- **Chat page** — Dark minimal chat with sidebar

---

Built by **Golam Fahad Mullick** | Azure AI Developer
