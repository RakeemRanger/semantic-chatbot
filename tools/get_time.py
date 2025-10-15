import datetime

from semantic_kernel.functions import kernel_function

class Time:
    """
    Tools for AI
    """
    @kernel_function(
        description="Get current dateand time"
    )
    async def get_time() -> datetime.datetime.now:
        """
        current date and time
        """
        return datetime.datetime.now()


