import os

from github import (
    Auth,
    Github
)
from github.Repository import Repository
from semantic_kernel.functions import kernel_function
from anthropic import Anthropic

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
        logger = self.logger
        logger.info(f"""
Triggering Github repo creation LLM function
""")
        
        user = self.gh_client.get_user()
        try:
            new_repo = user.create_repo(
                name=repo_name,
                description=project_description
            )
            logger.info(f"LLM function create GH repo {new_repo.name} successfully")
            return new_repo.name
        except Exception as e:
            logger.info(f"Error: Unable to create github repo: {e}")
    
