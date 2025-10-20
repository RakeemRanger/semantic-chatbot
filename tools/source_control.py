import os

from github import (
    Auth,
    Github
)
from semantic_kernel.functions import kernel_function

from lib.log_client import logClient

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
        try:
            user = self.gh_client.get_user()
            logger.info("Gihub List repos LLM fuction trigger successfully")
            for repo in user.get_repos():
                return repo.name
        except Exception as e:
            logger.error(f"""
Issue with LLM function call: {e}
""")

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
        This is a non-kernel function meant to be called internally.
        
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
                auto_init=False
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
        
        # Create the repository
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
            
            # Create blobs for all files
            blobs = []
            for file_info in files_to_commit:
                blob = repo.create_git_blob(file_info['content'], "utf-8")
                blobs.append({
                    'path': file_info['path'],
                    'sha': blob.sha,
                    'mode': '100644',  # Regular file
                    'type': 'blob'
                })
            
            # Create tree
            tree = repo.create_git_tree(blobs)
            
            # Create commit
            commit = repo.create_git_commit(
                message=commit_message,
                tree=tree,
                parents=[]  # No parents for initial commit
            )
            
            # Update master/main branch reference
            try:
                ref = repo.get_git_ref("heads/main")
                ref.edit(commit.sha)
            except:
                # If main doesn't exist, try master
                try:
                    ref = repo.get_git_ref("heads/master")
                    ref.edit(commit.sha)
                except:
                    # Create main branch
                    repo.create_git_ref("refs/heads/main", commit.sha)
            
            logger.info(f"Successfully committed {len(files_to_commit)} files to {repo_name}")
            
            return {
                "status": "success",
                "message": f"Successfully committed {len(files_to_commit)} files",
                "repo_url": repo.html_url,
                "repo_name": repo.name,
                "commit_sha": commit.sha
            }
            
        except Exception as e:
            logger.error(f"Error committing project: {e}")
            return {"status": "error", "message": str(e), "repo_url": repo.html_url if repo else None}
    
