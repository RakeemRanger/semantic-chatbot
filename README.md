# AI-Powered Project Scaffold Generator 🚀

> An intelligent project scaffolding application powered by Microsoft Semantic Kernel and Claude Sonnet 4.5. Automatically generates complete, production-ready project structures with AI-driven code generation, GitHub integration, and intelligent change detection.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Semantic Kernel](https://img.shields.io/badge/Semantic%20Kernel-Latest-purple)](https://github.com/microsoft/semantic-kernel)
[![Claude Sonnet 4.5](https://img.shields.io/badge/Claude-Sonnet%204.5-orange)](https://www.anthropic.com/claude)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)](https://streamlit.io/)

## 🎯 What is This?

This is an **AI-powered project scaffold generator** that creates complete, production-ready applications through natural language conversations. Simply describe what you want to build, and the AI generates:

- 📁 Complete project structure with proper organization
- 💻 Production-ready code files (app logic, APIs, services)
- 🧪 Comprehensive test suites
- 📝 Documentation (README, setup guides, API docs)
- 🐳 Docker configurations and docker-compose
- ⚙️ Configuration files (.env, settings, logging)
- 🔧 CI/CD pipeline templates
- 🐙 Automatic GitHub repository creation
- 🔀 Feature branch workflow with pull requests
- 🗄️ Database schemas and migrations
- 🌐 Frontend components (if applicable)

## ✨ Key Features

### 🤖 AI-Powered Generation
- **Claude Sonnet 4.5 Integration** - State-of-the-art code generation
- **Streaming API** - Real-time progress updates for large projects
- **Intelligent File Generation** - Context-aware, production-ready code
- **Multi-Language Support** - Python, JavaScript, TypeScript, Go, Rust, and more
- **Framework Awareness** - FastAPI, Flask, React, Next.js, Express, Django, etc.

### 🎨 Dual Interface
- **CLI Mode** - Terminal-based interaction for developers
- **Web UI** - Beautiful Streamlit interface for teams
- **Chat Interface** - Natural language project creation
- **File Preview** - See generated files before committing

### 🐙 GitHub Integration
- **Auto Repository Creation** - Creates GitHub repos automatically
- **Feature Branch Workflow** - Updates create branches + PRs (never commit to main)
- **Change Detection** - Tracks local and remote modifications
- **Intelligent Commit Messages** - AI-generated, descriptive commits
- **PR Management** - Detailed pull request descriptions with change summaries

### 🗄️ Project Database
- **Persistent Memory** - Tracks all generated projects across sessions
- **UUID-based Tracking** - Unique identifiers for each project
- **Metadata Storage** - Commit history, PR details, file snapshots
- **Search & Filter** - Find projects by name, description, repository
- **JSON Storage** - Simple, portable database format at `~/.dartinbot/projects/projects_db.json`

### 🔍 Change Detection System
- **Local Changes** - Detects modifications by users or other tools
- **GitHub Changes** - Tracks commits and remote updates
- **Sync Status** - Compares local vs remote state
- **Snapshot System** - SHA256-based baseline tracking for reliability
- **Multi-Agent Aware** - Knows when other tools modify projects
- **Detailed Reports** - Shows added/modified/deleted files with timestamps

### 📦 Project Management
- **Create Projects** - Generate complete applications from scratch
- **Update Projects** - AI-powered incremental updates (adds features intelligently)
- **Delete Projects** - Clean up local files and/or GitHub repos
- **List Projects** - View all tracked projects with details
- **Project Info** - Get detailed context about any project
- **Detect Changes** - Check what changed locally or on GitHub

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Available Commands](#available-commands)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔧 Prerequisites

- **Python 3.8+** (3.12 recommended)
- **Anthropic API Key** - [Get one here](https://console.anthropic.com/)
- **GitHub Personal Access Token** - [Generate here](https://github.com/settings/tokens)
  - Required permissions: `repo` (Full control), `workflow`
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

Create a `.env` file in the project root:

```bash
# Required - Anthropic API for Claude
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Required - GitHub for repository management  
GITHUB_ACCESS_TOKEN=your-github-token-here
```

Or export them directly:
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
export GITHUB_ACCESS_TOKEN='your-github-token-here'
```

### 5. Verify Installation
```bash
python -c "import semantic_kernel; print('✓ Semantic Kernel installed')"
python -c "import streamlit; print('✓ Streamlit installed')"
python -c "import anthropic; print('✓ Anthropic installed')"
python -c "from tools.project_db import get_db; print('✓ Project database ready')"
```

## 🎯 Quick Start

### CLI Mode (Terminal)

```bash
# Run the AI chatbot
python -m main
```

You'll see:
```
🤖 Semantic Kernel Chatbot with Claude (Type 'exit' or 'quit' to end)
User: _
```

Type your project request and press Enter!

### Web UI Mode (Streamlit)

```bash
# Launch Streamlit interface
streamlit run app.py

# Or use the launch script (Linux/Mac)
./run_web.sh
```

The web interface will open at `http://localhost:8501`

## 💡 Usage Examples

### Example 1: Create a FastAPI Weather API

**User Request:**
```
Create a FastAPI application for a weather API with timezone information, 
5-day forecasts, and humorous weather messages. Include caching, error 
handling, Docker support, and comprehensive tests. Name it weather-api-app
```

**What Gets Generated:**
```
weather-api-app/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   └── v1/
│   │       ├── weather.py      # Weather endpoints
│   │       ├── timezone.py     # Timezone endpoints
│   │       └── combined.py     # Combined endpoints
│   ├── services/
│   │   ├── weather_client.py   # External API client
│   │   ├── weather_messages.py # Humor generator
│   │   └── cache.py            # Caching service
│   ├── schemas/
│   │   ├── weather.py          # Pydantic models
│   │   └── timezone.py
│   └── core/
│       ├── config.py           # Settings
│       └── logging_config.py
├── tests/
│   ├── api/
│   │   ├── test_weather.py
│   │   └── test_timezone.py
│   └── services/
│       └── test_weather_messages.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── pytest.ini
```

**Result:**
- ✅ 38 files created
- ✅ GitHub repository created
- ✅ Initial commit pushed
- ✅ Project added to database
- ✅ Ready to run with `uvicorn app.main:app`

### Example 2: Update an Existing Project

**User Request:**
```
Update timezone-weather-api to add authentication using JWT tokens
```

**What Happens:**
1. AI analyzes existing project structure
2. Generates authentication middleware
3. Adds JWT token generation/validation
4. Updates endpoints with `@require_auth` decorators
5. Adds authentication tests
6. Updates README with auth documentation
7. Creates feature branch `feature/add-jwt-authentication`
8. Opens pull request with detailed description
9. Updates project snapshot

**Result:**
```
Pull Request #5: Add JWT Authentication
- Modified: 8 files
- Added: 4 files
- Deleted: 0 files
Branch: feature/add-jwt-authentication-1729456789
```

### Example 3: Detect Changes

**User Request:**
```
Check what changed in my weather-api-app
```

**Response:**
```
🔍 CHANGE DETECTION REPORT
============================================================

Project: weather-api-app
Status: Changes detected locally (not on GitHub yet)

📁 LOCAL CHANGES (since last snapshot):
- Added: 2 files
- Modified: 3 files
- Deleted: 0 files

  Modified Files:
    - app/main.py (changed at 2025-10-20T15:33:09)
    - README.md (changed at 2025-10-20T15:30:15)
    - requirements.txt (changed at 2025-10-20T15:28:42)

  Added Files:
    - app/middleware/auth.py (1234 bytes)
    - tests/test_auth.py (567 bytes)

🔄 SYNC STATUS:
- In sync: ❌ No
- Only local: 2 files (not pushed to GitHub)
============================================================
```

### Example 4: Create a React + TypeScript App

**User Request:**
```
Create a React app with TypeScript, Tailwind CSS, and React Router. 
Include a dashboard with charts, user authentication flow, and API 
integration. Use Vite for building. Name it dashboard-app
```

**What Gets Generated:**
- Complete TypeScript React application
- Vite configuration
- Tailwind CSS setup
- React Router setup
- Authentication components (Login, Register, ProtectedRoute)
- Dashboard with sample charts
- API service layer with Axios
- TypeScript types and interfaces
- ESLint and Prettier config
- Package.json with all dependencies
- README with setup instructions

### Example 5: List All Projects

**User Request:**
```
List all my projects
```

**Response:**
```
You have 3 active project(s):

**timezone-weather-api** (UUID: 8012cb68...)
  - Repository: timezone-weather-api
  - Location: /home/user/.dartinbot/projects/timezone-weather-api
  - Description: Production-ready FastAPI application...
  - Created: 2025-10-20T20:54:21
  - URL: https://github.com/RakeemRanger/timezone-weather-api

**bls-data-semantic-kernel** (UUID: 7a91bc54...)
  - Repository: bls-data-semantic-kernel
  - Location: /home/user/.dartinbot/projects/bls-data-semantic-kernel
  - Description: Streamlit application with Semantic Kernel...
  - Created: 2025-10-20T19:22:15
  - URL: https://github.com/RakeemRanger/bls-data-semantic-kernel

**dashboard-app** (UUID: 6f8de423...)
  - Repository: dashboard-app
  - Location: /home/user/.dartinbot/projects/dashboard-app
  - Description: React TypeScript dashboard with charts...
  - Created: 2025-10-20T18:10:33
  - URL: https://github.com/RakeemRanger/dashboard-app
```

## 🎮 Available Commands

The AI understands natural language, so you can phrase requests however you like!

### Project Creation
- "Create a [type] application for [purpose] with [features]. Name it [name]"
- "Build me a [framework] app that does [description]"
- "Generate a [language] project with [requirements]"

### Project Updates
- "Update [project-name] to add [feature]"
- "Modify [project-name] to include [changes]"
- "Add [feature] to my [project-name] project"

### Project Management
- "List all my projects"
- "List my repos" / "Show my GitHub repositories"
- "Tell me about [project-name]"
- "Get info on [project-name]"
- "Delete [project-name]" (deletes local and/or remote)

### Change Detection
- "Check what changed in [project-name]"
- "Detect changes in [project-name]"
- "Has [project-name] been modified?"
- "Update snapshot for [project-name]"

## 🏗️ Project Structure

```
semantic-chatbot/
├── main.py                     # CLI entry point
├── app.py                      # Streamlit web UI
├── run_web.sh                  # Launch script
├── requirements.txt            # Dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                 # Git ignore patterns
├── README.md                   # This file
│
├── tools/                      # AI Tools & Plugins
│   ├── scaffold_generator.py  # Project scaffold generator
│   ├── source_control.py       # GitHub integration
│   ├── project_db.py           # Project database
│   ├── change_detector.py      # Change detection system
│   └── prompts/
│       └── scaffoldPrompt.md   # Scaffold generation prompt
│
├── lib/                        # Core libraries
│   ├── claude_details.py       # Claude API client
│   ├── log_client.py           # Logging configuration
│   └── CONSTANTS.py            # Constants and paths
│
├── plugins/                    # Semantic Kernel plugins
│   ├── TimeTools.py            # Time/date functions
│   └── AppInfo.py              # App metadata
│
├── .streamlit/                 # Streamlit configuration
│   └── config.toml             # Custom theme
│
├── logs/                       # Application logs
│   └── tools.source_control.log
│
└── tests/                      # Test files
    ├── test_project_db.py
    ├── test_change_detection.py
    └── ...
```

### Generated Projects Location

All generated projects are stored in:
```
~/.dartinbot/projects/
├── project-name-1/
├── project-name-2/
├── project-name-3/
└── projects_db.json           # Project database
```

## 🔧 How It Works

### 1. Project Creation Flow

```
User Request
    ↓
Semantic Kernel
    ↓
Claude Sonnet 4.5 (Streaming API)
    ↓
JSON Scaffold Generation
    {
      "project_name": "...",
      "folders": [...],
      "files": [
        {
          "path": "...",
          "content": "..."
        }
      ]
    }
    ↓
File System Creation
    ↓
GitHub Repository Creation
    ↓
Git Commit & Push
    ↓
Database Entry (UUID, metadata)
    ↓
File Snapshot (SHA256 hashes)
    ↓
Success Response
```

### 2. Project Update Flow

```
Update Request
    ↓
Get Project from Database
    ↓
Load Existing Files
    ↓
Claude Analyzes + Generates Changes
    {
      "summary": "...",
      "changes": [
        {
          "path": "...",
          "action": "modify|add|delete",
          "content": "..."
        }
      ]
    }
    ↓
Apply Changes Locally
    ↓
Create Feature Branch
    ↓
Commit to Feature Branch
    ↓
Create Pull Request
    ↓
Update Database + Snapshot
    ↓
Return PR URL
```

### 3. Change Detection Flow

```
detect_project_changes()
    ↓
Load Last Snapshot from DB
    ↓
Scan Current Local Files
    ↓
Compute SHA256 Hashes
    ↓
Compare to Snapshot
    ↓
Query GitHub API
    ↓
Get Recent Commits
    ↓
Compare Local vs GitHub
    ↓
Generate Report
    - Local changes
    - GitHub commits
    - Sync status
    ↓
Return to User
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key for Claude |
| `GITHUB_ACCESS_TOKEN` | Yes | GitHub PAT with `repo` and `workflow` permissions |

### Streamlit Configuration

Located in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
headless = true
port = 8501
```

### Project Database Location

Default: `~/.dartinbot/projects/projects_db.json`

Can be customized in `tools/project_db.py`:
```python
db = ProjectDatabase(db_path="/custom/path/projects_db.json")
```

## 📚 Documentation

Comprehensive documentation is available in the `/docs` folder:

- **[PROJECT_DATABASE.md](PROJECT_DATABASE.md)** - Project database system guide
- **[CHANGE_DETECTION.md](CHANGE_DETECTION.md)** - Change detection system docs
- **[SCAFFOLD_GUIDE.md](SCAFFOLD_GUIDE.md)** - Scaffold generation guide
- **[SCAFFOLD_IMPLEMENTATION.md](SCAFFOLD_IMPLEMENTATION.md)** - Implementation details

## 🐛 Troubleshooting

### Issue: "Repository creation failed. name already exists"

**Solution:** The project database will now automatically detect existing repos and reuse them instead of trying to create duplicates.

### Issue: Changes not detected

**Solution:** Run `update_project_snapshot(repo_name)` to update the baseline snapshot.

### Issue: PR creation failed

**Solution:** Check that your GitHub PAT has the `repo` and `workflow` permissions. Regenerate if needed.

### Issue: Anthropic API errors

**Solution:** 
- Verify your API key is correct
- Check your API usage/credits
- Ensure you have access to Claude Sonnet 4.5

### Issue: Streaming timeout

**Solution:** For very large projects (100+ files), the streaming may take >10 minutes. This is normal. The system uses Claude's streaming API specifically for this.

### Issue: "Project not found in database"

**Solution:** The project might have been created outside the system. Use the scaffold generator to create projects so they're tracked properly.

## 🎁 Example Projects You Can Create

Here are some ideas:

1. **REST APIs**
   - FastAPI weather service
   - Express.js todo API
   - Django blog backend
   - Flask machine learning API

2. **Web Applications**
   - React dashboard
   - Next.js e-commerce site
   - Vue.js admin panel
   - Streamlit data app

3. **Data Science**
   - Jupyter notebook project
   - Pandas data pipeline
   - Scikit-learn model training
   - TensorFlow inference service

4. **DevOps**
   - Docker-based microservices
   - Kubernetes deployment configs
   - CI/CD pipeline templates
   - Infrastructure as Code (Terraform)

5. **Specialized**
   - Discord bot
   - Slack bot
   - Chrome extension
   - CLI tool

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Microsoft Semantic Kernel** - AI orchestration framework
- **Anthropic Claude** - State-of-the-art language model
- **Streamlit** - Beautiful web UI framework
- **PyGithub** - GitHub API integration

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/RakeemRanger/semantic-chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RakeemRanger/semantic-chatbot/discussions)
- **Email**: [Your Email]

---

**Built with ❤️ using Semantic Kernel and Claude Sonnet 4.5**
