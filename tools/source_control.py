import os
import json
from datetime import datetime

from github import (
    Auth,
    Github,
    InputGitTreeElement
)
from semantic_kernel.functions import kernel_function

from lib.log_client import logClient
from lib.CONSTANTS import SCAFFOLD_PROMPT_FILE
from lib.claude_details import AnthropicDetails
from tools.project_db import get_db
from tools.change_detector import ChangeDetector

class ProjectSourceControl:
    """
    Handles the Source Control component of the project scaffold app
    The LLM model will be limited to the functions and the PAT permissions
    """
    def __init__(self, ):
        self.GITHUB_PAT = os.getenv("GITHUB_ACCESS_TOKEN")
        self.AUTH = Auth.Token(self.GITHUB_PAT)
        self.gh_client = Github(auth=self.AUTH)
        self.logger = logClient(__name__)
        self.anthropic_details = AnthropicDetails()
        self.anthropic_client = self.anthropic_details.anthropic_client()
        self.project_db = get_db()  # Initialize project database
        self.change_detector = ChangeDetector(self.gh_client, self.project_db)  # Initialize change detector
        logger = self.logger
        if self.GITHUB_PAT is None:
            logger.error("""
                        Could not load GitHub PAT, ensure your PAT is
                        set as an enviroment variable""")
        else:
            logger.info("GitHub PAT loaded succesfully")
            try:
                self.AUTH
                logger.info("Authenticated using PAT")
            except:
                logger.error("""
                             Could not Authenticate with the loaded Personal Acces Token".
                             Ensure your Github PAT has sufficient permissions""")

    @kernel_function(
            description="list all user Github Repositories"
    )
    async def list_repos(self, ) -> str:
        logger = self.logger
        logger.info("Triggering Github List repos LLM function")
        all_repos = []
        try:
            user = self.gh_client.get_user()
            logger.info("Gihub List repos LLM fuction trigger successfully")
            for repo in user.get_repos():
                all_repos.append(repo.name)
            
            logger.info(f"Total repositories found: {len(all_repos)}")
            return f"You have {len(all_repos)} repositories: " + ", ".join([f"**{r}**" for r in all_repos])
        except Exception as e:
            logger.error(f"""
Issue with LLM function call: {e}
""")
            return f"Failed to list repositories: {e}"
    
    @kernel_function(
            description="List all tracked projects from the project database with their details including UUID, name, repository, location, and status"
    )
    async def list_projects(self, ) -> str:
        """Lists all tracked projects from the database"""
        logger = self.logger
        logger.info("Listing all tracked projects from database")
        try:
            summary = self.project_db.get_summary()
            logger.info("Successfully retrieved project summary")
            return summary
        except Exception as e:
            logger.error(f"Failed to list projects: {e}")
            return f"Failed to list projects: {e}"
    
    @kernel_function(
            description="Get detailed context about a specific project by repository name. Use this to check if a project exists before creating it."
    )
    async def get_project_info(self, repo_name: str) -> str:
        """Get detailed information about a specific project"""
        logger = self.logger
        logger.info(f"Getting project info for: {repo_name}")
        try:
            context = self.project_db.get_project_context(repo_name)
            if context:
                logger.info(f"Found project: {repo_name}")
                return context
            else:
                logger.info(f"Project not found: {repo_name}")
                return f"No project found with repository name: {repo_name}"
        except Exception as e:
            logger.error(f"Failed to get project info: {e}")
            return f"Failed to get project info: {e}"
    
    @kernel_function(
            description="Detect changes in a project - checks for modifications made locally (by user or other agents) and on GitHub since last check. Use this to understand what changed in a project."
    )
    async def detect_project_changes(self, repo_name: str) -> str:
        """Detect and report changes in a project"""
        logger = self.logger
        logger.info(f"Detecting changes for: {repo_name}")
        try:
            changes = self.change_detector.detect_changes(repo_name)
            report = self.change_detector.format_changes_report(changes)
            logger.info(f"Change detection complete for: {repo_name}")
            return report
        except Exception as e:
            logger.error(f"Failed to detect changes: {e}")
            return f"Failed to detect changes: {e}"
    
    @kernel_function(
            description="Update the file snapshot for a project in the database. Use this after making changes to track the new baseline state."
    )
    async def update_project_snapshot(self, repo_name: str) -> str:
        """Update the file snapshot for a project"""
        logger = self.logger
        logger.info(f"Updating snapshot for: {repo_name}")
        try:
            success = self.change_detector.update_snapshot(repo_name)
            if success:
                logger.info(f"Snapshot updated: {repo_name}")
                return f"✅ Successfully updated file snapshot for '{repo_name}'"
            else:
                return f"❌ Failed to update snapshot for '{repo_name}'"
        except Exception as e:
            logger.error(f"Failed to update snapshot: {e}")
            return f"Failed to update snapshot: {e}"

    @kernel_function(
            description="Create Github Repo"
    )  
    async def create_repo(self, repo_name: str,
                    project_description: str) -> str:
        """
        Creates a GitHub repository without initializing it with files.
        Returns the repository object if successful, None otherwise.
        """
        logger = self.logger
        logger.info(f"Triggering Github repo creation LLM function")
        
        user = self.gh_client.get_user()
        try:
            new_repo = user.create_repo(
                name=repo_name,
                description=project_description,
                auto_init=False  # Don't auto-initialize with README
            )
            logger.info(f"LLM function create GH repo {new_repo.name} successfully")
            return new_repo.name
        except Exception as e:
            logger.error(f"Error: Unable to create github repo: {e}")
            return None
    
    def create_repo_and_initialize(self, repo_name: str, project_description: str):
        """
        Creates a GitHub repository and returns the repo object for further operations.
        Initializes with auto_init=True to create the initial commit, which is required
        for the Git Database API to work.
        
        Args:
            repo_name: Name of the repository to create
            project_description: Description of the repository
            
        Returns:
            Repository object if successful, None otherwise
        """
        logger = self.logger
        logger.info(f"Creating GitHub repository: {repo_name}")
        
        user = self.gh_client.get_user()
        try:
            new_repo = user.create_repo(
                name=repo_name,
                description=project_description,
                auto_init=True  # Initialize with README to create initial commit
            )
            logger.info(f"Successfully created repository: {new_repo.name}")
            return new_repo
        except Exception as e:
            logger.error(f"Error creating GitHub repository: {e}")
            return None
    
    def commit_project(self, project_root_path: str, repo_name: str, 
                      project_description: str, commit_message: str = "Initial commit"):
        """
        Commits an entire project directory to a GitHub repository.
        Creates the repo if it doesn't exist, then commits all files.
        
        Args:
            project_root_path: Absolute path to the project root directory
            repo_name: Name of the GitHub repository
            project_description: Description of the repository
            commit_message: Commit message (default: "Initial commit")
            
        Returns:
            dict with status and repository URL, or error message
        """
        logger = self.logger
        
        # Validate project path exists
        if not os.path.exists(project_root_path):
            error_msg = f"Project path does not exist: {project_root_path}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        if not os.path.isdir(project_root_path):
            error_msg = f"Project path is not a directory: {project_root_path}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        logger.info(f"Committing project from: {project_root_path}")
        
        # Check if repository already exists, if not create it
        try:
            user = self.gh_client.get_user()
            repo = user.get_repo(repo_name)
            logger.info(f"Repository '{repo_name}' already exists, will push to existing repo")
        except:
            # Repository doesn't exist, create it
            logger.info(f"Creating GitHub repository: {repo_name}")
            repo = self.create_repo_and_initialize(repo_name, project_description)
            if repo is None:
                return {"status": "error", "message": "Failed to create repository"}
        
        try:
            # Collect all files from the project directory
            files_to_commit = []
            
            for root, dirs, files in os.walk(project_root_path):
                # Skip hidden directories and common ignore patterns
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                
                for file in files:
                    # Skip hidden files and common ignore patterns
                    if file.startswith('.'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    # Get relative path from project root
                    relative_path = os.path.relpath(file_path, project_root_path)
                    
                    # Read file content
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        files_to_commit.append({
                            'path': relative_path,
                            'content': content
                        })
                        logger.info(f"Added file: {relative_path}")
                    except Exception as e:
                        logger.warning(f"Could not read file {relative_path}: {e}")
            
            if not files_to_commit:
                logger.warning("No files found to commit")
                return {"status": "warning", "message": "No files found to commit", "repo_url": repo.html_url}
            
            # Create blobs for all files using InputGitTreeElement
            tree_elements = []
            for file_info in files_to_commit:
                # Create InputGitTreeElement for each file
                element = InputGitTreeElement(
                    path=file_info['path'],
                    mode='100644',  # Regular file
                    type='blob',
                    content=file_info['content']
                )
                tree_elements.append(element)
                logger.info(f"Added tree element: {file_info['path']}")
            
            logger.info(f"Created {len(tree_elements)} tree elements successfully")
            
            # Get the current branch and parent commit (since repo was initialized with auto_init=True)
            try:
                # Try to get main branch first
                ref = repo.get_git_ref("heads/main")
                parent_commit = repo.get_git_commit(ref.object.sha)
                base_tree = parent_commit.tree
                branch_name = "main"
                logger.info(f"Found main branch with base tree: {base_tree.sha}")
            except Exception as e:
                # Fall back to master if main doesn't exist
                try:
                    ref = repo.get_git_ref("heads/master")
                    parent_commit = repo.get_git_commit(ref.object.sha)
                    base_tree = parent_commit.tree
                    branch_name = "master"
                    logger.info(f"Found master branch with base tree: {base_tree.sha}")
                except Exception as e2:
                    # If neither exists, this shouldn't happen with auto_init=True, but handle it
                    logger.warning(f"No default branch found: {e}, {e2}")
                    parent_commit = None
                    base_tree = None
                    branch_name = "main"
            
            # Create tree with base tree from parent commit
            try:
                if base_tree:
                    tree = repo.create_git_tree(tree_elements, base_tree)
                    logger.info(f"Created tree with base: {tree.sha}")
                else:
                    tree = repo.create_git_tree(tree_elements)
                    logger.info(f"Created tree without base: {tree.sha}")
            except Exception as tree_error:
                logger.error(f"Failed to create git tree: {type(tree_error).__name__}: {str(tree_error)}")
                # Log more details about the error
                if hasattr(tree_error, 'data'):
                    logger.error(f"Error data: {tree_error.data}")
                if hasattr(tree_error, 'status'):
                    logger.error(f"Error status: {tree_error.status}")
                raise Exception(f"Git tree creation failed: {type(tree_error).__name__}: {str(tree_error)}")
            
            # Create commit with parent (to replace the auto-generated README commit)
            if parent_commit:
                commit = repo.create_git_commit(
                    message=commit_message,
                    tree=tree,
                    parents=[parent_commit]
                )
                logger.info(f"Created commit with parent: {commit.sha}")
            else:
                commit = repo.create_git_commit(
                    message=commit_message,
                    tree=tree,
                    parents=[]
                )
                logger.info(f"Created commit without parent: {commit.sha}")
            
            # Update branch reference
            if parent_commit:
                ref.edit(commit.sha)
            else:
                repo.create_git_ref(f"refs/heads/{branch_name}", commit.sha)
            
            logger.info(f"Successfully committed {len(files_to_commit)} files to {repo_name}")
            
            # Create file snapshot for change detection
            file_snapshot = self.change_detector.scan_local_files(project_root_path)
            logger.info(f"Created file snapshot with {len(file_snapshot)} files")
            
            # Add or update project in database
            try:
                project_uuid = self.project_db.add_project(
                    name=repo_name,
                    repo_name=repo_name,
                    local_path=project_root_path,
                    description=project_description,
                    repo_url=repo.html_url,
                    additional_metadata={
                        "commit_sha": commit.sha,
                        "commit_message": commit_message,
                        "branch": branch_name,
                        "files_count": len(files_to_commit),
                        "file_snapshot": file_snapshot,
                        "snapshot_created_at": datetime.now().isoformat()
                    }
                )
                logger.info(f"Added project to database with UUID: {project_uuid}")
            except Exception as db_error:
                logger.warning(f"Failed to add project to database: {db_error}")
            
            return {
                "status": "success",
                "message": f"Successfully committed {len(files_to_commit)} files",
                "repo_url": repo.html_url,
                "repo_name": repo.name,
                "commit_sha": commit.sha,
                "project_uuid": project_uuid if 'project_uuid' in locals() else None
            }
            
        except Exception as e:
            logger.error(f"Error committing project: {e}")
            return {"status": "error", "message": str(e), "repo_url": repo.html_url if repo else None}
    
    @kernel_function(
            description="Update an existing project with AI-generated changes. Analyzes the project, generates intelligent file updates based on user requirements, creates a feature branch, and submits a pull request. Use this when the user wants to modify, enhance, or add features to an existing project."
    )
    async def update_project_ai(self, repo_name: str, user_query: str) -> str:
        """
        LLM-callable function to update a project with AI assistance.
        
        Args:
            repo_name: Name of the GitHub repository to update
            user_query: Description of what changes to make
            
        Returns:
            Formatted string with update results including PR URL
        """
        logger = self.logger
        logger.info(f"LLM triggered update_project_ai for: {repo_name}")
        logger.info(f"User query: {user_query}")
        
        # Get project from database
        try:
            project = self.project_db.get_project_by_repo(repo_name)
            if not project:
                return f"Error: Project '{repo_name}' not found in database. Use list_projects() to see available projects."
            
            project_path = project['local_path']
            logger.info(f"Found project at: {project_path}")
            
        except Exception as e:
            error_msg = f"Failed to get project from database: {e}"
            logger.error(error_msg)
            return error_msg
        
        # Call the internal update_project method
        result = self.update_project(
            project_root_path=project_path,
            repo_name=repo_name,
            user_query=user_query,
            commit_message=None  # Auto-generated
        )
        
        # Format result for LLM
        if result["status"] == "success":
            response = f"""Successfully updated project '{repo_name}'! 🎉

**Summary**: {result['message']}

**Pull Request Created**:
- PR #{result['pr_number']}: {result['pr_url']}
- Feature Branch: {result['feature_branch']}
- Base Branch: {result['base_branch']}

**Changes Made**:
- Modified: {result['changes']['modified']} files
- Added: {result['changes']['added']} files  
- Deleted: {result['changes']['deleted']} files

**Commit**: {result['commit_sha'][:7]}

The changes are ready for review in the pull request. You can merge the PR when ready!
"""
            logger.info(f"Update successful: PR #{result['pr_number']}")
            return response
            
        elif result["status"] == "partial":
            response = f"""Partial success updating '{repo_name}':

{result['message']}

**Feature Branch**: {result['feature_branch']}
**Commit**: {result['commit_sha'][:7]}

The branch was created but the PR failed. You may need to create the PR manually.
"""
            logger.warning(f"Partial update: {result['message']}")
            return response
            
        else:
            error_msg = f"Failed to update '{repo_name}': {result['message']}"
            logger.error(error_msg)
            return error_msg
    
    def update_project(self, project_root_path: str, repo_name: str, 
                      user_query: str, commit_message: str = None):
        """
        Updates an existing project based on user requirements.
        Uses Claude AI to generate updated files, then commits to GitHub.
        
        Args:
            project_root_path: Absolute path to the project root directory
            repo_name: Name of the existing GitHub repository
            user_query: User's description of what changes to make
            commit_message: Optional custom commit message (auto-generated if None)
            
        Returns:
            dict with status and repository URL, or error message
        """
        logger = self.logger
        
        # Validate project path exists
        if not os.path.exists(project_root_path):
            error_msg = f"Project path does not exist: {project_root_path}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        if not os.path.isdir(project_root_path):
            error_msg = f"Project path is not a directory: {project_root_path}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        logger.info(f"Updating project from: {project_root_path}")
        logger.info(f"User request: {user_query}")
        
        # Get the existing repository
        try:
            user = self.gh_client.get_user()
            repo = user.get_repo(repo_name)
            logger.info(f"Found repository: {repo.name}")
        except Exception as e:
            error_msg = f"Repository '{repo_name}' not found: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        # Read existing project structure
        project_files = {}
        for root, dirs, files in os.walk(project_root_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_root_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        project_files[relative_path] = f.read()
                except Exception as e:
                    logger.warning(f"Could not read file {relative_path}: {e}")
        
        logger.info(f"Read {len(project_files)} existing files")
        
        # Build prompt for Claude to generate updates
        update_prompt = f"""You are an expert software engineer. The user wants to update an existing project.

PROJECT LOCATION: {project_root_path}
REPOSITORY: {repo_name}

USER REQUEST: {user_query}

EXISTING PROJECT FILES:
{json.dumps(list(project_files.keys()), indent=2)}

CRITICAL INSTRUCTIONS:
1. Analyze the user's request carefully
2. Determine which files need to be modified, added, or deleted
3. Generate the complete updated file contents
4. Return ONLY valid JSON in this exact format (NO markdown, NO code fences):

{{
  "changes": [
    {{
      "path": "relative/path/to/file",
      "action": "modify|add|delete",
      "content": "full file content here (empty string for delete)"
    }}
  ],
  "summary": "Brief description of changes made"
}}

RULES:
- Include COMPLETE file content, not snippets
- Use proper file paths relative to project root
- action must be: "modify", "add", or "delete"
- For "delete" action, content must be empty string ""
- Return ONLY JSON, no explanations outside JSON
- Do NOT wrap JSON in markdown code fences
"""

        # Call Claude to generate updates
        try:
            logger.info("Requesting updates from Claude AI...")
            response = self.anthropic_client.messages.create(
                model=self.anthropic_details.claude_sonnet_latest(),
                max_tokens=64000,
                stream=True,
                messages=[{"role": "user", "content": update_prompt}]
            )
            
            # Collect streaming response
            full_text = ""
            with response as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, "text"):
                            full_text += event.delta.text
            
            # Extract JSON from response
            json_start = full_text.find('{')
            json_end = full_text.rfind('}') + 1
            json_str = full_text[json_start:json_end]
            
            update_data = json.loads(json_str)
            logger.info(f"Claude generated {len(update_data['changes'])} file changes")
            logger.info(f"Summary: {update_data['summary']}")
            
        except Exception as e:
            error_msg = f"Failed to generate updates with Claude: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        # Apply changes to local files
        files_modified = []
        files_added = []
        files_deleted = []
        
        try:
            for change in update_data['changes']:
                file_path = os.path.join(project_root_path, change['path'])
                action = change['action']
                
                if action == "delete":
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        files_deleted.append(change['path'])
                        logger.info(f"Deleted: {change['path']}")
                
                elif action in ["modify", "add"]:
                    # Create directory if needed
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    # Write file content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(change['content'])
                    
                    if action == "modify":
                        files_modified.append(change['path'])
                        logger.info(f"Modified: {change['path']}")
                    else:
                        files_added.append(change['path'])
                        logger.info(f"Added: {change['path']}")
            
            logger.info(f"Applied changes locally: {len(files_modified)} modified, {len(files_added)} added, {len(files_deleted)} deleted")
            
        except Exception as e:
            error_msg = f"Failed to apply changes locally: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        # Collect all current files for commit
        files_to_commit = []
        for root, dirs, files in os.walk(project_root_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_root_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    files_to_commit.append({'path': relative_path, 'content': content})
                except Exception as e:
                    logger.warning(f"Could not read file {relative_path}: {e}")
        
        # Create tree elements
        tree_elements = []
        for file_info in files_to_commit:
            element = InputGitTreeElement(
                path=file_info['path'],
                mode='100644',
                type='blob',
                content=file_info['content']
            )
            tree_elements.append(element)
        
        logger.info(f"Prepared {len(tree_elements)} files for commit")
        
        # Get base branch (main or master) and parent commit
        try:
            base_ref = repo.get_git_ref("heads/main")
            parent_commit = repo.get_git_commit(base_ref.object.sha)
            base_tree = parent_commit.tree
            base_branch = "main"
        except:
            try:
                base_ref = repo.get_git_ref("heads/master")
                parent_commit = repo.get_git_commit(base_ref.object.sha)
                base_tree = parent_commit.tree
                base_branch = "master"
            except Exception as e:
                error_msg = f"Could not find main or master branch: {e}"
                logger.error(error_msg)
                return {"status": "error", "message": error_msg}
        
        # Create feature branch name from summary
        import re
        import time
        timestamp = int(time.time())
        # Create branch name from summary (lowercase, replace spaces/special chars with hyphens)
        branch_suffix = re.sub(r'[^a-z0-9]+', '-', update_data['summary'].lower())[:50]
        feature_branch_name = f"feature/{branch_suffix}-{timestamp}"
        
        logger.info(f"Creating feature branch: {feature_branch_name}")
        
        # Create tree and commit
        try:
            tree = repo.create_git_tree(tree_elements, base_tree)
            
            # Generate commit message if not provided
            if not commit_message:
                commit_message = f"Update: {update_data['summary']}\n\nChanges:\n"
                if files_modified:
                    commit_message += f"- Modified: {', '.join(files_modified[:5])}"
                    if len(files_modified) > 5:
                        commit_message += f" and {len(files_modified) - 5} more"
                    commit_message += "\n"
                if files_added:
                    commit_message += f"- Added: {', '.join(files_added[:5])}"
                    if len(files_added) > 5:
                        commit_message += f" and {len(files_added) - 5} more"
                    commit_message += "\n"
                if files_deleted:
                    commit_message += f"- Deleted: {', '.join(files_deleted)}\n"
            
            # Create commit
            commit = repo.create_git_commit(
                message=commit_message,
                tree=tree,
                parents=[parent_commit]
            )
            
            logger.info(f"Created commit: {commit.sha}")
            
            # Create feature branch reference
            try:
                feature_ref = repo.create_git_ref(f"refs/heads/{feature_branch_name}", commit.sha)
                logger.info(f"Created feature branch: {feature_branch_name}")
            except Exception as e:
                error_msg = f"Failed to create feature branch: {e}"
                logger.error(error_msg)
                return {"status": "error", "message": error_msg}
            
            # Create pull request
            try:
                pr_title = f"Update: {update_data['summary']}"
                pr_body = f"""## Changes
                
{update_data['summary']}

### Details
- **Modified files**: {len(files_modified)}
- **Added files**: {len(files_added)}
- **Deleted files**: {len(files_deleted)}

### File Changes
"""
                if files_modified:
                    pr_body += "\n**Modified:**\n"
                    for f in files_modified[:10]:
                        pr_body += f"- `{f}`\n"
                    if len(files_modified) > 10:
                        pr_body += f"- ... and {len(files_modified) - 10} more\n"
                
                if files_added:
                    pr_body += "\n**Added:**\n"
                    for f in files_added[:10]:
                        pr_body += f"- `{f}`\n"
                    if len(files_added) > 10:
                        pr_body += f"- ... and {len(files_added) - 10} more\n"
                
                if files_deleted:
                    pr_body += "\n**Deleted:**\n"
                    for f in files_deleted:
                        pr_body += f"- `{f}`\n"
                
                pr_body += f"\n---\n*Generated by AI-powered project updater*\n*Commit: {commit.sha[:7]}*"
                
                pull_request = repo.create_pull(
                    title=pr_title,
                    body=pr_body,
                    head=feature_branch_name,
                    base=base_branch
                )
                
                logger.info(f"Created pull request: {pull_request.html_url}")
                
                # Create updated file snapshot
                file_snapshot = self.change_detector.scan_local_files(project_root_path)
                logger.info(f"Created updated file snapshot with {len(file_snapshot)} files")
                
                # Update project in database
                try:
                    project = self.project_db.get_project_by_repo(repo_name)
                    if project:
                        self.project_db.update_project(
                            project['uuid'],
                            {
                                "metadata": {
                                    **project.get('metadata', {}),
                                    "last_update": {
                                        "commit_sha": commit.sha,
                                        "pr_number": pull_request.number,
                                        "pr_url": pull_request.html_url,
                                        "feature_branch": feature_branch_name,
                                        "summary": update_data['summary'],
                                        "changes": {
                                            "modified": len(files_modified),
                                            "added": len(files_added),
                                            "deleted": len(files_deleted)
                                        }
                                    },
                                    "file_snapshot": file_snapshot,
                                    "snapshot_updated_at": datetime.now().isoformat()
                                }
                            }
                        )
                        logger.info(f"Updated project in database: {project['uuid']}")
                except Exception as db_error:
                    logger.warning(f"Failed to update project in database: {db_error}")
                
                return {
                    "status": "success",
                    "message": update_data['summary'],
                    "repo_url": repo.html_url,
                    "repo_name": repo.name,
                    "commit_sha": commit.sha,
                    "feature_branch": feature_branch_name,
                    "base_branch": base_branch,
                    "pr_number": pull_request.number,
                    "pr_url": pull_request.html_url,
                    "changes": {
                        "modified": len(files_modified),
                        "added": len(files_added),
                        "deleted": len(files_deleted)
                    },
                    "commit_message": commit_message
                }
                
            except Exception as e:
                error_msg = f"Failed to create pull request: {e}"
                logger.error(error_msg)
                # Return partial success - branch was created but PR failed
                return {
                    "status": "partial",
                    "message": f"Branch created but PR failed: {e}",
                    "repo_url": repo.html_url,
                    "repo_name": repo.name,
                    "commit_sha": commit.sha,
                    "feature_branch": feature_branch_name,
                    "base_branch": base_branch,
                    "changes": {
                        "modified": len(files_modified),
                        "added": len(files_added),
                        "deleted": len(files_deleted)
                    }
                }
            
        except Exception as e:
            error_msg = f"Failed to commit updates: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg, "repo_url": repo.html_url}
    
    @kernel_function(
            description="Delete a project locally and/or from GitHub. Can delete just local files, just the GitHub repository, or both. Use when user wants to remove or clean up a project."
    )
    async def delete_project_ai(self, repo_name: str, delete_local: bool = True, delete_remote: bool = True) -> str:
        """
        LLM-callable function to delete a project.
        
        Args:
            repo_name: Name of the GitHub repository to delete
            delete_local: Whether to delete local files (default: True)
            delete_remote: Whether to delete GitHub repository (default: True)
            
        Returns:
            Formatted string with deletion results
        """
        logger = self.logger
        logger.info(f"LLM triggered delete_project_ai for: {repo_name}")
        logger.info(f"Delete local: {delete_local}, Delete remote: {delete_remote}")
        
        # Get project from database
        try:
            project = self.project_db.get_project_by_repo(repo_name)
            if not project:
                return f"Error: Project '{repo_name}' not found in database. Use list_projects() to see available projects."
            
            project_path = project['local_path']
            logger.info(f"Found project at: {project_path}")
            
        except Exception as e:
            error_msg = f"Failed to get project from database: {e}"
            logger.error(error_msg)
            return error_msg
        
        # Call the internal delete_project method
        result = self.delete_project(
            project_root_path=project_path,
            repo_name=repo_name,
            delete_local=delete_local,
            delete_remote=delete_remote
        )
        
        # Format result for LLM
        if result["status"] == "success":
            response = f"""Successfully deleted project '{repo_name}'! 🗑️

**Actions Taken**:
"""
            for msg in result["messages"]:
                response += f"- {msg}\n"
            
            logger.info(f"Delete successful: {repo_name}")
            return response
            
        elif result["status"] == "partial":
            response = f"""Partially deleted project '{repo_name}':

**Results**:
"""
            for msg in result["messages"]:
                response += f"- {msg}\n"
            
            logger.warning(f"Partial delete: {repo_name}")
            return response
            
        else:
            error_msg = f"Failed to delete '{repo_name}':\n"
            for msg in result["messages"]:
                error_msg += f"- {msg}\n"
            
            logger.error(error_msg)
            return error_msg
    
    def delete_project(self, project_root_path: str, repo_name: str, delete_local: bool = True, delete_remote: bool = True):
        """
        Deletes a project locally and/or from GitHub.
        
        Args:
            project_root_path: Absolute path to the project root directory
            repo_name: Name of the GitHub repository
            delete_local: Whether to delete local project files (default: True)
            delete_remote: Whether to delete GitHub repository (default: True)
            
        Returns:
            dict with status and details about what was deleted
        """
        import shutil
        
        logger = self.logger
        results = {
            "status": "success",
            "local_deleted": False,
            "remote_deleted": False,
            "messages": []
        }
        
        # Delete local project
        if delete_local:
            if os.path.exists(project_root_path):
                try:
                    shutil.rmtree(project_root_path)
                    logger.info(f"Deleted local project: {project_root_path}")
                    results["local_deleted"] = True
                    results["messages"].append(f"Local project deleted: {project_root_path}")
                except Exception as e:
                    error_msg = f"Failed to delete local project: {e}"
                    logger.error(error_msg)
                    results["status"] = "partial"
                    results["messages"].append(error_msg)
            else:
                warning_msg = f"Local project path does not exist: {project_root_path}"
                logger.warning(warning_msg)
                results["messages"].append(warning_msg)
        
        # Delete GitHub repository
        if delete_remote:
            try:
                user = self.gh_client.get_user()
                repo = user.get_repo(repo_name)
                repo_url = repo.html_url
                repo.delete()
                logger.info(f"Deleted GitHub repository: {repo_name}")
                results["remote_deleted"] = True
                results["messages"].append(f"GitHub repository deleted: {repo_url}")
            except Exception as e:
                error_msg = f"Failed to delete GitHub repository: {e}"
                logger.error(error_msg)
                if results["status"] == "success":
                    results["status"] = "partial"
                else:
                    results["status"] = "error"
                results["messages"].append(error_msg)
        
        # Update project in database (mark as deleted)
        try:
            project = self.project_db.get_project_by_repo(repo_name)
            if project:
                if delete_local and delete_remote:
                    # Hard delete if both local and remote are deleted
                    self.project_db.hard_delete_project(project['uuid'])
                    logger.info(f"Removed project from database: {project['uuid']}")
                    results["messages"].append("Project removed from database")
                else:
                    # Soft delete if only one is deleted
                    self.project_db.delete_project(project['uuid'])
                    logger.info(f"Marked project as deleted in database: {project['uuid']}")
                    results["messages"].append("Project marked as deleted in database")
        except Exception as db_error:
            logger.warning(f"Failed to update project in database: {db_error}")
            results["messages"].append(f"Warning: Failed to update database: {db_error}")
        
        # Set final status
        if not results["local_deleted"] and not results["remote_deleted"]:
            results["status"] = "error"
            results["messages"].append("Nothing was deleted")
        
        return results
    
