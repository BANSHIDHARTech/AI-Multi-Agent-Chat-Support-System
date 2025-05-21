from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    
    All specialized agents should inherit from this class
    and implement the required abstract methods.
    """
    
    def __init__(self, name: str = "Base Agent"):
        self.name = name
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    async def process(self, message: str, **kwargs):
        """
        Process the incoming message and return a response.
        
        Args:
            message: The user's message
            **kwargs: Additional parameters specific to the agent
            
        Returns:
            The processed result
        """
        pass
    
    def _log_processing(self, message: str, context: dict = None):
        """Log the processing of a message with context"""
        if context:
            logger.info(f"{self.name} processing message: '{message}' with context: {context}")
        else:
            logger.info(f"{self.name} processing message: '{message}'")
