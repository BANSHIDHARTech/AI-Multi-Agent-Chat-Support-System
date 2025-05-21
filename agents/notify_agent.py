from agents.base_agent import BaseAgent
import logging
import asyncio
from typing import Dict, Any, Optional
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class NotifyAgent(BaseAgent):
    """
    Agent that handles notifications via various channels (email, SMS, etc.)
    
    For this demonstration, notifications are just logged rather than actually sent.
    """
    
    def __init__(self):
        super().__init__(name="Notify Agent")
        
        # Track sent notifications
        self.notifications = []
        
        # Check for notification API credentials
        self.email_enabled = os.getenv("EMAIL_API_KEY") is not None
        self.sms_enabled = os.getenv("SMS_API_KEY") is not None
        
    async def process(self, message: str, **kwargs):
        """
        Process a notification request.
        
        Args:
            message: Notification message
            **kwargs: Additional parameters including notification_type
            
        Returns:
            bool: Whether the notification was sent successfully
        """
        notification_type = kwargs.get("notification_type", "info")
        recipient = kwargs.get("recipient", "support@example.com")
        
        self._log_processing(message, {"type": notification_type, "recipient": recipient})
        
        # Send the notification
        return await self.send_notification(message, recipient, notification_type)
    
    async def send_notification(self, message: str, recipient: str = "support@example.com", notification_type: str = "info") -> bool:
        """
        Send a notification.
        
        Args:
            message: The notification message
            recipient: The recipient address/number
            notification_type: The type of notification
            
        Returns:
            bool: Whether the notification was sent successfully
        """
        # Record the notification
        notification = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "recipient": recipient,
            "type": notification_type
        }
        
        self.notifications.append(notification)
        
        # Log the notification (in a real system, this would actually send it)
        logger.info(f"NOTIFICATION [{notification_type.upper()}] To: {recipient} - {message}")
        
        # Simulate different notification channels based on type
        if notification_type in ["urgent", "high"]:
            # Simulate SMS and email for urgent messages
            if self.sms_enabled:
                await self._mock_send_sms(recipient, message)
            if self.email_enabled:
                await self._mock_send_email(recipient, f"URGENT: {message}", "high")
            
            # Also notify in logs
            logger.warning(f"URGENT NOTIFICATION: {message}")
            
        elif notification_type in ["ticket_created", "complaint"]:
            # Simulate email for tickets and complaints
            if self.email_enabled:
                await self._mock_send_email(recipient, f"New {notification_type}: {message}", "medium")
        
        else:
            # Simulate email for other notifications
            if self.email_enabled:
                await self._mock_send_email(recipient, message, "low")
        
        return True
    
    async def _mock_send_email(self, recipient: str, message: str, priority: str) -> bool:
        """Mock sending an email (for demonstration)"""
        # In a real implementation, this would use SendGrid, AWS SES, etc.
        logger.info(f"MOCK EMAIL [{priority.upper()}] To: {recipient} - {message}")
        
        # Simulate network delay
        await asyncio.sleep(0.1)
        return True
    
    async def _mock_send_sms(self, recipient: str, message: str) -> bool:
        """Mock sending an SMS (for demonstration)"""
        # In a real implementation, this would use Twilio, etc.
        logger.info(f"MOCK SMS To: {recipient} - {message}")
        
        # Simulate network delay
        await asyncio.sleep(0.1)
        return True
    
    def get_notification_history(self, limit: int = 10) -> list:
        """
        Get recent notification history.
        
        Args:
            limit: Maximum number of notifications to return
            
        Returns:
            list: Recent notifications
        """
        return sorted(
            self.notifications,
            key=lambda x: x["timestamp"],
            reverse=True
        )[:limit]
