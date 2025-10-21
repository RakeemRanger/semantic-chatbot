# Change Detection System

## Overview
The change detection system monitors projects for modifications made locally (by users or other agents) and on GitHub. It helps maintain awareness of project state changes across different sources.

## Purpose
- **Detect Local Changes**: Track file modifications, additions, and deletions made outside the chatbot
- **Detect GitHub Changes**: Monitor commits and changes pushed to GitHub
- **Sync Status**: Compare local files with GitHub to identify discrepancies
- **Snapshot Tracking**: Maintain baselines to detect what changed since last check
- **Multi-Agent Support**: Track changes made by other tools or developers

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Change Detection System                     │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  Local Scanner   │    │  GitHub Scanner  │
│                  │    │                  │
│ - File hashing   │    │ - Commit history │
│ - Metadata       │    │ - Tree scanning  │
│ - Timestamps     │    │ - SHA tracking   │
└────────┬─────────┘    └─────────┬────────┘
         │                        │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   Snapshot Comparison  │
         │                        │
         │ - Added files          │
         │ - Modified files       │
         │ - Deleted files        │
         │ - Sync status          │
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────┐
         │  Project Database  │
         │  (file_snapshot)   │
         └────────────────────┘
```

## Components

### 1. ChangeDetector Class (`tools/change_detector.py`)

Main class that handles all change detection operations.

**Key Methods:**

```python
# Scan local files and compute hashes
scan_local_files(project_root: str) -> Dict[str, Dict]

# Get files from GitHub repository
get_github_files(repo_name: str, branch: str) -> Dict[str, Dict]

# Compare current state to saved snapshot
compare_local_to_snapshot(project_root: str, snapshot: Dict) -> Dict

# Compare local files to GitHub
compare_local_to_github(project_root: str, repo_name: str) -> Dict

# Get recent commits from GitHub
get_github_recent_commits(repo_name: str, since_sha: str) -> List[Dict]

# Comprehensive change detection
detect_changes(repo_name: str) -> Dict

# Update snapshot in database
update_snapshot(repo_name: str) -> bool

# Format changes into readable report
format_changes_report(changes: Dict) -> str
```

### 2. File Snapshot Format

Each file in the snapshot has:

```json
{
  "path/to/file.py": {
    "hash": "sha256_hash_of_content",
    "size": 1234,
    "mtime": 1729456789.123,
    "mtime_iso": "2025-10-20T15:33:09.123456"
  }
}
```

### 3. Change Detection Result

```json
{
  "status": "changes_both|changes_local|changes_github|out_of_sync|in_sync",
  "message": "Human-readable status message",
  "project": {
    "name": "project-name",
    "uuid": "abc123...",
    "local_path": "/path/to/project",
    "repo_name": "repo-name"
  },
  "local_changes": {
    "added": [...],
    "modified": [...],
    "deleted": [...],
    "unchanged": [...],
    "total_changes": 5
  },
  "sync_status": {
    "only_local": [...],
    "only_github": [...],
    "both": [...],
    "in_sync": true|false,
    "total_differences": 2
  },
  "github_commits": [
    {
      "sha": "abc123...",
      "message": "Commit message",
      "author": "Author Name",
      "date": "2025-10-20T...",
      "url": "https://github.com/..."
    }
  ],
  "current_files_count": 42,
  "github_files_count": 40,
  "last_known_commit": "def456..."
}
```

## LLM Functions

### 1. `detect_project_changes(repo_name: str)`

Detects and reports all changes in a project.

**Usage**: 
```
User: "Check what changed in my timezone-weather-api project"
User: "Did anyone modify the project?"
User: "What's different since last time?"
```

**Returns**: Detailed report with:
- Local changes (added/modified/deleted files)
- GitHub commits (new commits since last check)
- Sync status (local vs GitHub)

**Example Output**:
```
🔍 CHANGE DETECTION REPORT
============================================================

**Project**: timezone-weather-api
**Status**: Changes detected locally (not on GitHub yet)
**UUID**: 8012cb68...
**Local Path**: /home/user/.dartinbot/projects/timezone-weather-api
**Repository**: timezone-weather-api

