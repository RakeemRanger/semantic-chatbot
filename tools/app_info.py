from semantic_kernel.functions import kernel_function

class AppName:
    @kernel_function(
        description="AI chatbot info"
    )
    async def app() -> str:
        return "Dartinbot"