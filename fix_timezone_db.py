"""
Quick script to fix the timezone-weather-api database entry
"""
from tools.project_db import get_db

db = get_db()

# Get the project
project = db.get_project_by_repo("timezone-weather-api")

if project:
    print(f"Found project: {project['name']}")
    print(f"UUID: {project['uuid']}")
    print(f"Current metadata: {project.get('metadata', {})}")
    
    # Update with the latest commit info
    db.update_project(
        project['uuid'],
        {
            "metadata": {
                **project.get('metadata', {}),
                "last_commit": {
                    "sha": "073f846882cc0e04f762987b71e7dc1f3b05a8d6",
                    "message": "Added 5-day weather forecast and humorous weather messages",
                    "type": "update",
                    "branch": "main",
                    "note": "Updated via scaffold generator (should use update_project_ai next time)"
                }
            }
        }
    )
    
    print("\n✅ Updated project metadata")
    print("\nNOTE: Next time use the update_project_ai function instead of regenerating the scaffold!")
    print("Example: 'Update timezone-weather-api to add feature X'")
    print("The LLM will now call update_project_ai() which creates a PR instead of committing directly.")

else:
    print("Project not found!")
