from agents.base_agent import BaseAgent
from agents.faq_agent import FAQAgent
from agents.ticket_agent import TicketAgent
from agents.account_agent import AccountAgent
import logging

logger = logging.getLogger(__name__)

class RoutingAgent(BaseAgent):
    """
    Agent responsible for routing messages to the appropriate specialized agent
    based on the classified intent.
    """
    
    def __init__(self):
        super().__init__(name="Routing Agent")
        
        # Initialize specialized agents
        self.faq_agent = FAQAgent()
        self.ticket_agent = TicketAgent()
        self.account_agent = AccountAgent()
        
        # Define routing rules
        self.routing_map = {
            "greeting": self.faq_agent,
            "farewell": self.faq_agent,
            "help": self.faq_agent,
            "faq": self.faq_agent,
            "account": self.account_agent,
            "complaint": self.ticket_agent,
            "urgent": self.ticket_agent,
            "order": self.ticket_agent,
            "product": self.faq_agent,
            "other": self.faq_agent
        }
    
    async def process(self, message: str, **kwargs):
        """
        Process the message by determining which agent should handle it.
        
        Args:
            message: The user's message
            **kwargs: Additional parameters, including intent
            
        Returns:
            The agent that should handle the message
        """
        intent = kwargs.get("intent", "other")
        self._log_processing(message, {"intent": intent})
        
        return await self.route(intent, message)
    
    async def route(self, intent: str, message: str):
        """
        Route the message to the appropriate agent based on intent.
        
        Args:
            intent: The classified intent
            message: The original message
            
        Returns:
            The agent that should handle the message
        """
        # Get the appropriate agent based on intent
        target_agent = self.routing_map.get(intent, self.faq_agent)
        
        logger.info(f"Routing message with intent '{intent}' to {target_agent.name}")
        
        return target_agent
