"""
Utility functions for generating prompts for AI-based agents.
"""

class PromptTemplates:
    """
    Class containing templates for various prompts used in the system.
    """
    
    @staticmethod
    def intent_classification_prompt(message: str) -> str:
        """
        Generate a prompt for intent classification.
        
        Args:
            message: The user's message
            
        Returns:
            str: The prompt for intent classification
        """
        return f"""
        You are an intent classifier for a customer support system.
        Classify the following user message into exactly one of these categories:
        - greeting: General greetings
        - farewell: Saying goodbye
        - help: Asking for general help
        - account: Questions about user accounts
        - order: Order-related inquiries
        - product: Product-related inquiries
        - complaint: Customer complaints
        - urgent: Urgent issues requiring immediate attention
        - faq: General questions
        - other: None of the above
        
        Respond with ONLY the category name, nothing else.
        
        User message: "{message}"
        """
    
    @staticmethod
    def faq_response_prompt(message: str, intent: str) -> str:
        """
        Generate a prompt for FAQ response generation.
        
        Args:
            message: The user's message
            intent: The classified intent
            
        Returns:
            str: The prompt for FAQ response generation
        """
        return f"""
        You are a helpful customer support assistant. The user has asked a question
        that has been classified as a '{intent}' intent.
        
        User message: "{message}"
        
        Please provide a concise, helpful, and friendly response to this question.
        Keep your answer under 150 words and focus on being informative and accurate.
        """
    
    @staticmethod
    def ticket_creation_prompt(message: str, intent: str) -> str:
        """
        Generate a prompt for ticket creation response.
        
        Args:
            message: The user's message
            intent: The classified intent
            
        Returns:
            str: The prompt for ticket creation response
        """
        priority = "urgent" if intent == "urgent" else "standard"
        
        return f"""
        You are creating a support ticket for a customer issue with {priority} priority.
        
        Customer message: "{message}"
        
        Generate a brief summary of the issue (max 50 characters) to use as the ticket subject.
        Then provide a detailed description of the issue based on the information provided.
        
        Format your response as:
        Subject: [Your subject here]
        Description: [Your description here]
        """
    
    @staticmethod
    def account_query_prompt(message: str) -> str:
        """
        Generate a prompt for account query response.
        
        Args:
            message: The user's message
            
        Returns:
            str: The prompt for account query response
        """
        return f"""
        You are a customer support assistant handling an account-related query.
        
        User query: "{message}"
        
        Provide a helpful response about their account. Since this is a demo,
        do not request or expose any real personal information. Instead, use
        placeholder/mock data where appropriate.
        
        Be professional, concise, and empathetic in your response.
        """
