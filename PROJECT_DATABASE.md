# Project Database System

## Overview
The project database is a simple JSON-based system for tracking all projects created and managed by the semantic chatbot. It provides persistent memory across sessions and helps the LLM make intelligent decisions about project management.

## Purpose
- **Avoid Duplicate Repos**: Check if a project already exists before creating it
- **Persistent Memory**: Remember project details across chat sessions
- **Project Context**: Provide LLM with complete project information
- **Multiple Projects**: Track many projects with unique UUIDs
- **Update History**: Store metadata about updates, commits, and PRs

## Database Location
```
/home/nodebrite/semantic/.dartinbot/projects/projects_db.json
```

## Project Schema
Each project has the following structure:

```json
{
  "uuid": "abe21008-3d83-4bf5-acfc-02aff34f0086",
  "name": "My Project",
  "repo_name": "my-project-repo",
  "local_path": "/home/user/.dartinbot/projects/my-project",
  "description": "A cool project description",
  "repo_url": "https://github.com/user/my-project-repo",
  "created_at": "2025-10-20T20:50:00.439803",
  "updated_at": "2025-10-20T20:50:00.439831",
  "status": "active",
  "metadata": {
    "commit_sha": "abc123...",
    "branch": "main",
    "files_count": 12,
    "last_update": {
      "commit_sha": "def456...",
      "pr_number": 5,
      "pr_url": "https://github.com/user/repo/pull/5",
      "feature_branch": "feature/update-123",
      "summary": "Added new feature",
      "changes": {
        "modified": 3,
        "added": 2,
        "deleted": 1
      }
    }
  }
}
```

## LLM Functions
The following kernel functions are available for the LLM:

### 1. `list_projects()`
Lists all tracked projects with their details.

**Usage**: "Show me all my projects" or "What projects do I have?"

**Returns**: Formatted summary with UUID, name, repository, location, and status.

### 2. `get_project_info(repo_name: str)`
Gets detailed information about a specific project.

**Usage**: "Tell me about the bls-data-semantic-kernel project"

**Returns**: Complete project context including UUID, paths, metadata, and update history.

**Use Case**: Check if a project exists before creating it!

## Integration with Source Control

### On Project Creation (`commit_project`)
1. Creates GitHub repository (or uses existing)
2. Commits files to GitHub
3. **Adds project to database** with:
   - Generated UUID
   - Project name and repo name
   - Local path
   - Repository URL
   - Initial commit metadata

### On Project Update (`update_project`)
1. Gets existing project from database
2. Uses Claude AI to generate updates
3. Creates feature branch and PR
4. **Updates project metadata** with:
   - Last update timestamp
   - PR number and URL
   - Feature branch name
   - Change summary
   - File change counts

### On Project Delete (`delete_project`)
1. Deletes local files (optional)
2. Deletes GitHub repository (optional)
3. **Updates database**:
   - Soft delete (marks as "deleted") if partial
   - Hard delete (removes from DB) if complete

## Database API

### ProjectDatabase Class

```python
from tools.project_db import get_db

db = get_db()  # Get global instance
```

#### Methods

**Add Project**
```python
uuid = db.add_project(
    name="Project Name",
    repo_name="repo-name",
    local_path="/path/to/project",
    description="Description",
    repo_url="https://github.com/user/repo",
    additional_metadata={"key": "value"}
)
```

**Get Project**
```python
project = db.get_project(uuid)
project = db.get_project_by_name("Project Name")
project = db.get_project_by_repo("repo-name")
```

**List Projects**
```python
all_projects = db.list_all_projects()
active_projects = db.list_active_projects()
```

**Update Project**
```python
success = db.update_project(uuid, {
    "description": "New description",
    "metadata": {"new_key": "new_value"}
})
```

**Delete Project**
```python
# Soft delete (marks as deleted)
success = db.delete_project(uuid)

# Hard delete (removes from DB)
success = db.hard_delete_project(uuid)
```

**Search Projects**
```python
results = db.search_projects("search term")
```

