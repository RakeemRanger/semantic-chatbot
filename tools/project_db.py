"""
Project Database - Simple JSON-based database for tracking projects
"""
import json
import os
import uuid
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

class ProjectDatabase:
    """Manages project metadata in a JSON database"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the project database
        
        Args:
            db_path: Path to the JSON database file. If None, uses default location.
        """
        if db_path is None:
            # Default to .dartinbot/projects/projects_db.json
            home = Path.home()
            db_dir = home / "semantic" / ".dartinbot" / "projects"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "projects_db.json"
        
        self.db_path = str(db_path)
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create the database file if it doesn't exist"""
        if not os.path.exists(self.db_path):
            self._write_db({"projects": [], "version": "1.0"})
    
    def _read_db(self) -> Dict:
        """Read the entire database"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading database: {e}")
            return {"projects": [], "version": "1.0"}
    
    def _write_db(self, data: Dict):
        """Write the entire database"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing database: {e}")
    
    def add_project(self, name: str, repo_name: str, local_path: str, 
                   description: str = "", repo_url: str = "", 
                   additional_metadata: Dict = None) -> str:
        """
        Add a new project to the database
        
        Args:
            name: Project name
            repo_name: GitHub repository name
            local_path: Absolute path to local project directory
            description: Project description
            repo_url: GitHub repository URL
            additional_metadata: Any additional metadata to store
            
        Returns:
            UUID of the created project
        """
        db = self._read_db()
        
        # Check if project already exists by repo_name
        existing = self.get_project_by_repo(repo_name)
        if existing:
            print(f"Project with repo '{repo_name}' already exists: {existing['uuid']}")
            return existing['uuid']
        
        project_uuid = str(uuid.uuid4())
        project = {
            "uuid": project_uuid,
            "name": name,
            "repo_name": repo_name,
            "local_path": local_path,
            "description": description,
            "repo_url": repo_url,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "active",
            "metadata": additional_metadata or {}
        }
        
        db["projects"].append(project)
        self._write_db(db)
        
        print(f"Added project '{name}' with UUID: {project_uuid}")
        return project_uuid
    
    def get_project(self, project_uuid: str) -> Optional[Dict]:
        """Get a project by UUID"""
        db = self._read_db()
        for project in db["projects"]:
            if project["uuid"] == project_uuid:
                return project
        return None
    
    def get_project_by_name(self, name: str) -> Optional[Dict]:
        """Get a project by name"""
        db = self._read_db()
        for project in db["projects"]:
            if project["name"] == name:
                return project
        return None
    
    def get_project_by_repo(self, repo_name: str) -> Optional[Dict]:
        """Get a project by repository name"""
        db = self._read_db()
        for project in db["projects"]:
            if project["repo_name"] == repo_name:
                return project
        return None
    
    def list_all_projects(self) -> List[Dict]:
        """Get all projects"""
        db = self._read_db()
        return db["projects"]
    
    def list_active_projects(self) -> List[Dict]:
        """Get all active projects"""
        db = self._read_db()
        return [p for p in db["projects"] if p.get("status") == "active"]
    
    def update_project(self, project_uuid: str, updates: Dict) -> bool:
        """
        Update a project's metadata
        
        Args:
            project_uuid: UUID of the project to update
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        db = self._read_db()
        
        for i, project in enumerate(db["projects"]):
            if project["uuid"] == project_uuid:
                # Update fields
                for key, value in updates.items():
                    if key != "uuid":  # Never allow UUID changes
                        project[key] = value
                
                # Always update the timestamp
                project["updated_at"] = datetime.now().isoformat()
                
                db["projects"][i] = project
                self._write_db(db)
                print(f"Updated project: {project_uuid}")
                return True
        
        print(f"Project not found: {project_uuid}")
        return False
    
    def delete_project(self, project_uuid: str) -> bool:
        """
        Delete a project from the database (soft delete by default)
        
        Args:
            project_uuid: UUID of the project to delete
            
        Returns:
            True if successful, False otherwise
        """
        db = self._read_db()
        
        for i, project in enumerate(db["projects"]):
            if project["uuid"] == project_uuid:
                # Soft delete - mark as deleted
                project["status"] = "deleted"
                project["deleted_at"] = datetime.now().isoformat()
                db["projects"][i] = project
                self._write_db(db)
                print(f"Deleted project: {project_uuid}")
                return True
        
        print(f"Project not found: {project_uuid}")
        return False
    
    def hard_delete_project(self, project_uuid: str) -> bool:
        """
        Permanently delete a project from the database
        
        Args:
            project_uuid: UUID of the project to delete
            
        Returns:
            True if successful, False otherwise
        """
        db = self._read_db()
        
        original_count = len(db["projects"])
        db["projects"] = [p for p in db["projects"] if p["uuid"] != project_uuid]
        
        if len(db["projects"]) < original_count:
            self._write_db(db)
            print(f"Permanently deleted project: {project_uuid}")
            return True
        
        print(f"Project not found: {project_uuid}")
        return False
    
    def search_projects(self, query: str) -> List[Dict]:
        """
        Search projects by name, description, or repo_name
        
        Args:
            query: Search query string
            
        Returns:
            List of matching projects
        """
        db = self._read_db()
        query_lower = query.lower()
        
        results = []
        for project in db["projects"]:
            if project.get("status") == "deleted":
                continue
            
            # Search in name, description, and repo_name
            if (query_lower in project["name"].lower() or
                query_lower in project.get("description", "").lower() or
                query_lower in project["repo_name"].lower()):
                results.append(project)
        
        return results
    
    def get_summary(self) -> str:
        """Get a summary of all projects for LLM context"""
        db = self._read_db()
        active_projects = [p for p in db["projects"] if p.get("status") == "active"]
        
        if not active_projects:
            return "No active projects found."
        
        summary = f"You have {len(active_projects)} active project(s):\n\n"
        
        for project in active_projects:
            summary += f"**{project['name']}** (UUID: {project['uuid'][:8]}...)\n"
            summary += f"  - Repository: {project['repo_name']}\n"
            summary += f"  - Location: {project['local_path']}\n"
            summary += f"  - Description: {project.get('description', 'No description')}\n"
            summary += f"  - Created: {project.get('created_at', 'Unknown')}\n"
            if project.get('repo_url'):
                summary += f"  - URL: {project['repo_url']}\n"
            summary += "\n"
        
        return summary
    
    def get_project_context(self, repo_name: str) -> Optional[str]:
        """
        Get detailed context about a specific project for LLM
        
        Args:
            repo_name: Repository name to get context for
            
        Returns:
            Formatted string with project details
        """
        project = self.get_project_by_repo(repo_name)
        
        if not project:
            return None
        
        context = f"""PROJECT CONTEXT:
UUID: {project['uuid']}
Name: {project['name']}
Repository: {project['repo_name']}
Local Path: {project['local_path']}
Description: {project.get('description', 'No description')}
Status: {project.get('status', 'unknown')}
Created: {project.get('created_at', 'Unknown')}
Last Updated: {project.get('updated_at', 'Unknown')}
"""
        
        if project.get('repo_url'):
            context += f"Repository URL: {project['repo_url']}\n"
        
        if project.get('metadata'):
            context += f"\nAdditional Metadata:\n"
            for key, value in project['metadata'].items():
                context += f"  {key}: {value}\n"
        
        return context


# Global instance for easy access
_db_instance = None

def get_db() -> ProjectDatabase:
    """Get the global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = ProjectDatabase()
    return _db_instance
