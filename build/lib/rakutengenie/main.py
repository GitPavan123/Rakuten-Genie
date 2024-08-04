import os
import sys
import json
import threading
import itertools
import google.generativeai as genai
from dotenv import load_dotenv
import time

# initializing the google gemini llm with the api key 
def load_api_key():
    load_dotenv()
    api_key = os.getenv("GOOGLE_GEMINI_API")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# Replicating the folder structure(Project metadata) of the current working directory
def gather_project_info(project_dir):
    def get_folder_structure(dir_path):
        folder_structure = []
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path):
                folder_structure.append([item] + get_folder_structure(item_path))
            else:
                folder_structure.append(item)
        return folder_structure

    project_info = {
        'folder_structure': get_folder_structure(project_dir)
    }

    # Detecting project type based on package manager
    if os.path.exists(os.path.join(project_dir, 'requirements.txt')):
        project_info['language'] = 'Python'
        project_info['dependencies_file'] = 'requirements.txt'
        project_info['python_version'] = f"{sys.version_info.major}.{sys.version_info.minor}"
    elif os.path.exists(os.path.join(project_dir, 'package.json')):
        project_info['language'] = 'JavaScript'
        project_info['dependencies_file'] = 'package.json'
    
    return project_info

# Generating custom docker file based on the projects's metadata being prepared
def generate_dockerfile(project_info):
    model = load_api_key()
    folder_structure_json = json.dumps(project_info['folder_structure'])
    
    python_version = project_info.get('python_version')
    python_image = f"python:{python_version}-slim" if python_version else "python:latest"

    # Query prompt
    prompt = (
        f"Generate a Dockerfile for a project with the following folder structure:\n"
        f"{folder_structure_json}\n\n"
        f"The project is written in {project_info.get('language', 'unknown')} "
        f"and has dependencies listed in {project_info.get('dependencies_file', 'unknown')}. "
        f"Use the Docker image '{python_image}' for the Python environment. "
        f"Don't specify any other things other that the dockerfile"
        f"But do provide comments for each line"
    )
    
    response = model.generate_content(prompt)
    dockerfile_content = response.text

    lines = dockerfile_content.splitlines()

    if len(lines) > 2:
        lines = lines[1:-1]
    elif len(lines) == 2:
        lines = []

    cleaned_dockerfile_content = "\n".join(lines)

    return cleaned_dockerfile_content

# CLI loading animation logic
def loading_animation(done_event):
    for char in itertools.cycle('|/-\\'):
        if done_event.is_set():
            break
        sys.stdout.write(f'\rGenerating Dockerfile... {char}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDockerfile generated!     \n')

# Main function responsible for integration of various functions
def main():
    project_dir = os.getcwd()  
    
    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a valid directory.")
        sys.exit(1)
    
    project_info = gather_project_info(project_dir)
    if not project_info:
        print("Error: Could not determine project details.")
        sys.exit(1)
    
    output_path = os.path.join(project_dir, 'Dockerfile')
    
    if os.path.exists(output_path):
        response = input("A Dockerfile already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if response != 'y':
            print("Aborting operation. No changes were made.")
            sys.exit(0)
    
    done_event = threading.Event()
    loader_thread = threading.Thread(target=loading_animation, args=(done_event,))
    loader_thread.start()

    dockerfile_content = generate_dockerfile(project_info)
    
    done_event.set()
    loader_thread.join()
    
    with open(output_path, 'w') as f:
        f.write(dockerfile_content)
    
    print(f"Dockerfile created at {output_path}")

if __name__ == "__main__":
    main()
