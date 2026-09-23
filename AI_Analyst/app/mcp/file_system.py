import os

sandbox_path = os.path.abspath(
    os.path.join(os.getcwd(), "sandbox")
)
os.makedirs(sandbox_path, exist_ok=True)
files_params = {
    "command": "npx",
    "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        sandbox_path
    ]
}