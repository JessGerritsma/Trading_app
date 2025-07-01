import json
from pathlib import Path

json_path = Path("../../apps/backend/data/chat_history.json")
md_path = Path("chat_history.md")

with open(json_path, "r", encoding="utf-8") as f:
    history = json.load(f)

with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Chat History Log\n\n")
    for entry in history:
        f.write(f"---\n**{entry['timestamp']}**\nUser: {entry['user']}\nAI: {entry['ai']}\n\n")

print(f"Exported {len(history)} chat entries to {md_path}") 