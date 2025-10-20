from anthropic import Anthropic

from lib.CONSTANTS import ANTHROPIC_API_KEY

class AnthropicDetails:
        """
        Returns Anthropic Client & provides Model details
        """
        def __init__(self, ):
              self.API_KEY=ANTHROPIC_API_KEY
        
        def anthropic_client(self, ) -> Anthropic:
              return Anthropic(
                    api_key=self.API_KEY
              )
        
        def claude_sonnet_latest(self, ) -> str:
            client = self.anthropic_client()
            latest_model = client.models.list()
            claude_sonnet_models = []
            for model in latest_model:
                if 'claude-sonnet' in model.id:
                    claude_sonnet_models.append(model.id)
            return str(claude_sonnet_models[0])