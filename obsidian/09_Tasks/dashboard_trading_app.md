# 📊 Trading App Project Dashboard

> Project: AI Trading App  
> Vault Path: `D:/Trading_app/obsidian`  
> Task Folder: `09_Tasks/`  

---

## ✅ Status Overview

```dataview
table count(rows) as "Tasks"
from "09_Tasks"
where project = "Trading App"
group by status
