from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn

from database import SessionLocal, engine, Base
from models.chat import Message, Conversation
from models.ticket import Ticket
from agents.intent_classifier_agent import IntentClassifierAgent
from agents.routing_agent import RoutingAgent
from agents.support_agent import SupportAgent
from agents.notify_agent import NotifyAgent
from schemas.chat import MessageCreate, MessageResponse, ConversationResponse
from schemas.ticket import TicketCreate, TicketResponse
import logging

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="AI Multi-Agent Chat Support System")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize agents
intent_classifier = IntentClassifierAgent()
router = RoutingAgent()
support_agent = SupportAgent()
notify_agent = NotifyAgent()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    """
    Process chat messages through the multi-agent system
    
    1. Classify the intent of the message
    2. Route to the appropriate agent
    3. Generate a response
    4. Notify if needed
    5. Return the response
    """
    try:
        logger.info(f"Received message: {message.content}")
        
        # Create or get conversation
        conversation = db.query(Conversation).filter(
            Conversation.id == message.conversation_id
        ).first() if message.conversation_id else None
        
        if not conversation:
            conversation = Conversation()
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Save user message
        user_message = Message(
            content=message.content,
            is_user=True,
            conversation_id=conversation.id
        )
        db.add(user_message)
        db.commit()
        
        # Process with agent system
        intent = await intent_classifier.process(message.content)
        logger.info(f"Classified intent: {intent}")
        
        target_agent = await router.route(intent, message.content)
        logger.info(f"Routed to agent: {target_agent.__class__.__name__}")
        
        response_content = await support_agent.generate_response(target_agent, message.content, intent)
        logger.info(f"Generated response: {response_content}")
        
        # Save agent response
        agent_message = Message(
            content=response_content,
            is_user=False,
            conversation_id=conversation.id
        )
        db.add(agent_message)
        db.commit()
        db.refresh(agent_message)
        
        # Notify if needed (asynchronously without waiting)
        if intent in ["complaint", "urgent"]:
            await notify_agent.send_notification(
                message.content, 
                response_content,
                intent
            )
        
        return MessageResponse(
            id=agent_message.id,
            content=agent_message.content,
            conversation_id=conversation.id,
            timestamp=agent_message.timestamp,
            is_user=False
        )
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.post("/api/tickets", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """Create a new support ticket"""
    db_ticket = Ticket(
        subject=ticket.subject,
        description=ticket.description,
        priority=ticket.priority,
        status="open"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # Notify about new ticket
    await notify_agent.send_notification(
        f"New ticket created: {ticket.subject}",
        ticket.description,
        "ticket_created"
    )
    
    return db_ticket

@app.get("/api/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get all messages in a conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return ConversationResponse(
        id=conversation.id,
        messages=[
            MessageResponse(
                id=msg.id,
                content=msg.content,
                conversation_id=msg.conversation_id,
                timestamp=msg.timestamp,
                is_user=msg.is_user
            ) for msg in messages
        ],
        created_at=conversation.created_at
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
