from agents.base_agent import BaseAgent
import logging
import json
import os
from typing import Dict

logger = logging.getLogger(__name__)

class FAQAgent(BaseAgent):
    """
    Agent that handles frequently asked questions with predefined answers.
    """
    
    def __init__(self):
        super().__init__(name="FAQ Agent")
        
        # Load FAQ data from file or use default
        self.faqs = self._load_faqs()
        
    def _load_faqs(self) -> Dict[str, str]:
        """Load FAQ data from file if available, otherwise use defaults"""
        try:
            if os.path.exists("data/faqs.json"):
                with open("data/faqs.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading FAQs from file: {str(e)}. Using default FAQs.")
        
        return {
            "greeting": "Hello! Welcome to our support chat. How can I help you today?",
            "farewell": "Thank you for chatting with us. Have a great day!",
            "help": "I can help you with account issues, orders, product information, or creating support tickets. Just let me know what you need!",
            "business_hours": "Our support team is available Monday to Friday, 9 AM to 6 PM Eastern Time.",
            "shipping": "We typically ship orders within 1-2 business days. Standard delivery takes 3-5 business days...",
            "returns": "We accept returns within 30 days of purchase...",
            "warranty": "Our products come with a 1-year limited warranty...",
            "payment_methods": "We accept all major credit cards, PayPal, and Apple Pay.",
            "order_tracking": "Track your order by logging in or using your tracking number.",
            "cancel_order": "Orders can be cancelled within 1 hour. Contact support if later.",
            "product_availability": "Availability is shown on each product page. Sign up for alerts.",
            "contact": "Reach us at support@example.com or (555) 123-4567.",
            "default": "I understand you have a question. Could you please provide more details?"
        }

    async def process(self, message: str, **kwargs) -> str:
        """
        Match keywords from message to known FAQs and return the answer.
        """
        message = message.lower()
        for keyword, answer in self.faqs.items():
            if keyword in message:
                return answer
        return self.faqs.get("default", "Sorry, I couldn't find an answer for that.")

