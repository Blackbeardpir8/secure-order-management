import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ❌ DIRECTORIES TO NEVER ENTER
EXCLUDE_DIRS = {
    "__pycache__", "node_modules", "migrations", "venv",
    ".git", ".idea", ".vscode", ".pytest_cache",
    "build", "dist",
    "collectstatic", "static", "media",
    "rest_framework", "admin",
    "fonts", "css", "js", "img",
}

# ❌ FILE TYPES TO SKIP
EXCLUDE_EXTENSIONS = {
    ".svg", ".png", ".jpg", ".jpeg", ".gif",
    ".woff", ".woff2", ".ttf", ".eot",
    ".map"
}

def generate_tree(path, prefix=""):
    try:
        items = sorted(os.listdir(path))
    except (FileNotFoundError, PermissionError):
        return

    visible_items = []

    for item in items:
        if item.startswith("."):
            continue

        full_path = os.path.join(path, item)

        # 🚫 BLOCK directories BEFORE recursion
        if os.path.isdir(full_path):
            if item in EXCLUDE_DIRS:
                continue
            visible_items.append(item)

        else:
            ext = os.path.splitext(item)[1].lower()
            if ext not in EXCLUDE_EXTENSIONS:
                visible_items.append(item)

    for index, item in enumerate(visible_items):
        full_path = os.path.join(path, item)
        connector = "|-- " if index != len(visible_items) - 1 else "`-- "
        print(prefix + connector + item)

        if os.path.isdir(full_path):
            extension = "|   " if index != len(visible_items) - 1 else "    "
            generate_tree(full_path, prefix + extension)

if __name__ == "__main__":
    project_name = os.path.basename(os.getcwd())

    print("```bash")
    print(f"{project_name}/")
    generate_tree(".")
    print("```")

# Run:
# python generate_clean_tree.py > clean_tree.md
