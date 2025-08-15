#!/usr/bin/env python3
"""
Utility script to add new projects to the projects list in app.py
This makes it easy to expand the project portfolio without manually editing the main app file.
"""

import json
from datetime import datetime

def create_project():
    """Interactive project creation utility"""
    print("✨ Team M&I - Project Addition Utility ✨")
    print("=" * 50)
    
    # Get project details
    project_id = input("Project ID (e.g., 'my-new-app'): ").strip()
    title = input("Project Title (with emoji): ").strip()
    description = input("Project Description: ").strip()
    category = input("Category (Web App, Portfolio, Mobile, etc.): ").strip()
    status = input("Status (Live Demo, Interactive, Live, etc.): ").strip()
    
    print("\nTechnologies (comma-separated):")
    technologies = [tech.strip() for tech in input("e.g., Flask, Python, CSS3: ").split(",")]
    
    print("\nKey Features (comma-separated):")
    features = [feature.strip() for feature in input("e.g., Responsive design, API integration: ").split(",")]
    
    link = input("Project Link (e.g., /my-project): ").strip()
    github = input("GitHub Link (optional, press Enter to skip): ").strip() or None
    image = input("Image Path (optional, press Enter to skip): ").strip() or None
    
    # Auto-assign priority (you can adjust this logic)
    priority = len(technologies) + len(features)  # Simple priority calculation
    
    # Create project dictionary
    project = {
        "id": project_id,
        "title": title,
        "description": description,
        "category": category,
        "status": status,
        "technologies": technologies,
        "features": features,
        "link": link,
        "github": github,
        "image": image,
        "priority": priority
    }
    
    return project

def generate_python_code(project):
    """Generate Python code to add to app.py"""
    python_code = f"""
    {{
        "id": "{project['id']}",
        "title": "{project['title']}",
        "description": "{project['description']}",
        "category": "{project['category']}",
        "status": "{project['status']}",
        "technologies": {json.dumps(project['technologies'])},
        "features": {json.dumps(project['features'])},
        "link": "{project['link']}",
        "github": {json.dumps(project['github'])},
        "image": {json.dumps(project['image'])},
        "priority": {project['priority']}
    }},"""
    
    return python_code

def main():
    """Main function"""
    try:
        project = create_project()
        
        print("\n" + "=" * 50)
        print("✨ Project Created Successfully! ✨")
        print("=" * 50)
        
        # Display the project
        print(f"Project ID: {project['id']}")
        print(f"Title: {project['title']}")
        print(f"Category: {project['category']}")
        print(f"Status: {project['status']}")
        print(f"Technologies: {', '.join(project['technologies'])}")
        print(f"Features: {', '.join(project['features'])}")
        print(f"Link: {project['link']}")
        print(f"Priority: {project['priority']}")
        
        # Generate Python code
        python_code = generate_python_code(project)
        
        print("\n" + "=" * 50)
        print("📝 Python Code to Add to app.py:")
        print("=" * 50)
        print("Add this to the projects list in app.py:")
        print(python_code)
        
        # Save to JSON file for backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"project_{project['id']}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(project, f, indent=2)
        
        print(f"\n💾 Project saved to {filename}")
        print("\n📋 Instructions:")
        print("1. Copy the Python code above")
        print("2. Open app.py")
        print("3. Find the projects list")
        print("4. Add the new project entry")
        print("5. Restart your Flask app")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
