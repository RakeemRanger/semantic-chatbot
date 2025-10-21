"""
Change Detection System - Detects modifications made locally and on GitHub
Helps track changes made by users or other agents outside of the chatbot
"""
import os
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from github import Github


class ChangeDetector:
    """Detects changes in local files and GitHub repositories"""
    
    def __init__(self, gh_client: Github, project_db):
        """
        Initialize change detector
        
        Args:
            gh_client: Authenticated GitHub client
            project_db: Project database instance
        """
        self.gh_client = gh_client
        self.project_db = project_db
    
    def compute_file_hash(self, file_path: str) -> str:
        """Compute SHA256 hash of a file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"Error hashing file {file_path}: {e}")
            return ""
    
    def scan_local_files(self, project_root: str) -> Dict[str, Dict]:
        """
        Scan all files in a project directory and compute hashes
        
        Args:
            project_root: Absolute path to project root
            
        Returns:
            Dict mapping relative paths to file info (hash, size, mtime)
        """
        files_info = {}
        
        if not os.path.exists(project_root):
            return files_info
        
        for root, dirs, files in os.walk(project_root):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                'node_modules', '__pycache__', 'venv', 'env', '.git', 
                '.vscode', '.idea', 'dist', 'build'
            ]]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_root)
                
                try:
                    stat_info = os.stat(file_path)
                    files_info[relative_path] = {
                        'hash': self.compute_file_hash(file_path),
                        'size': stat_info.st_size,
                        'mtime': stat_info.st_mtime,
                        'mtime_iso': datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                    }
                except Exception as e:
                    print(f"Error scanning {relative_path}: {e}")
        
        return files_info
    
    def get_github_files(self, repo_name: str, branch: str = "main") -> Dict[str, Dict]:
        """
        Get all files from a GitHub repository
        
        Args:
            repo_name: Repository name
            branch: Branch name (default: main)
            
        Returns:
            Dict mapping paths to file info (sha, size)
        """
        files_info = {}
        
        try:
            user = self.gh_client.get_user()
            repo = user.get_repo(repo_name)
            
            # Try main first, then master
            try:
                tree = repo.get_git_tree(branch, recursive=True)
            except:
                try:
                    tree = repo.get_git_tree("master", recursive=True)
                except Exception as e:
                    print(f"Could not get tree for {repo_name}: {e}")
                    return files_info
            
            for item in tree.tree:
                if item.type == "blob":  # Only files, not directories
                    files_info[item.path] = {
                        'sha': item.sha,
                        'size': item.size
                    }
        
        except Exception as e:
            print(f"Error getting GitHub files: {e}")
        
        return files_info
    
    def compare_local_to_snapshot(self, project_root: str, snapshot: Dict[str, Dict]) -> Dict:
        """
        Compare current local files to a previous snapshot
        
        Args:
            project_root: Path to project
            snapshot: Previous file snapshot from database
            
        Returns:
            Dict with added, modified, deleted, and unchanged files
        """
        current_files = self.scan_local_files(project_root)
        
        added = []
        modified = []
        deleted = []
        unchanged = []
        
        # Check for added and modified files
        for path, info in current_files.items():
            if path not in snapshot:
                added.append({
                    'path': path,
                    'size': info['size'],
                    'hash': info['hash']
                })
            elif snapshot[path]['hash'] != info['hash']:
                modified.append({
                    'path': path,
                    'size': info['size'],
                    'old_hash': snapshot[path]['hash'],
                    'new_hash': info['hash'],
                    'old_mtime': snapshot[path].get('mtime_iso', 'Unknown'),
                    'new_mtime': info['mtime_iso']
                })
            else:
                unchanged.append(path)
        
        # Check for deleted files
        for path in snapshot:
            if path not in current_files:
                deleted.append({
                    'path': path,
                    'old_hash': snapshot[path]['hash']
                })
        
        return {
            'added': added,
            'modified': modified,
            'deleted': deleted,
            'unchanged': unchanged,
            'total_changes': len(added) + len(modified) + len(deleted)
        }
    
    def compare_local_to_github(self, project_root: str, repo_name: str, branch: str = "main") -> Dict:
        """
        Compare local files to GitHub repository
        
        Args:
            project_root: Path to local project
            repo_name: GitHub repository name
            branch: Branch to compare against
            
        Returns:
            Dict with differences between local and GitHub
        """
        local_files = self.scan_local_files(project_root)
        github_files = self.get_github_files(repo_name, branch)
        
        only_local = []
        only_github = []
        both = []
        
        for path in local_files:
            if path in github_files:
                both.append(path)
            else:
                only_local.append(path)
        
        for path in github_files:
            if path not in local_files:
                only_github.append(path)
        
        return {
            'only_local': only_local,
            'only_github': only_github,
            'both': both,
            'in_sync': len(only_local) == 0 and len(only_github) == 0,
            'total_differences': len(only_local) + len(only_github)
        }
    
    def get_github_recent_commits(self, repo_name: str, since_sha: Optional[str] = None, max_commits: int = 10) -> List[Dict]:
        """
        Get recent commits from GitHub
        
        Args:
            repo_name: Repository name
            since_sha: Only get commits after this SHA (optional)
            max_commits: Maximum number of commits to retrieve
            
        Returns:
            List of commit info dicts
        """
        commits_info = []
        
        try:
            user = self.gh_client.get_user()
            repo = user.get_repo(repo_name)
            
            commits = repo.get_commits()
            
            found_since = since_sha is None
            count = 0
            
            for commit in commits:
                if count >= max_commits:
                    break
                
                if not found_since:
                    if commit.sha == since_sha:
                        found_since = True
                    continue
                
                commits_info.append({
                    'sha': commit.sha,
                    'message': commit.commit.message,
                    'author': commit.commit.author.name,
                    'date': commit.commit.author.date.isoformat(),
                    'url': commit.html_url
                })
                count += 1
        
        except Exception as e:
            print(f"Error getting commits: {e}")
        
        return commits_info
    
    def detect_changes(self, repo_name: str) -> Dict:
        """
        Comprehensive change detection for a project
        
        Args:
            repo_name: Repository name to check
            
        Returns:
            Dict with all detected changes and sync status
        """
        # Get project from database
        project = self.project_db.get_project_by_repo(repo_name)
        
        if not project:
            return {
                'error': f"Project '{repo_name}' not found in database",
                'status': 'not_found'
            }
        
        project_root = project['local_path']
        last_commit_sha = project.get('metadata', {}).get('commit_sha')
        last_snapshot = project.get('metadata', {}).get('file_snapshot', {})
        
        # Scan current state
        current_files = self.scan_local_files(project_root)
        github_files = self.get_github_files(repo_name)
        
        # Compare local to last snapshot (detect local changes)
        local_changes = self.compare_local_to_snapshot(project_root, last_snapshot) if last_snapshot else None
        
        # Compare local to GitHub (detect sync status)
        sync_status = self.compare_local_to_github(project_root, repo_name)
        
        # Get recent GitHub commits
        github_commits = self.get_github_recent_commits(repo_name, since_sha=last_commit_sha, max_commits=5)
        
        # Determine overall status
        has_local_changes = local_changes and local_changes['total_changes'] > 0
        has_github_changes = len(github_commits) > 0
        is_synced = sync_status['in_sync']
        
        if has_local_changes and has_github_changes:
            status = "changes_both"
            message = "Changes detected both locally and on GitHub"
        elif has_local_changes:
            status = "changes_local"
            message = "Changes detected locally (not on GitHub yet)"
        elif has_github_changes:
            status = "changes_github"
            message = "New commits on GitHub (not pulled locally)"
        elif not is_synced:
            status = "out_of_sync"
            message = "Local and GitHub are out of sync"
        else:
            status = "in_sync"
            message = "Project is in sync"
        
        return {
            'status': status,
            'message': message,
            'project': {
                'name': project['name'],
                'uuid': project['uuid'],
                'local_path': project_root,
                'repo_name': repo_name
            },
            'local_changes': local_changes,
            'sync_status': sync_status,
            'github_commits': github_commits,
            'current_files_count': len(current_files),
            'github_files_count': len(github_files),
            'last_known_commit': last_commit_sha
        }
    
    def update_snapshot(self, repo_name: str) -> bool:
        """
        Update the file snapshot in the database for a project
        
        Args:
            repo_name: Repository name
            
        Returns:
            True if successful
        """
        project = self.project_db.get_project_by_repo(repo_name)
        
        if not project:
            print(f"Project '{repo_name}' not found")
            return False
        
        project_root = project['local_path']
        current_files = self.scan_local_files(project_root)
        
        # Update database with new snapshot
        self.project_db.update_project(
            project['uuid'],
            {
                'metadata': {
                    **project.get('metadata', {}),
                    'file_snapshot': current_files,
                    'snapshot_updated_at': datetime.now().isoformat()
                }
            }
        )
        
        print(f"Updated snapshot for '{repo_name}' with {len(current_files)} files")
        return True
    
    def format_changes_report(self, changes: Dict) -> str:
        """
        Format change detection results into a readable report
        
        Args:
            changes: Output from detect_changes()
            
        Returns:
            Formatted string report
        """
        if changes.get('status') == 'not_found':
            return changes.get('error', 'Unknown error')
        
        report = f"""
