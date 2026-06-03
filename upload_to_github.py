import os
import urllib.request
import json
import base64

# Config
OWNER = "harshsinghps57-spec"
REPO = "Exploratory-Data-Analysis-and-Business-Intelligence"

print("=====================================================================")
print("GITHUB REPOSITORY UPLOADER")
print("=====================================================================")

# Prompt for Personal Access Token
token = os.environ.get("GITHUB_TOKEN")
if not token:
    print("Please set your GitHub Personal Access Token (PAT) with repo write permissions.")
    print("You can get one from: https://github.com/settings/tokens")
    token = input("Enter your GitHub PAT: ").strip()

if not token:
    print("[ERROR] GitHub Token is required to upload files!")
    exit(1)

# File paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Files to upload
files_to_upload = []
exclude_dirs = {".git", "__pycache__", "node_modules", "brain", ".gemini", "scratch"}
exclude_files = {"setup_week2.py", "download_repo.py"}

# Walk directory tree
for root, dirs, files in os.walk(BASE_DIR):
    # Prune excluded directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file in exclude_files:
            continue
        # Get absolute path
        abs_path = os.path.join(root, file)
        # Get relative path for GitHub path
        rel_path = os.path.relpath(abs_path, BASE_DIR).replace("\\", "/")
        files_to_upload.append((abs_path, rel_path))

print(f"Found {len(files_to_upload)} files to upload.")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Superstore-BI-Uploader"
}

def upload_file(abs_path, github_path):
    # Read file content
    with open(abs_path, "rb") as f:
        content = f.read()
    
    # Check size
    file_size_mb = len(content) / (1024 * 1024)
    if file_size_mb > 50:
        print(f"[WARNING] Skipping {github_path} (File is too large: {file_size_mb:.1f}MB)")
        return
        
    encoded_content = base64.b64encode(content).decode("utf-8")
    
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{github_path}"
    
    # Check if file already exists to get its SHA (for update)
    sha = None
    req_check = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req_check) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            sha = res_data.get("sha")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[ERROR] Checking {github_path}: {e}")
            return
            
    # Prepare payload
    data = {
        "message": f"Upload {github_path} - Week 2 Deliverable",
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha
        
    req_body = json.dumps(data).encode("utf-8")
    req_upload = urllib.request.Request(url, data=req_body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req_upload) as response:
            print(f"[SUCCESS] Uploaded: {github_path}")
    except urllib.error.HTTPError as e:
        res_err = e.read().decode("utf-8")
        print(f"[ERROR] Failed to upload {github_path}: {e.code} - {res_err}")

# Upload each file
for abs_path, rel_path in files_to_upload:
    upload_file(abs_path, rel_path)

print("\nUpload process completed!")
