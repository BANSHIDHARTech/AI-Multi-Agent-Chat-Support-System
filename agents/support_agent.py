from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class SupportAgent(BaseAgent):
    """
    Agent that coordinates responses from specialized agents and ensures
    they meet quality standards before returning to the user.
    """
    
    def __init__(self):
        super().__init__(name="Support Agent")
    
    async def process(self, message: str, **kwargs):
        """
        Process the message through the appropriate specialized agent.
        
        Args:
            message: The user's message
            **kwargs: Additional parameters including intent and agent
            
        Returns:
            str: The response to the user
        """
        intent = kwargs.get("intent", "other")
        agent = kwargs.get("agent", None)
        
        self._log_processing(message, {"intent": intent, "agent": agent.__class__.__name__ if agent else None})
        
        if agent:
            # Generate response from the specialized agent
            response = await agent.process(message, intent=intent)
            
            # Post-process the response if needed
            response = self._format_response(response, intent)
            
            return response
        else:
            # Fallback response if no agent is specified
            return "I'm not sure how to help with that. Could you try rephrasing your question?"
    
    async def generate_response(self, agent, message: str, intent: str):
        """
        Generate a response using the specified agent.
        
        Args:
            agent: The specialized agent to use
            message: The user's message
            intent: The classified intent
            
        Returns:
            str: The agent's response
        """
        response = await agent.process(message, intent=intent)
        return self._format_response(response, intent)
    
    def _format_response(self, response: str, intent: str) -> str:
        """
        Format and enhance the response based on the intent.
        
        Args:
            response: The raw response from the specialized agent
            intent: The intent of the user's message
            
        Returns:
            str: The formatted response
        """
        # Add appropriate prefixes or context based on intent
        if intent == "greeting":
            # No need to modify greeting responses
            return response
            
        if intent == "urgent":
            # Ensure urgent responses convey appropriate concern
            if "urgent" not in response.lower() and "priority" not in response.lower():
                return "I understand this is urgent. " + response
        
        if intent == "complaint":
            # Add empathy to complaint responses
            if "sorry" not in response.lower() and "apologize" not in response.lower():
                return "I'm sorry to hear about your experience. " + response
        
        # Add a closing line for certain responses
        if len(response) > 50 and not (intent in ["greeting", "farewell"]):
            if not response.endswith("?") and "anything else" not in response.lower():
                response += " Is there anything else I can help you with?"
        
        return response
