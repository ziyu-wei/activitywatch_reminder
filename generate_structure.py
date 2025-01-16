import os

def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)

def main():
    # Define the structure
    os.makedirs("activitywatch-reminder/src", exist_ok=True)
    
    # Create files with content
    create_file("activitywatch-reminder/README.md", "# ActivityWatch Reminder\\n\\nProject details here.")
    create_file("activitywatch-reminder/.gitignore", "*.pyc\\n__pycache__/\\nenv/\\n.DS_Store")
    create_file("activitywatch-reminder/requirements.txt")
    create_file("activitywatch-reminder/src/main.py")
    create_file("activitywatch-reminder/src/aw_api.py")
    create_file("activitywatch-reminder/src/config.py")
    create_file("activitywatch-reminder/src/notifier.py")
    
    print("Project structure created successfully!")

if __name__ == "__main__":
    main()
