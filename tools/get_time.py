import datetime

from semantic_kernel.functions import kernel_function

from lib.log_client import logClient

class Time:
    """
    Tools for AI
    """
    @kernel_function(
        description="Get current date and time"
    )
    async def get_time() -> datetime.datetime.now:
        """
        current date and time
        """
        logger = logClient(__name__)
        logger.info("Triggering Time LLM Function")
        return datetime.datetime.now()