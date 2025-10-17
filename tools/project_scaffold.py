import os

from github import (
    Auth,
    Github
)
from github.Repository import Repository
from semantic_kernel.functions import kernel_function

class ProjectSourceControl:
    """
    Handles the Source Control component of the project scaffold app
    The LLM model will be limited to the functions and the PAT permissions
    """
    def __init__(self, ):
        self.GITHUB_PAT = os.getenv("GITHUB_ACCESS_TOKEN")
        self.AUTH = Auth.Token(self.GITHUB_PAT)
        self.gh_client = Github(auth=self.AUTH)

    @kernel_function(
            description="list all user Github Repositories"
    )
    async def list_repos(self, ) -> str:
        user = self.gh_client.get_user()
        for repo in user.get_repos():
            return repo.name

    @kernel_function(
            description="Create Github Repo"
    )  
    async def create_repo(self, repo_name: str,
                    project_description: str) -> str:
        user = self.gh_client.get_user()
        try:
            new_repo = user.create_repo(
                name=repo_name,
                description=project_description
            )
            return new_repo.name
        except Exception as e:
            return f"Error: Unable to create github repo: {e}"