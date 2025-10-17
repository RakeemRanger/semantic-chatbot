# Semantic Kernel Chatbot with Claude

A chatbot implementation using Microsoft's Semantic Kernel framework with Anthropic's Claude AI model, featuring automatic function calling capabilities.

## Features
- 🔄 Asynchronous chat implementation
- 🤖 Integration with Claude Sonnet 4.5 model
- 💬 Persistent chat history management
- 🛠️ **Automatic function calling** with Semantic Kernel plugins
- ⏰ Time plugin for retrieving current date and time
- 🐙 GitHub integration for repository management (list & create repos)
- 🔌 Extensible plugin architecture for adding custom tools
- ❌ Clean exit handling

## Prerequisites
- Python 3.8+
- Anthropic API key
- Required Python packages (see `requirements.txt`)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RakeemRanger/semantic-chatbot.git
   cd semantic-chatbot
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv semanticvenv
   source semanticvenv/bin/activate  # Linux/Mac
   # or
   .\semanticvenv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Linux/Mac
   export ANTHROPIC_API_KEY='your-api-key-here'
   export GITHUB_ACCESS_TOKEN='your-github-token-here'  # For GitHub integration
   
   # Windows
   set ANTHROPIC_API_KEY=your-api-key-here
   set GITHUB_ACCESS_TOKEN=your-github-token-here
   ```

## Usage

Run the chatbot:
```bash
python main.py
# or
python chatter.py
```

Example interactions:
```
User: Hello!
Assistant: Hi! How can I help you today?

User: What time is it?
Assistant: The current time is 2:30 PM on October 17, 2025.

User: can you list all repos
Assistant: You have one GitHub repository:

- **dartinbot-framework-qa**

User: can you create a repo name chancetheman and the repo is about a football app
Assistant: Great! I've successfully created the GitHub repository "chancetheman" for your football app project. The repository is now set up and ready for you to start adding your code and files.

User: exit
```
Assistant: Hi! How can I help you today?

User: What time is it?
Assistant: The current time is 2:30 PM on October 15, 2025.

User: exit
```

## Code Structure

### Main Components
```python
from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.anthropic import (
    AnthropicChatCompletion,
    AnthropicChatPromptExecutionSettings
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.core_plugins.time_plugin import TimePlugin
```

### Core Functions

#### `chat_with_ai()`
The main async function that sets up the kernel, adds services and plugins, and manages the chat loop.

```python
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
    
    # Add plugins
    kernel.add_plugin(Time, "Time")
    
    # Get the chat completion service
    chat_completion = kernel.get_service(service_id="chat")
    
    # Enable automatic function calling
    settings = AnthropicChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )
    
    # Chat loop with function calling enabled
    response = await chat_completion.get_chat_message_content(
        chat_history=history,
        settings=settings,
        kernel=kernel,  # Required for function calling
    )
```

### Key Classes
- **`Kernel`**: Core Semantic Kernel orchestrator
- **`ChatHistory`**: Maintains conversation context across turns
- **`AnthropicChatCompletion`**: Handles Claude model integration
- **`AnthropicChatPromptExecutionSettings`**: Configures chat completion behavior
- **`FunctionChoiceBehavior`**: Enables automatic function/tool calling
- **`TimePlugin`**: Built-in plugin for time-related queries

## Function Calling / Plugins

This chatbot uses Semantic Kernel's automatic function calling feature, allowing Claude to automatically invoke functions when needed.

### Built-in Plugins
- **TimePlugin**: Provides current date and time information
- **ProjectSourceControl**: GitHub repository management
  - List user repositories
  - Create new repositories
  - Query repository information

### Custom Plugins
Custom tools are located in the `tools/` directory:

```python
# tools/get_time.py
from semantic_kernel.functions import kernel_function

class Time:
    @kernel_function(description="Get current date and time")
    async def get_time() -> datetime.datetime:
        return datetime.datetime.now()
```

