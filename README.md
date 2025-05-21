# AI Multi-Agent Chat Support System

This project is a proof-of-concept (PoC) for an automated customer support system using a modular, multi-agent architecture. It demonstrates how different AI agents can work together to classify user intents, route messages to specialized agents, generate responses, and send notifications.

## Architecture Overview

![Architecture Diagram](https://i.imgur.com/iJVhygq.png)

The system follows this workflow:

1. User sends a query to the FastAPI `/api/chat` endpoint
2. `IntentClassifierAgent` classifies the intent using rule-based logic or OpenAI API
3. `RoutingAgent` routes the query to one of:
   - `FAQAgent` (for static answers)
   - `TicketAgent` (for creating support tickets)
   - `AccountAgent` (for account-related queries)
4. `SupportAgent` processes the response
5. `NotifyAgent` sends updates via mock notifications (simulated)

## Key Features

- **Modular Architecture**: Each agent has a specific role and can be updated independently
- **Intent Classification**: Rule-based with optional OpenAI API enhancement
- **Dynamic Routing**: Messages are routed to specialized agents based on intent
- **Ticket Management**: Support tickets are created and stored in SQLite
- **Conversation History**: All messages are stored in a database
- **Notification System**: Simulated notifications for urgent issues
- **Simple Chat UI**: Browser-based interface for testing

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-multi-agent-chat.git
   cd ai-multi-agent-chat
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. (Optional) Set up environment variables by creating a `.env` file:
   ```
   # .env
   OPENAI_API_KEY=your_openai_api_key  # Optional, for AI-based intent classification
   DATABASE_URL=sqlite:///./chat_support.db
   ```

5. Run the application:
   ```
   python main.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## API Usage

### Chat Endpoint

```
POST /api/chat
```

Request body:
```json
{
  "content": "I need help with my account",
  "conversation_id": null  // Optional, omit for new conversation
}
```

Response:
```json
{
  "id": 2,
  "content": "I can help you with your account. What specific information are you looking for?",
  "conversation_id": 1,
  "timestamp": "2023-10-25T14:30:45.123456",
  "is_user": false
}
```

### Create Ticket Endpoint

```
POST /api/tickets
```

Request body:
```json
{
  "subject": "Account access issue",
  "description": "I can't log into my account after the recent update",
  "priority": "high"
}
```

Response:
```json
{
  "id": 1,
  "subject": "Account access issue",
  "description": "I can't log into my account after the recent update",
  "status": "open",
  "priority": "high",
  "created_at": "2023-10-25T14:35:23.123456",
  "updated_at": null
}
```

### Get Conversation History

```
GET /api/conversations/{conversation_id}
```

Response:
```json
{
  "id": 1,
  "messages": [
    {
      "id": 1,
      "content": "I need help with my account",
      "conversation_id": 1,
      "timestamp": "2023-10-25T14:30:30.123456",
      "is_user": true
    },
    {
      "id": 2,
      "content": "I can help you with your account. What specific information are you looking for?",
      "conversation_id": 1,
      "timestamp": "2023-10-25T14:30:45.123456",
      "is_user": false
    }
  ],
  "created_at": "2023-10-25T14:30:30.123456"
}
```

## Folder Structure

```
multi_agent_support/
├── agents/                 # Agent modules
│   ├── base_agent.py       # Abstract base class for all agents
│   ├── intent_classifier_agent.py
│   ├── routing_agent.py
│   ├── faq_agent.py
│   ├── ticket_agent.py
│   ├── account_agent.py
│   ├── support_agent.py
│   └── notify_agent.py
├── data/                   # Static data files
│   └── faqs.json
├── models/                 # Database models
│   ├── chat.py
│   └── ticket.py
├── schemas/                # Pydantic schemas for validation
│   ├── chat.py
│   └── ticket.py
├── static/                 # Static assets
│   └── style.css
├── templates/              # HTML templates
│   └── index.html
├── utils/                  # Utility functions
│   ├── prompt_templates.py
│   └── error_handling.py
├── database.py             # Database connection and setup
├── main.py                 # FastAPI application
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Extending the System

### Adding a New Agent

1. Create a new file in the `agents/` directory (e.g., `my_new_agent.py`)
2. Extend the `BaseAgent` class and implement the `process` method
3. Register the agent in the `RoutingAgent` if needed

Example:
```python
from agents.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="My New Agent")
        
    async def process(self, message: str, **kwargs):
        self._log_processing(message)
        # Implement your agent logic here
        return "Response from my new agent"
```

### Adding New Intents

To add new intents to the classifier:

1. Open `agents/intent_classifier_agent.py`
2. Add new patterns to the `intent_patterns` dictionary

Example:
```python
self.intent_patterns = {
    # ... existing patterns
    "new_intent": [
        re.compile(r"keyword1", re.IGNORECASE),
        re.compile(r"keyword2", re.IGNORECASE)
    ]
}
```

3. Update the routing in `agents/routing_agent.py` to route the new intent to the appropriate agent

## License

This project is licensed under the MIT License - see the LICENSE file for details.