📁 LOCAL CHANGES (since last snapshot):
- Added: 2 files
- Modified: 3 files
- Deleted: 1 file
- Unchanged: 35 files

  **Added Files**:
    - app/new_feature.py (1234 bytes)
    - tests/test_new_feature.py (567 bytes)

  **Modified Files**:
    - app/main.py (changed at 2025-10-20T15:33:09)
    - README.md (changed at 2025-10-20T15:30:15)
    - requirements.txt (changed at 2025-10-20T15:28:42)

  **Deleted Files**:
    - old_file.py

🔄 SYNC STATUS:
- Files in both: 38
- Only local: 2
- Only GitHub: 0
- In sync: ❌ No

  **Only Local** (not on GitHub):
    - app/new_feature.py
    - tests/test_new_feature.py

============================================================
```

### 2. `update_project_snapshot(repo_name: str)`

Updates the baseline snapshot in the database.

**Usage**:
```
User: "Update the snapshot for timezone-weather-api"
User: "Save the current state as baseline"
```

**Returns**: Success/failure message

**When to Use**:
- After making approved changes
- After pulling from GitHub
- To establish new baseline for future comparisons

### 3. Integration with Other Functions

Change detection is automatically called by:

**`commit_project()`**:
- Creates initial snapshot when project is created
- Stores in database for future comparisons

**`update_project_ai()`**:
- Updates snapshot after successful PR creation
- Tracks new baseline after changes

## Use Cases

### Use Case 1: User Makes Manual Changes

**Scenario**: User edits files directly in VS Code

```
1. User modifies app/main.py locally
2. LLM: detect_project_changes("my-project")
3. Report shows: "1 file modified locally"
4. LLM can decide to:
   - Incorporate changes into next update
   - Ask user if they want to commit
   - Update snapshot to acknowledge changes
```

### Use Case 2: Another Agent Modifies Project

**Scenario**: GitHub Copilot or another tool creates files

```
1. Another agent adds new_feature.py
2. LLM: detect_project_changes("my-project")
3. Report shows: "1 file added locally"
4. LLM can:
   - Review the new file
   - Commit it to GitHub
   - Update related files
   - Update snapshot
```

### Use Case 3: Commits Pushed to GitHub

**Scenario**: User pushes directly to GitHub

```
1. User commits and pushes via git CLI
2. LLM: detect_project_changes("my-project")
3. Report shows: "2 new GitHub commits"
4. LLM can:
   - List the commits
   - Warn that local is behind
   - Suggest syncing local with GitHub
```

### Use Case 4: Out of Sync Detection

**Scenario**: Local and GitHub diverged

```
1. User modifies files locally
2. Someone else pushes to GitHub
3. LLM: detect_project_changes("my-project")
4. Report shows: "Changes detected both locally and on GitHub"
5. LLM can:
   - Warn about potential conflicts
   - Suggest pulling from GitHub first
   - Help resolve conflicts
