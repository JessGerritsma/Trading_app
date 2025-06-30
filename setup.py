import os

folders = [
    "01_Idea_Log",
    "02_Progress_Updates",
    "03_AI_Insights",
    "04_Research",
    "05_Code",
    "06_Data",
    "07_Results",
    "08_Templates"
]

templates = {
    "08_Templates/update_state.md": """---
creation_date: <% tp.date.now("YYYY-MM-DD") %>
tags: [update]
---

# 🧠 Daily Update - <% tp.date.now("YYYY-MM-DD") %>

## 🗓️ Date
<% tp.date.now("dddd, MMMM Do YYYY") %>

## 🔄 What changed?
- 

## 📈 Trades Taken
- 

## 🤖 AI Tools Used
- 

## 💡 Insights
- 

## ⏭️ Next Steps
- 
"""
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file_path, content in templates.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Vault structure rebuilt.")
