from agents.base_agent import BaseAgent
import logging
import json
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class AccountAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Account Agent")

    async def process(self, message: str, **kwargs) -> str:
        """
        Return mock responses for account-related queries.
        """
        message = message.lower()
        if "balance" in message:
            return "Your current account balance is ₹1,250.00."
        elif "email" in message:
            return "Your registered email is user@example.com."
        elif "reset password" in message or "change password" in message or "password" in message:
            return "To reset your password, click 'Forgot Password' on the login page and follow the instructions."
        elif "update" in message or "change" in message:
            return "You can update your account details from your profile settings."
        else:
            return "I can help you with balance, email, password reset, or updating your account. Please tell me what you want to do."
    
    def __init__(self):
        super().__init__(name="Account Agent")
        
        # Load mock account data
        self.accounts = self._load_mock_accounts()
        self.response_templates = self._load_templates()
        
    def _load_mock_accounts(self) -> Dict[str, Dict]:
        """Load mock account data from file if available, otherwise use defaults"""
        try:
            if os.path.exists("data/mock_accounts.json"):
                with open("data/mock_accounts.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading mock accounts: {str(e)}. Using defaults.")
        
        # Default mock accounts
        return {
            "user1": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "plan": "Premium",
                "status": "Active",
                "last_login": "2023-10-15T14:30:00"
            },
            "user2": {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "plan": "Basic",
                "status": "Active",
                "last_login": "2023-10-18T09:15:00"
            },
            "demo": {
                "name": "Demo User",
                "email": "demo@example.com",
                "plan": "Free",
                "status": "Active",
                "last_login": "2023-10-20T11:45:00"
            }
        }
    
    def _load_templates(self) -> Dict[str, str]:
        """Load response templates"""
        try:
            if os.path.exists("data/account_templates.json"):
                with open("data/account_templates.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading account templates: {str(e)}. Using defaults.")
        
        # Default templates with improved responses
        return {
            "account_info": "Here are your account details:\nName: {name}\nEmail: {email}\nPlan: {plan}\nStatus: {status}\nLast Login: {last_login}",
            "not_logged_in": "You'll need to log in to access your account information. You can log in at example.com/login. If you've forgotten your password, I can help you reset it.",
            "password_reset": "I've sent a password reset link to your email address. Please check your inbox (and spam folder) and follow the instructions. The link will expire in 24 hours for security.",
            "password_help": "To reset your password:\n1. Go to example.com/login\n2. Click 'Forgot Password'\n3. Enter your email address\n4. Follow the instructions in the reset email\n\nNeed more help? Just let me know!",
            "login_help": "To log in:\n1. Visit example.com/login\n2. Enter your email and password\n3. Click 'Sign In'\n\nIf you've forgotten your password, I can help you reset it. Would you like to do that?",
            "account_locked": "Your account has been temporarily locked for security. This usually happens after multiple incorrect password attempts. Wait 30 minutes and try again, or I can help you reset your password.",
            "generic": "I can help you with your account. What would you like to know about? I can help with:\n- Account information\n- Password reset\n- Login issues\n- Account settings\n- Subscription/plan details"
        }
