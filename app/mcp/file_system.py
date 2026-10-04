import os

import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sandbox_path = os.path.join(PROJECT_ROOT, "sandbox")
os.makedirs(sandbox_path, exist_ok=True)

files_params = {
    "command": "npx",
    "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        sandbox_path
    ]
}