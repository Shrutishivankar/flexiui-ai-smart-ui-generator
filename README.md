# FlexiUI AI Smart UI Generator 🚀

An AI-powered smart UI generator that dynamically creates UI components based on user prompts. Built as a foundation for low-code/no-code website building platforms.

## Features

- 🤖 AI-based UI generation using natural language prompts
- 💬 Intelligent Q&A chatbot for design questions
- 🧩 Modular backend architecture with Flask & SQLite
- 🎨 Clean frontend structure with Bootstrap 5
- ⚡ Fast API-driven communication with Claude AI
- 💾 Database persistence for chat history
- 🔐 Session management for conversation context

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **AI:** Claude API (Anthropic)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5

## Project Structure
```
flexiui-chatbot/
│
├── backend/
│   ├── __pycache__/        # Python cache (ignored)
│   ├── instance/           # Flask instance folder (ignored)
│   ├── ai_service.py       # AI logic & UI generation
│   ├── app.py              # Main Flask backend
│   ├── models.py           # Data models / schemas
│   ├── prompts.py          # Prompt templates
│   ├── requirements.txt    # Backend dependencies
│   ├── test_env.py         # Environment testing script
│   └── test_import.py      # Import validation script
│
└── frontend/
    ├── assets/             # Static assets
    ├── app.js              # Frontend logic
    ├── index.html          # Main UI page
    └── style.css           # Styling
        
```

## Getting Started

### Prerequisites

- Python 3.8+
- Claude API key from [Anthropic Console](https://console.anthropic.com/)

### Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/FlexiUI_AI_Smart_UI_Generator.git
cd flexiui-chatbot
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file in project root
```env
CLAUDE_API_KEY=your-api-key-here
```

4. Run the application
```bash
python app.py
```

5. Open browser and navigate to
```
http://127.0.0.1:5000/chatbot
```

## Usage

### UI Generation Mode
```
"Create a landing page with navbar, hero section, and 3 feature cards"
"Design a contact form with email and message fields"
"Build a portfolio page with image gallery"
```

### Q&A Mode
```
"What is CSS Flexbox?"
"How do I make a responsive navbar?"
"Best practices for form design?"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chatbot` | GET | Chatbot interface page |
| `/api/chat` | POST | Send message to AI |
| `/api/chat/history` | GET | Get session chat history |
| `/api/chat/clear` | POST | Clear chat history |

### Example API Call
```javascript
fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: "Create a navbar" })
})
.then(res => res.json())
.then(data => {
    console.log(data.response);  // AI response
    console.log(data.intent);    // "UI_GENERATION" or "QUESTION"
});
```

## Database Schema

### ChatHistory Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_message | TEXT | User's input |
| bot_response | TEXT | AI's response |
| intent | VARCHAR(50) | Type of query |
| created_at | DATETIME | Timestamp |

## Environment Variables

Create a `.env` file:
```env
CLAUDE_API_KEY=your-claude-api-key-here
```

⚠️ **Never commit `.env` to version control**

## Development

Run in debug mode:
```bash
python app.py
```

## Future Enhancements

- [ ] Visual component preview
- [ ] Export generated UI as HTML/React
- [ ] Drag-and-drop UI editor integration
- [ ] Multi-user authentication
- [ ] Template library
- [ ] Voice input support
