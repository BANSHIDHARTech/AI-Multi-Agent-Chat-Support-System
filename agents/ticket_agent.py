from agents.base_agent import BaseAgent
import logging
from datetime import datetime
from typing import Dict, Optional, Any
import json
import os

logger = logging.getLogger(__name__)

class TicketAgent(BaseAgent):
    """
    Agent that handles support ticket creation and management.
    """
    
    def __init__(self):
        super().__init__(name="Ticket Agent")
        
        # In-memory ticket store
        self.tickets = {}
        self.next_ticket_id = 1
        
        # Load ticket templates for responses
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """Load response templates from file if available, otherwise use defaults"""
        try:
            if os.path.exists("data/ticket_templates.json"):
                with open("data/ticket_templates.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading ticket templates: {str(e)}. Using defaults.")
        
        # Default templates
        return {
            "created": "I've created a support ticket for you. Your ticket number is #{ticket_id}. Our support team will review it shortly.",
            "urgent": "I've created an URGENT support ticket for you. Your ticket number is #{ticket_id}. Our support team has been notified and will prioritize this issue.",
            "updated": "Your ticket #{ticket_id} has been updated with your new information.",
            "generic": "I'll need to create a support ticket to help with this issue. Could you briefly describe the problem you're experiencing?",
            "confirmation": "Thank you for providing that information. I'll create a support ticket for this issue. Is there anything else you'd like to add?"
        }
    
    async def process(self, message: str, **kwargs):
        """
        Process ticket-related queries and create/update tickets.
        
        Args:
            message: The user's message
            **kwargs: Additional parameters including intent
            
        Returns:
            str: Response to the user
        """
        intent = kwargs.get("intent", "")
        self._log_processing(message, {"intent": intent})
        
        # For demonstration purposes, we'll create a ticket
        # In a real system, this would interact with the database
        ticket_id = self._create_ticket(
            subject=f"Support request: {message[:30]}...",
            description=message,
            priority="high" if intent == "urgent" else "medium"
        )
        
        # Return the appropriate response
        if intent == "urgent":
            return self.templates["urgent"].replace("{ticket_id}", str(ticket_id))
        else:
            return self.templates["created"].replace("{ticket_id}", str(ticket_id))
    
    def _create_ticket(self, subject: str, description: str, priority: str) -> int:
        """
        Create a new ticket in the in-memory store.
        
        Args:
            subject: The ticket subject
            description: The ticket description
            priority: The ticket priority
            
        Returns:
            int: The ID of the created ticket
        """
        ticket_id = self.next_ticket_id
        self.next_ticket_id += 1
        
        self.tickets[ticket_id] = {
            "id": ticket_id,
            "subject": subject,
            "description": description,
            "status": "open",
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "updated_at": None
        }
        
        logger.info(f"Created ticket #{ticket_id}: {subject}")
        return ticket_id
        
    def _update_ticket(self, ticket_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing ticket.
        
        Args:
            ticket_id: The ID of the ticket to update
            updates: Dictionary of fields to update
            
        Returns:
            Optional[Dict]: The updated ticket or None if not found
        """
        if ticket_id not in self.tickets:
            logger.warning(f"Attempted to update non-existent ticket #{ticket_id}")
            return None
            
        ticket = self.tickets[ticket_id]
        
        for key, value in updates.items():
            if key in ticket:
                ticket[key] = value
                
        ticket["updated_at"] = datetime.now().isoformat()
        logger.info(f"Updated ticket #{ticket_id}")
        
        return ticket
