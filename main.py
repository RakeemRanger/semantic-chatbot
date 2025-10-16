"""
Simple Semantic Kernel Chatbot with Anthropic integrations
"""
import asyncio
import os

from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.anthropic import (
    AnthropicChatCompletion,
    AnthropicChatPromptExecutionSettings
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.core_plugins.time_plugin import TimePlugin

from tools.get_time import Time
from tools.app_info import AppName

anthropc_model = "claude-sonnet-4-5"
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

async def chat_with_ai() -> str:
    kernel = Kernel()
    
    # Add the AI service
    kernel.add_service(
        AnthropicChatCompletion(
            ai_model_id=anthropc_model,
            api_key=anthropic_api_key,
            service_id="chat"
        )
    )
    
    # Add plugins with unique names
    kernel.add_plugin(Time, "TimeTools")
    kernel.add_plugin(AppName, "AppInfo")
    
    # Get the chat completion service from the kernel
    chat_completion = kernel.get_service(service_id="chat")
    
    # Enable function calling in the settings
    settings = AnthropicChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )
    
    history = ChatHistory()
    
    try:
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            history.add_user_message(user_input)
            
            # Use get_chat_message_content with kernel to enable auto function calling
            response = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=settings,
                kernel=kernel,
            )
            
            print(f"Assistant: {response}")
            history.add_assistant_message(str(response))
    except Exception as e:
        print(f"Issue starting Chatbot: {e}")

def main():
    asyncio.run(chat_with_ai())

if __name__ == "__main__":
    main()
