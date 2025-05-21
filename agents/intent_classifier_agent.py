from agents.base_agent import BaseAgent
import re
import logging
import json
import os
from typing import Dict, List, Pattern
from dotenv import load_dotenv

# Try to import OpenAI for optional AI-powered classification
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class IntentClassifierAgent(BaseAgent):
    """
    Agent responsible for classifying the intent of user messages.
    
    Can use either rule-based classification with regex patterns or
    OpenAI's API for more advanced classification if configured.
    """
    
    def __init__(self):
        super().__init__(name="Intent Classifier Agent")
        
        # Initialize OpenAI client if API key is available
        self.openai_client = None
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI()
            logger.info("OpenAI client initialized for intent classification")
        
        # Define comprehensive intent patterns for rule-based classification
        self.intent_patterns: Dict[str, List[Pattern]] = {
            "greeting": [
                re.compile(r"^(hi|hello|hey|greetings|howdy|hola)", re.IGNORECASE),
                re.compile(r"^good (morning|afternoon|evening)", re.IGNORECASE)
            ],
            "farewell": [
                re.compile(r"^(bye|goodbye|see you|cya|farewell)", re.IGNORECASE),
                re.compile(r"^take care", re.IGNORECASE)
            ],
            "help": [
                re.compile(r"help( me)?", re.IGNORECASE),
                re.compile(r"how (can|do) I", re.IGNORECASE),
                re.compile(r"support", re.IGNORECASE)
            ],
            "account": [
                re.compile(r"(my )?account", re.IGNORECASE),
                re.compile(r"(sign|log) ?in", re.IGNORECASE),
                re.compile(r"password", re.IGNORECASE),
                re.compile(r"login", re.IGNORECASE),
                re.compile(r"profile", re.IGNORECASE),
                re.compile(r"reset.*password", re.IGNORECASE),
                re.compile(r"forgot.*password", re.IGNORECASE),
                re.compile(r"change.*password", re.IGNORECASE),
                re.compile(r"cant.*login", re.IGNORECASE)
            ],
            "order": [
                re.compile(r"(my )?(order|purchase)", re.IGNORECASE),
                re.compile(r"(track|cancel|modify).*order", re.IGNORECASE),
                re.compile(r"shipping", re.IGNORECASE),
                re.compile(r"delivery", re.IGNORECASE),
                re.compile(r"where.*order", re.IGNORECASE),
                re.compile(r"order.*status", re.IGNORECASE)
            ],
            "product": [
                re.compile(r"product", re.IGNORECASE),
                re.compile(r"(item|goods)", re.IGNORECASE),
                re.compile(r"(availability|in stock)", re.IGNORECASE),
                re.compile(r"specifications?", re.IGNORECASE),
                re.compile(r"features?", re.IGNORECASE),
                re.compile(r"how.*work", re.IGNORECASE),
                re.compile(r"warranty", re.IGNORECASE)
            ],
            "complaint": [
                re.compile(r"(complaint|dissatisfied|unhappy)", re.IGNORECASE),
                re.compile(r"(bad|poor) (service|experience)", re.IGNORECASE),
                re.compile(r"(not working|broken|damaged|defective)", re.IGNORECASE),
                re.compile(r"issue.*with", re.IGNORECASE),
                re.compile(r"problem.*with", re.IGNORECASE),
                re.compile(r"doesnt.*work", re.IGNORECASE),
                re.compile(r"faulty", re.IGNORECASE)
            ],
            "urgent": [
                re.compile(r"(urgent|emergency|immediately|asap)", re.IGNORECASE),
                re.compile(r"(critical|crucial)", re.IGNORECASE),
                re.compile(r"need.*now", re.IGNORECASE)
            ],
            "faq": [
                re.compile(r"(what|where|when|who|how|why)", re.IGNORECASE),
                re.compile(r"can you tell me", re.IGNORECASE),
                re.compile(r"explain", re.IGNORECASE),
                re.compile(r"info about", re.IGNORECASE),
                re.compile(r"\?$")
            ]
        }

    async def process(self, message: str, **kwargs):
        """
        Classify the intent of the user's message.
        
        Args:
            message: The user's message
            
        Returns:
            str: The classified intent
        """
        self._log_processing(message)
        
        # Try AI classification if available
        if self.openai_client:
            try:
                ai_intent = await self._classify_with_ai(message)
                if ai_intent:
                    logger.info(f"AI classified intent as: {ai_intent}")
                    return ai_intent
            except Exception as e:
                logger.warning(f"Error using AI classification: {str(e)}. Falling back to rule-based.")
        
        # Fall back to rule-based classification
        intent = self._classify_with_rules(message)
        logger.info(f"Rule-based classified intent as: {intent}")
        return intent
    
    async def _classify_with_ai(self, message: str) -> str:
        """
        Classify intent using OpenAI's API
        
        Args:
            message: The user's message
            
        Returns:
            str: The classified intent or None if classification failed
        """
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """
                    You are an intent classifier for a customer support system.
                    Classify the user message into exactly one of these categories:
                    - greeting: General greetings
                    - farewell: Saying goodbye
                    - help: Asking for general help
                    - account: Questions about user accounts, login, passwords
                    - order: Order-related inquiries
                    - product: Product-related inquiries
                    - complaint: Customer complaints about products/service
                    - urgent: Urgent issues requiring immediate attention
                    - faq: General questions
                    - other: None of the above
                    
                    Respond with ONLY the category name, nothing else.
                    """},
                    {"role": "user", "content": message}
                ],
                temperature=0.1
            )
            
            intent = response.choices[0].message.content.strip().lower()
            
            # Validate the intent is one we recognize
            if intent in self.intent_patterns or intent == "other":
                return intent
            
            logger.warning(f"AI returned unrecognized intent: {intent}")
            return None
            
        except Exception as e:
            logger.error(f"Error in AI intent classification: {str(e)}")
            return None
    
    def _classify_with_rules(self, message: str) -> str:
        """
        Classify intent using rule-based approach with regex patterns
        
        Args:
            message: The user's message
            
        Returns:
            str: The classified intent
        """
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern.search(message):
                    return intent
        
        # Default intent if no patterns match
        return "other"