```python
# tools/project_scaffold.py
from github import Github
from github.Auth import Token
from semantic_kernel.functions import kernel_function

class ProjectSourceControl:
    @kernel_function(description="list all user Github Repositories")
    async def list_repos(self):
        user = self.gh_client.get_user()
        return user.get_repos()
    
    @kernel_function(description="create a new Github Repository")
    async def create_repo(self, repo_name: str, description: str):
        user = self.gh_client.get_user()
        repo = user.create_repo(repo_name, description=description)
        return f"Repository '{repo_name}' created successfully!"
```

### Adding New Plugins
To add a new plugin:

1. Create a new class in the `tools/` directory
2. Decorate methods with `@kernel_function`
3. Add the plugin to the kernel in `main.py`:

```python
from tools.your_plugin import YourPlugin

kernel.add_plugin(YourPlugin, "PluginName")
```

The AI will automatically discover and use your functions when appropriate!

## Directory Structure
```
semantic-chatbot/
├── main.py              # Main chatbot implementation
├── chatter.py           # Alternative chatbot entry point
├── automain.py          # Autonomous agent version
├── tools/
│   ├── get_time.py      # Custom time tool
│   ├── app_info.py      # Application info plugin
│   ├── project_scaffold.py  # GitHub integration plugin
│   └── timetool.py      # Additional time utilities
├── semanticvenv/        # Virtual environment (gitignored)
├── README.md
├── requirements.txt
├── .gitignore
└── .git/
```

## Environment Variables
```env
ANTHROPIC_API_KEY=your-api-key-here
GITHUB_ACCESS_TOKEN=your-github-personal-access-token  # Required for GitHub features
```

### How to Get a GitHub Personal Access Token:
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (for repository access)
4. Copy the token and set it as an environment variable

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
[MIT License](LICENSE)

## Security Note
⚠️ **Important:** Never commit your API keys to version control. Always use environment variables for sensitive information.

## How It Works

1. **Kernel Setup**: Creates a Semantic Kernel instance and registers the AI service
2. **Plugin Registration**: Adds plugins (like TimePlugin) to the kernel
3. **Function Choice Behavior**: Configures automatic function calling with `FunctionChoiceBehavior.Auto()`
4. **Chat Loop**: 
   - Accepts user input
   - Sends message to Claude with available functions
   - Claude automatically decides when to call functions
   - Semantic Kernel invokes functions and returns results to Claude
   - Claude formulates final response using function results
5. **Response**: Displays Claude's answer to the user

## Key Configuration

### Enable Function Calling
```python
settings = AnthropicChatPromptExecutionSettings(
    function_choice_behavior=FunctionChoiceBehavior.Auto()
)
```

### Pass Kernel to Chat Completion
**Critical**: The kernel must be passed to enable function calling:
```python
response = await chat_completion.get_chat_message_content(
    chat_history=history,
    settings=settings,
    kernel=kernel,  # Required!
)
```

## Troubleshooting

### "I don't have access to real-time information"
- Ensure `FunctionChoiceBehavior.Auto()` is set in the settings
- Verify the kernel is passed to `get_chat_message_content()`
- Check that plugins are properly registered with `kernel.add_plugin()`

### NoneType Error
- Use `kernel.get_service(service_id="chat")` after adding the service
- Don't rely on the return value of `kernel.add_service()`

## To-Do
- [x] Implement automatic function calling
- [x] Add time plugin
- [ ] Add proper error handling with specific exceptions
- [ ] Implement chat history persistence to disk
- [ ] Add configuration file support
- [ ] Create test suite
- [ ] Add more custom plugins (weather, web search, etc.)
- [ ] Implement streaming responses
- [ ] Add model parameter customization (temperature, max tokens, etc.)

## Support
For support, please open an issue in the GitHub repository.

---
*This project uses the Semantic Kernel framework and Anthropic's Claude AI model. Please ensure you comply with all relevant terms of service and licensing requirements.*
