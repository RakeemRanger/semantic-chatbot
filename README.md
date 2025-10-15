# Semantic Kernel Chat Bot with Claude

A simple chatbot implementation using Microsoft's Semantic Kernel and Anthropic's Claude AI model.

## Features
- 🔄 Asynchronous chat implementation
- 🤖 Integration with Claude Sonnet 4.5 model
- 💬 Chat history management
- ❌ Clean exit handling

## Prerequisites
- Python 3.8+
- Anthropic API key
- Required Python packages:
  ```
  semantic-kernel
  asyncio
  ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install semantic-kernel
   ```

4. **Set up environment variables:**
   ```bash
   # Linux/Mac
   export ANTHROPIC_API_KEY='your-api-key-here'
   
   # Windows
   set ANTHROPIC_API_KEY=your-api-key-here
   ```

## Usage

Run the script:
```bash
python semantic.py
```

Example interaction:
```
user: Hello!
Assistant: Hi! How can I help you today?
user: exit
```

## Code Structure

### Main Components
```python
import asyncio
import os

from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.anthropic import (
    AnthropicChatCompletion,
    AnthropicChatPromptExecutionSettings
)
```

### Core Functions

#### `chat_with_ai()`
```python
async def chat_with_ai() -> str:
    bot = AnthropicChatCompletion(
        ai_model_id=model,
        api_key=api_key
    )
    # ... chat loop implementation
```

#### `main()`
```python
def main():
    asyncio.run(chat_with_ai())
```

### Important Classes
- `Kernel`: Core Semantic Kernel class
- `ChatHistory`: Maintains conversation context
- `AnthropicChatCompletion`: Handles Claude model integration
- `AnthropicChatPromptExecutionSettings`: Configures chat completion settings

## Error Handling
```python
try:
    # Chat operations
except:
    raise Exception("Error")
```

## Directory Structure
```
project/
├── src/
│   └── semantic.py
├── README.md
├── requirements.txt
└── .env.example
```

## Environment Variables
```env
ANTHROPIC_API_KEY=your-api-key-here
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

## To-Do
- [ ] Add proper error handling with specific exceptions
- [ ] Implement chat history persistence
- [ ] Add configuration file support
- [ ] Create test suite
- [ ] Add conversation context management
- [ ] Implement model parameter customization

## Support
For support, please open an issue in the GitHub repository.

---
*This project uses the Semantic Kernel framework and Anthropic's Claude AI model. Please ensure you comply with all relevant terms of service and licensing requirements.*