```

## File Hashing

Uses **SHA256** for file hashing:
- Fast and reliable
- Detects any content changes
- Industry standard
- No false positives

**Why Hashing?**
- More reliable than timestamps alone
- Detects content changes even if timestamp unchanged
- Works across systems with different time zones
- Handles timezone/DST issues

## Snapshot Strategy

**When Snapshots Are Created/Updated**:

1. **Initial Creation** (`commit_project`):
   - Scans all files
   - Computes hashes
   - Stores in database metadata

2. **After Updates** (`update_project_ai`):
   - Rescans modified project
   - Updates snapshot with new hashes
   - Preserves history of what was baseline

3. **Manual Updates** (`update_project_snapshot`):
   - User/LLM triggers explicit snapshot
   - Establishes new baseline
   - Resets change detection

**Snapshot Storage**:
```json
{
  "metadata": {
    "file_snapshot": {
      "file1.py": {"hash": "...", "size": 123, "mtime": ...},
      "file2.py": {"hash": "...", "size": 456, "mtime": ...}
    },
    "snapshot_created_at": "2025-10-20T...",
    "snapshot_updated_at": "2025-10-20T..."
  }
}
```

## GitHub Integration

**Commit Tracking**:
- Queries GitHub API for recent commits
- Compares against last known commit SHA
- Shows commit messages, authors, dates
- Provides URLs to view commits

**Tree Scanning**:
- Uses GitHub's tree API
- Gets recursive file list
- Compares with local files
- Identifies files only on one side

## Performance Considerations

**Local Scanning**:
- Skips common directories: `.git`, `node_modules`, `__pycache__`, etc.
- Skips hidden files (starting with `.`)
- Efficient file walking
- Caches results in memory

**GitHub API**:
- Uses recursive tree API (single call)
- Paginates commits as needed
- Rate limit aware
- Caches authentication

**Hash Computation**:
- Reads files in binary mode
- Streams large files
- Uses SHA256 (fast and secure)
- Only computes when needed

## Error Handling

**Graceful Degradation**:
- If local scan fails → returns empty result, logs error
- If GitHub API fails → returns cached/partial data
- If database fails → operation continues, warns user
- If file read fails → skips file, continues scan

**Error Messages**:
- Clear, actionable messages
- Suggests resolution steps
- Logs technical details for debugging
- User-friendly formatting

## Example Workflow

### Complete Change Detection Flow

```
1. User: "Check my timezone-weather-api for changes"

2. LLM calls: detect_project_changes("timezone-weather-api")

3. System:
   a. Gets project from database
   b. Loads last snapshot
   c. Scans current local files
   d. Computes hashes
   e. Compares to snapshot → finds 3 modified files
   f. Queries GitHub API
   g. Gets commits since last known SHA → finds 2 new commits
   h. Compares local to GitHub → finds 1 file only local
   i. Generates comprehensive report

4. LLM presents report:
   "I found changes in your project:
   - 3 files were modified locally
   - 2 new commits on GitHub
   - 1 file exists locally but not on GitHub
   
   Would you like me to sync these changes?"

5. User: "Yes, commit the local changes"

6. LLM calls: update_project_ai("timezone-weather-api", "Commit recent modifications")

7. System:
   a. Creates feature branch
   b. Commits changes
   c. Creates PR
   d. Updates snapshot (new baseline)

8. LLM: "Done! PR #42 created. Snapshot updated."
```

## Testing

Run the test script:

```bash
python3 test_change_detection.py
```

**Tests Include**:
1. Detect initial state
2. Make local change
3. Detect new change
4. Update snapshot
5. Verify no changes after snapshot
6. Delete file
7. Detect deletion

## Integration Points

### source_control.py

**Added Functions**:
- `detect_project_changes(repo_name)` - LLM kernel function
- `update_project_snapshot(repo_name)` - LLM kernel function

**Modified Functions**:
- `commit_project()` - Creates initial snapshot
- `update_project()` - Updates snapshot after changes

### project_db.py

**Storage Fields**:
- `metadata.file_snapshot` - Dictionary of file hashes
- `metadata.snapshot_created_at` - Timestamp
- `metadata.snapshot_updated_at` - Timestamp

## Future Enhancements

1. **Diff Generation**: Show actual file diffs, not just changed files
2. **Smart Merging**: Auto-merge non-conflicting changes
3. **Conflict Detection**: Warn about merge conflicts before they happen
4. **Change History**: Track history of all changes over time
5. **Rollback**: Restore previous states from snapshots
6. **Ignore Patterns**: Respect .gitignore for scanning
7. **Branch Awareness**: Track changes per branch
8. **Real-time Monitoring**: File system watchers for instant detection
9. **Change Statistics**: Graphs and metrics of change frequency
10. **Multi-User Tracking**: Attribute changes to specific users/agents

## Conclusion

The change detection system provides complete visibility into project modifications, whether made by the chatbot, users, other agents, or via GitHub. It enables intelligent decision-making about project state and helps maintain synchronization across different sources.
