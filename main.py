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
from tools.source_control import ProjectSourceControl
from tools.scaffold_generator import ProjectScaffold
from lib.claude_details import AnthropicDetails

async def chat_with_ai() -> str:
    anthropic_details = AnthropicDetails()
    anthropc_model = anthropic_details.claude_sonnet_latest()
    anthropic_api_key = anthropic_details.API_KEY
    kernel = Kernel()
    
    # Add the AI service
    kernel.add_service(
        AnthropicChatCompletion(
            ai_model_id=anthropc_model,
            api_key=anthropic_api_key,
            service_id="chat"
        )
    )
    
    # Add plugins with unique names (instantiate the classes with ())
    kernel.add_plugin(Time, "TimeTools")
    kernel.add_plugin(AppName(), "AppInfo")
    kernel.add_plugin(ProjectSourceControl(), "ProjectSourceControl")
    kernel.add_plugin(ProjectScaffold(), "ScaffoldGenerator")
    
    # Get the chat completion service from the kernel
    chat_completion = kernel.get_service(service_id="chat")
    
    # Enable function calling in the settings
    settings = AnthropicChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
        max_tokens=4096
    )
    
    history = ChatHistory()
    
    def clean_history():
        """Remove any messages with empty content from history"""
        cleaned_messages = []
        for msg in history.messages:
            if msg.content and str(msg.content).strip():
                cleaned_messages.append(msg)
        history.messages = cleaned_messages
    
    try:
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            history.add_user_message(user_input)
            
            # Clean history before making request
            clean_history()
            
            # Use get_chat_message_content with kernel to enable auto function calling
            response = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=settings,
                kernel=kernel,
            )
            
            # Only add non-empty responses to history
            response_text = str(response).strip()
            if response_text:
                print(f"Assistant: {response_text}")
                history.add_assistant_message(response_text)
            else:
                print("Assistant: [Task completed]")
            
            # Clean history after response
            clean_history()
    except Exception as e:
        print(f"Issue starting Chatbot: {e}")

def main():
    asyncio.run(chat_with_ai())

if __name__ == "__main__":
    main()