🔍 CHANGE DETECTION REPORT
{'=' * 60}

**Project**: {changes['project']['name']}
**Status**: {changes['message']}
**UUID**: {changes['project']['uuid']}
**Local Path**: {changes['project']['local_path']}
**Repository**: {changes['project']['repo_name']}

"""
        
        # Local changes
        if changes['local_changes']:
            lc = changes['local_changes']
            report += f"""
📁 LOCAL CHANGES (since last snapshot):
- Added: {len(lc['added'])} files
- Modified: {len(lc['modified'])} files
- Deleted: {len(lc['deleted'])} files
- Unchanged: {len(lc['unchanged'])} files

"""
            if lc['added']:
                report += "  **Added Files**:\n"
                for f in lc['added'][:5]:
                    report += f"    - {f['path']} ({f['size']} bytes)\n"
                if len(lc['added']) > 5:
                    report += f"    ... and {len(lc['added']) - 5} more\n"
            
            if lc['modified']:
                report += "  **Modified Files**:\n"
                for f in lc['modified'][:5]:
                    report += f"    - {f['path']} (changed at {f['new_mtime']})\n"
                if len(lc['modified']) > 5:
                    report += f"    ... and {len(lc['modified']) - 5} more\n"
            
            if lc['deleted']:
                report += "  **Deleted Files**:\n"
                for f in lc['deleted'][:5]:
                    report += f"    - {f['path']}\n"
                if len(lc['deleted']) > 5:
                    report += f"    ... and {len(lc['deleted']) - 5} more\n"
        
        # GitHub commits
        if changes['github_commits']:
            report += f"""
