import os

def create_project_structure():
    # Define project structure
    structure = {
        "data": ["raw", "processed"],
        "scripts": ["data_collection.py", "preprocessing.py", "model.py", "evaluation.py"],
        "models": [],
        "results": [],
        "root": ["main.py", "requirements.txt"]
    }

    # Create directories and files
    for folder, contents in structure.items():
        if folder == "root":
            for file in contents:
                with open(file, "w") as f:
                    f.write("# Placeholder for {}\n".format(file))
            continue

        os.makedirs(folder, exist_ok=True)
        for content in contents:
            if ".py" in content:
                with open(os.path.join(folder, content), "w") as f:
                    f.write("# Placeholder for {}\n".format(content))

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()