# Chat History Log (Auto-Generated)

> This file is auto-generated from `apps/backend/data/chat_history.json`.
> To update, run the script below or set up an Obsidian plugin/task to automate it.

---

## How to update this file

Run the following script (Python 3):

```python
import json
from pathlib import Path

json_path = Path("apps/backend/data/chat_history.json")
md_path = Path("obsidian/04_Logs/chat_history.md")

with open(json_path, "r", encoding="utf-8") as f:
    history = json.load(f)

with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Chat History Log\n\n")
    for entry in history:
        f.write(f"---\n**{entry['timestamp']}**\nUser: {entry['user']}\nAI: {entry['ai']}\n\n")
```

You can automate this with a scheduled task or Obsidian plugin.

--- 