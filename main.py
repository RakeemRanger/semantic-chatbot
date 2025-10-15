import asyncio
import os

from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.anthropic import (
    AnthropicChatCompletion,
    AnthropicChatPromptExecutionSettings
)

model = "claude-sonnet-4-5"
api_key = os.getenv("ANTHROPIC_API_KEY")

async def chat_with_ai() -> str:
    bot = AnthropicChatCompletion(
        ai_model_id=model,
        api_key=api_key
    )
    kernel = Kernel()
    chat_history = ChatHistory()
    execution_setting = AnthropicChatPromptExecutionSettings()
    kernel.add_service(bot)
    try:
        while True:
            user_input = input("user:")
            if user_input.lower in ["exit", "quit"]:
                break
            chat_history.add_user_message(user_input)
            response = await bot.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_setting
            )
            print(f"Assistant: {response}")
            chat_history.add_assistant_message(str(response))
    except Exception as e:
        print(f"Issue starting Chat Bot: {e}")


def main():
    asyncio.run(chat_with_ai())

if __name__ == "__main__":
    main()