📡 GITHUB CHANGES (new commits):
{len(changes['github_commits'])} new commit(s) since last check

"""
            for commit in changes['github_commits']:
                report += f"  **{commit['sha'][:7]}** - {commit['message'].split(chr(10))[0]}\n"
                report += f"    Author: {commit['author']} | Date: {commit['date']}\n"
                report += f"    URL: {commit['url']}\n\n"
        
        # Sync status
        sync = changes['sync_status']
        report += f"""
🔄 SYNC STATUS:
- Files in both: {len(sync['both'])}
- Only local: {len(sync['only_local'])}
- Only GitHub: {len(sync['only_github'])}
- In sync: {'✅ Yes' if sync['in_sync'] else '❌ No'}

"""
        
        if sync['only_local']:
            report += "  **Only Local** (not on GitHub):\n"
            for f in sync['only_local'][:5]:
                report += f"    - {f}\n"
            if len(sync['only_local']) > 5:
                report += f"    ... and {len(sync['only_local']) - 5} more\n"
        
        if sync['only_github']:
            report += "  **Only GitHub** (not local):\n"
            for f in sync['only_github'][:5]:
                report += f"    - {f}\n"
            if len(sync['only_github']) > 5:
                report += f"    ... and {len(sync['only_github']) - 5} more\n"
        
        report += "\n" + "=" * 60
        
        return report
