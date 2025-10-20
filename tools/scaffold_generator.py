import os
import json

from semantic_kernel.functions import kernel_function

from  lib.CONSTANTS import (
    SCAFFOLD_PROMPT_FILE,
    SCAFFOLD_DIRECTORY
    )
from lib.claude_details import AnthropicDetails
from lib.log_client import logClient
from tools.source_control import ProjectSourceControl

class ProjectScaffold:
    """
    Handles Creating the Project Scaffold
    """
    def __init__(self, ):
        self.anthropic_details = AnthropicDetails()
        self.anthropic_client = self.anthropic_details.anthropic_client()
        self.logger = logClient(__name__)

    def project_scaffolder(self, user_query: str) -> dict:
        client = self.anthropic_client
        with open(SCAFFOLD_PROMPT_FILE, "r") as file:
            prompt = file.read()
            file.close()
        query = user_query + "\n" + prompt
        
        # Stream is required for large responses
        response = client.messages.create(
            model=self.anthropic_details.claude_sonnet_latest(),
            max_tokens=64000,
            stream=True,
            messages=[
                {
                "role": "user",
                "content": query,
                }
                ]
                )
        
        # Collect the full response text from streaming chunks
        full_text = ""
        with response as stream:
            for event in stream:
                if event.type == "content_block_delta":
                    if hasattr(event.delta, "text"):
                        full_text += event.delta.text
        
        # Extract JSON from the response
        json_start = full_text.find('{')
        json_end = full_text.rfind('}') + 1
        json_str = full_text[json_start:json_end]
        
        # Parse and return the JSON
        return json.loads(json_str)
     
    @kernel_function(
            description="""
Generate Project Scaffold and commit to GitHub
"""
    )
    def generate_scaffold(self, query: str) -> str:
        """
        Generates a project scaffold from user query and automatically commits to GitHub.
        
        Args:
            query: User's project description/requirements
            
        Returns:
            Status message with project details and GitHub URL
        """
        logger = self.logger
        create = ProjectScaffold()

        # Generate the scaffold once and reuse it
        logger.info(f"Generating scaffold for query: {query}")
        scaffold = create.project_scaffolder(query)

        project_name = scaffold['project_name']
        project_desc = scaffold['description']
        
        print(f"\nCreating project: {project_name}")
        print(f"Description: {project_desc}\n")

        # Create project directory path
        project_path = os.path.join(SCAFFOLD_DIRECTORY, project_name)
        os.makedirs(project_path, exist_ok=True)
        logger.info(f"Created project directory: {project_path}")

        # Create all folders
        print("Creating directories...")
        folders = scaffold["structure"]["folders"]
        for dir in folders:
            try:
                full_path = os.path.join(project_path, dir)
                os.makedirs(full_path, exist_ok=True)
                print(f"  [SUCCESS] {dir}")
            except Exception as e:
                logger.error(f"Error creating directory {dir}: {e}")
                print(f"  [ERROR] Error creating {dir}: {e}")

        # Create all files
        print("\nCreating files...")
        files = scaffold["structure"]["files"]
        file_count = 0
        for file_path, content in files.items():
            try:
                full_path = os.path.join(project_path, file_path)
        
                # Create parent directory if it doesn't exist
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
                # Write file content
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                    print(f"  [SUCCESS] {file_path}")
                    file_count += 1
            except Exception as e:
                logger.error(f"Error creating file {file_path}: {e}")
                print(f"  [ERROR] Error creating {file_path}: {e}")

        print(f"\n[SUCCESS] Project '{project_name}' created successfully!")
        print(f"Location: {project_path}")
        print(f"Total files: {file_count}")
        
        # Automatically commit to GitHub
        print("\nCommitting to GitHub...")
        logger.info(f"Initiating GitHub commit for project: {project_name}")
        
        source_control = ProjectSourceControl()
        commit_result = source_control.commit_project(
            project_root_path=project_path,
            repo_name=project_name,
            project_description=project_desc,
            commit_message=f"Initial commit: {project_name}\n\n{project_desc}"
        )
        
        # Handle commit result
        if commit_result["status"] == "success":
            logger.info(f"Successfully committed project to GitHub: {commit_result['repo_url']}")
            print(f"\n Successfully committed to GitHub!")
            print(f"Repository: {commit_result['repo_url']}")
            print(f"Commit SHA: {commit_result['commit_sha']}")
            print(f"Files committed: {commit_result['message']}")
            
            return f"""
Project '{project_name}' created and committed successfully!
- Local Path: {project_path}
- GitHub URL: {commit_result['repo_url']}
- Files: {file_count} created
- Status: {commit_result['message']}
"""
        else:
            logger.error(f"Failed to commit to GitHub: {commit_result['message']}")
            print(f"\nProject created locally but GitHub commit failed!")
            print(f"Error: {commit_result['message']}")
            
            if commit_result.get('repo_url'):
                print(f"Repository (may be empty): {commit_result['repo_url']}")
            
            return f"""
Project '{project_name}' created locally but GitHub commit failed.
- Local Path: {project_path}
- Files: {file_count} created
- Error: {commit_result['message']}
Please commit manually or check your GitHub PAT permissions.
"""

