# Semantic Kernel Chatbot with Claude 🤖

> An intelligent chatbot powered by Microsoft's Semantic Kernel framework and Anthropic's Claude AI, featuring automatic function calling and extensible plugin architecture.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Semantic Kernel](https://img.shields.io/badge/Semantic%20Kernel-Latest-purple)](https://github.com/microsoft/semantic-kernel)
[![Claude Sonnet 4.5](https://img.shields.io/badge/Claude-Sonnet%204.5-orange)](https://www.anthropic.com/claude)

## ✨ Features

- 🔄 **Asynchronous Architecture** - Non-blocking I/O for responsive interactions
- 🤖 **Claude Sonnet 4.5 Integration** - State-of-the-art AI model from Anthropic
- 💬 **Persistent Chat History** - Maintains context across conversation turns
- 🛠️ **Automatic Function Calling** - AI autonomously invokes tools when needed
- ⏰ **Time Intelligence** - Real-time date and time information
- 🐙 **GitHub Integration** - List and create repositories via natural language
- � **App Info Plugin** - Application metadata and information
- �🔌 **Extensible Plugin System** - Easy-to-add custom tools and capabilities
- 🔒 **Secure by Default** - Environment-based secrets management

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Available Plugins](#available-plugins)
- [Creating Custom Plugins](#creating-custom-plugins)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔧 Prerequisites

- **Python 3.8+** (3.12 recommended)
- **Anthropic API Key** - [Get one here](https://console.anthropic.com/)
- **GitHub Personal Access Token** (optional, for GitHub features) - [Generate here](https://github.com/settings/tokens)
- Git (for cloning the repository)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/RakeemRanger/semantic-chatbot.git
cd semantic-chatbot
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv semanticvenv

# Activate it
source semanticvenv/bin/activate  # Linux/macOS
# OR
.\semanticvenv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (or export directly):

```bash
# Required
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'

# Optional (for GitHub features)
export GITHUB_ACCESS_TOKEN='your-github-token-here'
```

**Windows Users:**
```cmd
set ANTHROPIC_API_KEY=your-anthropic-api-key-here
set GITHUB_ACCESS_TOKEN=your-github-token-here
```

### 5. Verify Installation
```bash
python -c "import semantic_kernel; print('✓ Semantic Kernel installed')"
```

## 🎯 Quick Start

```bash
# Run the chatbot
python main.py
```

Type your questions and press Enter. Type `exit` or `quit` to stop.

## 💡 Usage Examples

### General Conversation
```
User: Hello! What can you help me with?
Assistant: Hi! I can help you with various tasks including checking the current time, 
managing your GitHub repositories, and answering questions. What would you like to do?
```

### Time Queries
```
User: What time is it?
Assistant: The current time is 2:30 PM on October 17, 2025.
```

### GitHub Repository Management

**List Repositories:**
```
User: can you list all my repos
Assistant: You have the following GitHub repositories:

- **semantic-chatbot**
- **dartinbot-framework-qa**
- **chancetheman**
```

**Create New Repository:**
```
User: can you create a repo named chancetheman and the repo is about a football app
Assistant: Great! I've successfully created the GitHub repository "chancetheman" for 
your football app project. The repository is now set up and ready for you to start 
adding your code and files.
```

### Complex Queries
The AI automatically determines which functions to call based on your request:

```
User: What's the current time and can you also show me my GitHub repos?
Assistant: The current time is 3:45 PM on October 17, 2025.

You have 3 GitHub repositories:
- semantic-chatbot
- dartinbot-framework-qa  
- chancetheman
```

## 🔌 Available Plugins

### Built-in Plugins

| Plugin | Description | Functions |
|--------|-------------|-----------|
| **TimePlugin** | Semantic Kernel's core time plugin | Get current date/time, timezone info |
| **Time** | Custom time utilities | Enhanced time formatting |
| **ProjectSourceControl** | GitHub integration | `list_repos()`, `create_repo()` |
| **AppInfo** | Application metadata | Returns "Dartinbot" app name |

### ProjectSourceControl Functions

#### `list_repos()`
Lists all repositories for the authenticated GitHub user.

**Returns:** String with repository names

**Example:**
```python
@kernel_function(description="list all user Github Repositories")
async def list_repos(self) -> str:
    user = self.gh_client.get_user()
    for repo in user.get_repos():
        return repo.name
```

#### `create_repo(repo_name: str, project_description: str)`
Creates a new GitHub repository for the authenticated user.

**Parameters:**
- `repo_name` (str): Name of the new repository
- `project_description` (str): Description of the repository purpose

**Returns:** String with repository name or error message

**Example:**
```python
@kernel_function(description="Create Github Repo")  
async def create_repo(self, repo_name: str, project_description: str) -> str:
    user = self.gh_client.get_user()
    try:
        new_repo = user.create_repo(
            name=repo_name,
            description=project_description
        )
        return new_repo.name
    except Exception as e:
        return f"Error: Unable to create github repo: {e}"
```

### Time Plugin Functions

#### `get_time()`
Returns the current date and time.

**Example:**
```python
@kernel_function(description="Get current date and time")
async def get_time() -> datetime.datetime.now:
    return datetime.datetime.now()
```

### AppInfo Plugin Functions

#### `app()`
Returns the application name.

**Returns:** "Dartinbot"

**Example:**
```python
@kernel_function(description="AI chatbot info")
async def app() -> str:
    return "Dartinbot"
```

## 🛠️ Creating Custom Plugins

### Step 1: Create Plugin Class

Create a new file in `tools/` directory:

```python
# tools/my_plugin.py
from semantic_kernel.functions import kernel_function

class MyPlugin:
    """
    Description of your plugin
    """
    
    def __init__(self):
        # Initialize any resources
        pass
    
    @kernel_function(description="Clear description of what this function does")
    async def my_function(self, param1: str, param2: int) -> str:
        """
        Function docstring
        
        Args:
            param1: Description of parameter 1
            param2: Description of parameter 2
            
        Returns:
            Result description
        """
        # Your implementation
        return f"Result: {param1} {param2}"
```

### Step 2: Register Plugin

Add to `main.py`:

```python
from tools.my_plugin import MyPlugin

# In chat_with_ai() function:
kernel.add_plugin(MyPlugin(), "MyPluginName")
```

### Step 3: Test

The AI will automatically discover and use your plugin:

```
User: Can you use my function with test and 42?
Assistant: Result: test 42
```

### Best Practices

✅ **DO:**
- Use descriptive function names
- Provide clear descriptions in `@kernel_function`
- Add type hints for parameters
- Handle exceptions gracefully
- Return informative error messages
- Instantiate classes with `()` when adding to kernel

❌ **DON'T:**
- Use vague descriptions
- Skip type annotations
- Forget error handling
- Return sensitive information in plain text
- Add class without instantiating: `kernel.add_plugin(MyPlugin)` ❌

## 📁 Project Structure

```
semantic-chatbot/
├── 📄 main.py                    # Main chatbot entry point
│
├── 📂 tools/                     # Custom plugins directory
│   ├── get_time.py              # Time utilities plugin
│   ├── app_info.py              # Application information ("Dartinbot")
│   └── project_scaffold.py      # GitHub integration (list/create repos)
│
├── 📂 semanticvenv/             # Virtual environment (gitignored)
│
├── 📄 requirements.txt          # Python dependencies
├── 📄 .gitignore                # Git ignore patterns
├── 📄 .env                      # Environment variables (gitignored)
└── 📄 README.md                 # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Interactive chatbot with automatic function calling |
| `tools/get_time.py` | Custom time plugin returning current datetime |
| `tools/project_scaffold.py` | GitHub API integration for repo management |
| `tools/app_info.py` | Returns application name "Dartinbot" |

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | Your Anthropic API key for Claude access |
| `GITHUB_ACCESS_TOKEN` | ⚠️ Optional | GitHub Personal Access Token for repo features |

### Getting Your API Keys

#### Anthropic API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save securely

#### GitHub Personal Access Token
1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a descriptive name (e.g., "Semantic Chatbot")
4. Select scopes:
   - ✅ `repo` - Full control of private repositories
   - ✅ `read:user` - Read user profile data
5. Click **"Generate token"**
6. **Copy immediately** (you won't see it again!)
7. Set as environment variable

### Model Configuration

In `main.py`, you can customize the AI model:

```python
anthropc_model = "claude-sonnet-4-5"  # Current model

# Other options:
# - "claude-3-5-sonnet-20241022"
# - "claude-3-opus-20240229"
# - "claude-3-haiku-20240307"
```

### Execution Settings

Customize AI behavior in your code:

```python
settings = AnthropicChatPromptExecutionSettings(
    function_choice_behavior=FunctionChoiceBehavior.Auto(),
    max_tokens=4096,           # Maximum response length
    temperature=0.7,           # Creativity (0.0-1.0)
    top_p=0.9,                # Nucleus sampling
)
```

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

## 🔍 How It Works

### Architecture Overview

```
User Input
    ↓
Chat History ←──────┐
    ↓               │
Semantic Kernel     │
    ├── AI Service (Claude)
    ├── Plugins Registry
    │   ├── TimePlugin
    │   ├── ProjectSourceControl
    │   └── Custom Tools
    ↓               │
Function Calling    │
    ├── Auto-detect needed functions
    ├── Invoke functions
    ├── Collect results
    ↓               │
Response Generation │
    └───────────────┘
```

### Execution Flow

1. **Initialize Kernel**
   ```python
   kernel = Kernel()
   kernel.add_service(AnthropicChatCompletion(...))
   
   # Add all plugins
   kernel.add_plugin(Time(), "TimeTools")
   kernel.add_plugin(AppName(), "AppInfo")
   kernel.add_plugin(ProjectSourceControl(), "ProjectSourceControl")
   ```

2. **Configure Function Calling**
   ```python
   settings = AnthropicChatPromptExecutionSettings(
       function_choice_behavior=FunctionChoiceBehavior.Auto()
   )
   ```

3. **User Input** → Chat history updated

4. **AI Analysis** → Claude decides if functions are needed

5. **Function Execution** → Semantic Kernel invokes tools automatically

6. **Response Synthesis** → Claude formulates answer using function results

### Key Concepts

#### Function Choice Behavior
Controls how AI selects functions:
- **Auto()**: AI decides when to use functions
- **Required()**: AI must use at least one function
- **None()**: AI cannot use functions (dry run)

#### Kernel Parameter
**Critical**: Must pass kernel to enable function calling:
```python
response = await chat_completion.get_chat_message_content(
    chat_history=history,
    settings=settings,
    kernel=kernel,  # ← Required!
)
```

Without `kernel`, Claude won't know about available functions!

## 🐛 Troubleshooting

### Common Issues

#### Issue: "I don't have access to real-time information"

**Symptoms:** AI says it can't access time or other functions

**Solutions:**
1. ✅ Verify `FunctionChoiceBehavior.Auto()` is set:
   ```python
   settings = AnthropicChatPromptExecutionSettings(
       function_choice_behavior=FunctionChoiceBehavior.Auto()
   )
   ```

2. ✅ Ensure kernel is passed to chat completion:
   ```python
   response = await chat_completion.get_chat_message_content(
       chat_history=history,
       settings=settings,
       kernel=kernel,  # Must include this!
   )
   ```

3. ✅ Verify plugins are registered:
   ```python
   kernel.add_plugin(Time(), "TimeTools")  # Note the () !
   ```

---

#### Issue: `TypeError: 'NoneType' object has no attribute 'get_chat_message_content'`

**Cause:** `kernel.add_service()` returns `None`

**Solution:**
```python
# Wrong ❌
chat_completion = kernel.add_service(AnthropicChatCompletion(...))

# Correct ✅
kernel.add_service(AnthropicChatCompletion(...))
chat_completion = kernel.get_service(service_id="chat")
```

---

#### Issue: `missing 1 required positional argument: 'self'`

**Cause:** Passing class instead of instance

**Solution:**
```python
# Wrong ❌
kernel.add_plugin(ProjectSourceControl, "GitHubTools")

# Correct ✅
kernel.add_plugin(ProjectSourceControl(), "GitHubTools")
```

---

#### Issue: Second plugin overrides first one

**Cause:** Plugins need unique names

**Solution:**
```python
# Wrong ❌
kernel.add_plugin(Time())
kernel.add_plugin(AppName())  # Might override!

# Correct ✅
kernel.add_plugin(Time(), "TimeTools")
kernel.add_plugin(AppName(), "AppInfo")
```

---

#### Issue: GitHub functions not working

**Checks:**
1. ✅ `GITHUB_ACCESS_TOKEN` is set
2. ✅ Token has correct scopes (`repo`, `read:user`)
3. ✅ Token hasn't expired
4. ✅ Import uses correct Auth method:
   ```python
   from github.Auth import Token
   self.AUTH = Auth.Token(self.GITHUB_PAT)
   ```

---

### Debug Mode

Enable verbose logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("semantic_kernel")
```

### Getting Help

1. Check [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
2. Review [Anthropic API Docs](https://docs.anthropic.com/)
3. Open an [Issue on GitHub](https://github.com/RakeemRanger/semantic-chatbot/issues)

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m "feat: add amazing feature"`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Commit Convention
- `feat:` New feature
- `fix:` Bug fix  
- `docs:` Documentation
- `refactor:` Code refactoring

---

## 📝 Roadmap

### Completed ✅
- [x] Automatic function calling
- [x] Time plugin
- [x] GitHub integration (list & create repos)
- [x] Autonomous agent mode

### Planned 📅
- [ ] Chat history persistence
- [ ] Configuration file support
- [ ] Test suite (pytest)
- [ ] Additional plugins (weather, web search)
- [ ] Streaming responses
- [ ] Docker support

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**Third-Party:**
- Semantic Kernel - MIT
- Anthropic Python SDK - MIT  
- PyGithub - LGPL-3.0

---

## 🔒 Security

⚠️ **Never commit:**
- API keys
- Access tokens
- Passwords

✅ **Always use:**
- Environment variables
- `.gitignore` for sensitive files

Report security issues to: [security@example.com](mailto:security@example.com)

---

## 👏 Acknowledgments

- **Microsoft Semantic Kernel Team** - Amazing framework
- **Anthropic** - Claude AI and excellent API
- **GitHub** - PyGithub library
- **Open Source Community** - Inspiration and contributions

---

## 📧 Support

- 📖 [Documentation](https://github.com/RakeemRanger/semantic-chatbot/wiki)
- 🐛 [Bug Reports](https://github.com/RakeemRanger/semantic-chatbot/issues)
- 💬 [Discussions](https://github.com/RakeemRanger/semantic-chatbot/discussions)

---

<div align="center">

**Made with ❤️ using Semantic Kernel and Claude AI**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/RakeemRanger/semantic-chatbot/issues) · [Request Feature](https://github.com/RakeemRanger/semantic-chatbot/issues) · [Contribute](https://github.com/RakeemRanger/semantic-chatbot/pulls)

</div>