**Get Summary for LLM**
```python
summary = db.get_summary()
print(summary)
# You have 3 active project(s):
# 
# **Project 1** (UUID: abc123...)
#   - Repository: project-1-repo
#   - Location: /path/to/project-1
#   ...
```

**Get Project Context for LLM**
```python
context = db.get_project_context("repo-name")
print(context)
# PROJECT CONTEXT:
# UUID: abc123...
# Name: Project Name
# Repository: repo-name
# ...
```

## Benefits

### 1. Prevents Duplicate Creation
Before creating a project, the LLM can check:
```python
project = db.get_project_by_repo("repo-name")
if project:
    print(f"Project already exists: {project['uuid']}")
```

### 2. Provides Context Across Sessions
The LLM can access project history even after restart:
```python
# User: "Update my bls project"
context = db.get_project_context("bls-data-semantic-kernel")
# LLM now knows the UUID, path, repo URL, last update, etc.
```

### 3. Tracks Multiple Projects
Each project has a unique UUID:
- `bls-data-semantic-kernel` → `abc123...`
- `semantic-chatbot` → `def456...`
- `test-project` → `ghi789...`

### 4. Stores Rich Metadata
Projects can store any additional data:
- Programming language
- Framework version
- Dependencies
- Last PR details
- Custom tags

### 5. Enables Intelligent Updates
The LLM can make decisions based on project history:
- "What was my last update?"
- "Show me projects updated this week"
- "Which projects have open PRs?"

## Example Workflow

### Creating a Project
```
User: Create a Flask web app for data analysis

LLM: 
1. Checks if project exists: get_project_info("flask-data-app")
2. Not found, proceeds with creation
3. Generates scaffold with Claude
4. Calls commit_project() 
5. Database automatically adds project with UUID
6. Returns: "Created project with UUID: abc123..."
```

### Updating a Project
```
User: Update my Flask app to add authentication

LLM:
1. Calls list_projects() to show available projects
2. Calls get_project_info("flask-data-app")
3. Gets context: UUID, local_path, repo_name
4. Calls update_project() with user query
5. Database automatically updates with PR details
6. Returns: "Created PR #5 for authentication feature"
```

### Checking Project Status
```
User: What projects do I have?

LLM: Calls list_projects()
Database returns:
You have 3 active project(s):

**Flask Data App** (UUID: abc123...)
  - Repository: flask-data-app
  - Location: /home/user/.dartinbot/projects/flask-data-app
  - Description: Web app for data analysis
  - Created: 2025-10-20T10:30:00
  - URL: https://github.com/user/flask-data-app
```

## Testing

Run the test script:
```bash
python3 test_project_db.py
```

This tests:
- Adding projects
- Getting projects by UUID/name/repo
- Updating projects
- Listing and searching
- Soft and hard deletion
- Database persistence

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Semantic Kernel                     │
│                  (LLM Orchestration)                    │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│ source_control.py│    │   project_db.py  │
│                  │    │                  │
│ - commit_project │◄──►│ - add_project    │
│ - update_project │    │ - get_project    │
│ - delete_project │    │ - update_project │
│ - list_repos     │    │ - list_projects  │
│ - list_projects  │    │ - search         │
│ - get_project_info│   │                  │
└────────┬─────────┘    └─────────┬────────┘
         │                        │
         ▼                        ▼
  ┌──────────────┐        ┌──────────────┐
  │   GitHub     │        │ projects_db  │
  │     API      │        │    .json     │
  └──────────────┘        └──────────────┘
```

## Future Enhancements

1. **Tags**: Add tagging system for categorizing projects
2. **Statistics**: Track metrics like update frequency, PR merge rate
3. **Backup**: Automatic backups of database file
4. **Search**: More advanced search with filters (by date, status, etc.)
5. **Export**: Export project list to CSV/JSON for reports
6. **Templates**: Store project templates for quick scaffolding
7. **Dependencies**: Track inter-project dependencies

## Conclusion

The project database provides the semantic chatbot with persistent memory and context awareness. It prevents errors, enables intelligent decisions, and tracks the complete lifecycle of all managed projects.
