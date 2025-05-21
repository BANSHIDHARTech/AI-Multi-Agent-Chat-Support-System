# 🌐 AI Multi-Agent Chat Support System (PoC-2)

This project is a **Proof of Concept (PoC)** for a modular AI-driven customer support chat system. It showcases how multiple autonomous agents can collaboratively handle and route customer queries using a smart architecture powered by **FastAPI** and optional **LLM integration**.

---
## 🧠 Architecture Overview

### 🧩 Modular Multi-Agent Workflow

```text
                ┌────────────────────────┐
                │  User Chat Query Input │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │ IntentClassifierAgent  │
                └────────────┬───────────┘
                             ▼
                ┌────────────────────────┐
                │     RoutingAgent       │
                └────────┬─────┬─────────┘
                         │     │
       ┌─────────────────┘     └──────────────────┐
       ▼                                          ▼
┌───────────────┐                        ┌────────────────┐
│   FAQAgent    │                        │ TicketAgent    │
└──────┬────────┘                        └──────┬─────────┘
       ▼                                      ▼
┌───────────────┐                  ┌────────────────────┐
│ SupportAgent  │                  │   AccountAgent      │
└──────┬────────┘                  └────────────────────┘
       ▼
┌───────────────┐
│ NotifyAgent   │ (Email/WhatsApp via Twilio/SendGrid)
└───────────────┘


---
## 🚀 Features

- ✅ **Intent Classification**: Rule-based with OpenAI fallback  
- 🔀 **Dynamic Routing**: Automatically routes queries  
- 💡 **Specialized Agents**: For FAQ, ticketing, and account queries  
- 💾 **SQLite Support**: For chat and ticket logs  
- 📬 **Mock Notifications**: Via Twilio/SendGrid  
- ⚡ **FastAPI Backend**: Async, high-performance  
- 🧩 **Modular Design**: Easy to extend  
- 🖥️ **Swagger UI**: For live testing

---

## ⚙️ Setup Instructions

### 📋 Prerequisites

- Python 3.8+
- pip

### 🔧 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/cogniwide-multi-agent-chat-support.git
cd cogniwide-multi-agent-chat-support

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables (optional)
echo "OPENAI_API_KEY=your_openai_key" > .env
echo "DATABASE_URL=sqlite:///./chat_support.db" >> .env

# 5. Run the application
uvicorn main:app --reload
🌐 Access the Swagger UI
Open in your browser:
👉 http://localhost:8000/docs

🔌 API Usage
📥 POST /api/chat
Request

json

{
  "content": "I need help with my account",
  "conversation_id": null
}
Response

json
.

{
  "id": 2,
  "content": "I can help you with your account. What specific information are you looking for?",
  "conversation_id": 1,
  "timestamp": "2025-05-21T14:30:45",
  "is_user": false
}
🛠️ POST /api/tickets
Request

json


{
  "subject": "Can't login",
  "description": "Login page throws an error",
  "priority": "high"
}
Response

json


{
  "id": 1,
  "subject": "Can't login",
  "status": "open",
  "priority": "high",
  "created_at": "2025-05-21T15:00:00"
}
🧾 GET /api/conversations/{conversation_id}
Response

json


{
  "id": 1,
  "messages": [
    {
      "id": 1,
      "content": "I need help with my account",
      "is_user": true
    },
    {
      "id": 2,
      "content": "What specific info are you looking for?",
      "is_user": false
    }
  ]
}
📁 Folder Structure
pgsql


multi_agent_support/
├── agents/
│   ├── base_agent.py
│   ├── intent_classifier_agent.py
│   ├── routing_agent.py
│   ├── faq_agent.py
│   ├── ticket_agent.py
│   ├── account_agent.py
│   ├── support_agent.py
│   └── notify_agent.py
├── models/
│   ├── chat.py
│   └── ticket.py
├── schemas/
│   ├── chat.py
│   └── ticket.py
├── utils/
│   ├── prompt_templates.py
│   └── error_handling.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── database.py
├── main.py
├── requirements.txt
└── README.md
➕ Extending the System
🔧 Add a New Agent
python


# agents/my_custom_agent.py

from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    async def process(self, message: str, **kwargs):
        return "Response from MyCustomAgent"
Update routing_agent.py to include it.

🧠 Add New Intent
python


# agents/intent_classifier_agent.py

self.intent_patterns["refund_request"] = [
    re.compile(r"refund", re.IGNORECASE),
    re.compile(r"money back", re.IGNORECASE)
]
Update the routing in routing_agent.py.

📦 Technologies Used
Tool	                        Purpose
Python 3.8+	               Core language
FastAPI	                  API backend (async support)
SQLite	                  Local database
OpenAI API	               (Optional) Intent classification
Twilio/SendGrid	         (Mocked) Notifications
Uvicorn	                  ASGI Server
Pydantic	                  Data validation

💼 Final Notes
This project was built to demonstrate AI-first system design using a clean, modular architecture. It's fully extendable and makes a solid base for real-world AI support automation platforms.
## License

This project is licensed under the MIT License - see the LICENSE file for details.
