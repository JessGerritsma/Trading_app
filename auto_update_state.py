import os
from datetime import datetime

# CONFIG
VAULT_DIR = "AI-Trading-Brain"
TARGET_FILE = os.path.join(VAULT_DIR, "00_Overview", "_current_state.md")
SCAN_FOLDERS = ["02_Strategies", "04_Logs", "05_Code"]

def get_recent_files(folder, count=2):
    full_path = os.path.join(VAULT_DIR, folder)
    files = [os.path.join(full_path, f) for f in os.listdir(full_path) if f.endswith(".md")]
    files.sort(key=os.path.getmtime, reverse=True)
    return files[:count]

def summarize_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        title = lines[0].strip() if lines else os.path.basename(file_path)
        body = [line.strip() for line in lines[1:10] if line.strip()]
        summary = "\n".join(f"- {line}" for line in body[:5])
        return f"### {title}\n{summary}\n"

def generate_summary():
    sections = []
    for folder in SCAN_FOLDERS:
        section = f"## 🔍 Summary from `{folder}`\n"
        for file in get_recent_files(folder):
            section += summarize_file(file)
        sections.append(section)
    return "\n\n".join(sections)

def update_state_file():
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📌 Current State (Auto-generated)\n")
        f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(generate_summary())
    print("✅ _current_state.md updated.")

if __name__ == "__main__":
    update_state_file()
