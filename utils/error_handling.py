"""
Utility functions for error handling throughout the system.
"""

import logging
import traceback
from typing import Dict, Any, Optional, Callable
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

class ErrorHandler:
    """
    Class for handling and logging errors throughout the system.
    """
    
    @staticmethod
    def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
        """
        Log an error with context information.
        
        Args:
            error: The exception that occurred
            context: Additional context information
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        if context:
            logger.error(
                f"Error: {error_type}: {error_message}. Context: {context}",
                exc_info=True
            )
        else:
            logger.error(f"Error: {error_type}: {error_message}", exc_info=True)
    
    @staticmethod
    def format_error_response(error: Exception) -> Dict[str, Any]:
        """
        Format an error for API response.
        
        Args:
            error: The exception that occurred
            
        Returns:
            Dict: Formatted error response
        """
        error_type = type(error).__name__
        
        return {
            "status": "error",
            "error_type": error_type,
            "message": str(error),
            "details": traceback.format_exc() if logger.level <= logging.DEBUG else None
        }
    
    @staticmethod
    def handle_agent_error(error: Exception, agent_name: str, fallback_response: str = None) -> str:
        """
        Handle errors from agents and provide fallback responses.
        
        Args:
            error: The exception that occurred
            agent_name: The name of the agent that raised the error
            fallback_response: Optional fallback response
            
        Returns:
            str: Fallback response
        """
        ErrorHandler.log_error(error, {"agent_name": agent_name})
        
        if fallback_response:
            return fallback_response
        
        # Default fallback responses by error type
        if isinstance(error, TimeoutError):
            return "I'm experiencing some delays. Could you please try again in a moment?"
        elif isinstance(error, ValueError):
            return "I couldn't process your request. Please check your input and try again."
        else:
            return "I encountered an issue while processing your request. Please try again or contact support if the problem persists."

def async_error_handler(fallback_response: Optional[str] = None):
    """
    Decorator for handling errors in async functions.
    
    Args:
        fallback_response: Optional fallback response
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Get agent name if available (assumes 'self' is first arg and has 'name' attribute)
                agent_name = getattr(args[0], 'name', 'Unknown') if args else 'Unknown'
                return ErrorHandler.handle_agent_error(e, agent_name, fallback_response)
        return wrapper
    return decorator

def sync_error_handler(fallback_response: Optional[str] = None):
    """
    Decorator for handling errors in sync functions.
    
    Args:
        fallback_response: Optional fallback response
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get agent name if available (assumes 'self' is first arg and has 'name' attribute)
                agent_name = getattr(args[0], 'name', 'Unknown') if args else 'Unknown'
                return ErrorHandler.handle_agent_error(e, agent_name, fallback_response)
        return wrapper
    return decorator
