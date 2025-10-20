#!/usr/bin/env python3
"""
Simple example showing JSON iteration and file creation
This demonstrates the core concept you requested
"""
import json
import os
from pathlib import Path


# Example JSON response from Claude
EXAMPLE_SCAFFOLD_JSON = '''
{
  "project_name": "example-api",
  "description": "Example Flask API project",
  "structure": {
    "folders": [
      "src",
      "src/controllers",
      "src/models",
      "tests",
      "config"
    ],
    "files": {
      "src/__init__.py": "",
      "src/app.py": "from flask import Flask\\n\\napp = Flask(__name__)\\n\\n@app.route('/')\\ndef hello():\\n    return {'message': 'Hello World'}",
      "src/controllers/__init__.py": "",
      "src/controllers/user_controller.py": "# User controller\\ndef get_users():\\n    return []",
      "src/models/__init__.py": "",
      "src/models/user.py": "class User:\\n    def __init__(self, name):\\n        self.name = name",
      "requirements.txt": "flask==2.3.0\\npython-dotenv==1.0.0",
      "README.md": "# Example API\\n\\n## Setup\\n\\n```bash\\npip install -r requirements.txt\\npython src/app.py\\n```",
      ".gitignore": "__pycache__/\\n*.pyc\\n.env\\nvenv/"
    }
  }
}
'''


def iterate_and_create_project(json_string: str, base_path: str = "."):
    """
    Core function: Iterate through JSON and create files/folders
    This is exactly what you asked for!
    """
    # Step 1: Parse JSON
    scaffold = json.loads(json_string)
    project_name = scaffold["project_name"]
    structure = scaffold["structure"]
    
    # Step 2: Create project directory
    project_path = Path(base_path) / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created project directory: {project_path}")
    
    # Step 3: Iterate through folders and create them
    print("\n📁 Creating folders:")
    for folder in structure["folders"]:
        folder_path = project_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {folder}")
    
    # Step 4: Iterate through files (key-value pairs) and create them
    print("\n📄 Creating files:")
    for file_path, content in structure["files"].items():
        full_path = project_path / file_path
        
        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file content
        full_path.write_text(content, encoding='utf-8')
        print(f"   ✓ {file_path} ({len(content)} bytes)")
    
    print(f"\n🎉 Project '{project_name}' created successfully!")
    print(f"📍 Location: {project_path.absolute()}")
    
    return project_path


def demonstrate_json_iteration():
    """
    Demonstrate how to iterate through the JSON structure
    """
    print("=" * 60)
    print("🔍 JSON ITERATION DEMONSTRATION")
    print("=" * 60)
    
    # Parse the example JSON
    scaffold = json.loads(EXAMPLE_SCAFFOLD_JSON)
    
    print("\n📋 Project Information:")
    print(f"   Name: {scaffold['project_name']}")
    print(f"   Description: {scaffold['description']}")
    
    structure = scaffold["structure"]
    
    print("\n📁 Folders (List):")
    for i, folder in enumerate(structure["folders"], 1):
        print(f"   {i}. {folder}")
    
    print("\n📄 Files (Dictionary - Key/Value Pairs):")
    for file_path, content in structure["files"].items():
        content_preview = content[:50].replace('\n', ' ')
        if len(content) > 50:
            content_preview += "..."
        print(f"   • {file_path}")
        print(f"     Content: {content_preview}")
        print(f"     Size: {len(content)} characters")
        print()


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("🚀 PROJECT SCAFFOLD - JSON ITERATION DEMO")
    print("=" * 60)
    
    # First, show how to iterate through JSON
    demonstrate_json_iteration()
    
    # Ask if user wants to create the project
    print("\n" + "=" * 60)
    response = input("Create this example project? (yes/no): ").strip().lower()
    
    if response == "yes":
        print("\n🔨 Creating project...")
        try:
            project_path = iterate_and_create_project(
                EXAMPLE_SCAFFOLD_JSON,
                base_path="./demo_projects"
            )
            
            print("\n✅ Success! You can now:")
            print(f"   cd {project_path}")
            print(f"   cat README.md")
            print(f"   tree {project_path}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    else:
        print("\n✋ Skipped project creation")
    
    print("\n" + "=" * 60)
    print("💡 KEY TAKEAWAY:")
    print("   1. Claude returns JSON with 'folders' (list) and 'files' (dict)")
    print("   2. You iterate through folders: for folder in folders:")
    print("   3. You iterate through files: for path, content in files.items():")
    print("   4. Create folders with mkdir, files with write_text()")
    print("=" * 60)
