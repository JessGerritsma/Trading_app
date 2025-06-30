
> Project: AI Trading App  
> Vault Path: `D:/Trading_app/obsidian`  
> Task Folder: `09_Tasks/`
> ---
 ## ✅ Status Overview
> ---
```dataview
table count(rows) as "Tasks"
from "09_Tasks"
where project = "Trading App"
group by status

```

```dataviewjs
const tasks = dv.pages('"09_Tasks"').where(p => p.project === "Trading App");
const total = tasks.length;
const done = tasks.filter(p => p.status == "done").length;
dv.paragraph(`✅ **Progress**: ${done} / ${total} (${Math.round((done / total) * 100)}%)`);

```

```
table status, due, priority
from "09_Tasks"
where project = "Trading App" and date(due) <= date(today) + dur(7 days)
sort due asc

```

```dataview
table due, priority, tags
from "09_Tasks"
where project = "Trading App"
group by status
sort due asc

```
```dataview
table status, due
from "09_Tasks"
where project = "Trading App"
group by contains(tags, "frontend") ? "Frontend" : contains(tags, "backend") ? "Backend" : "Other"
sort due asc

```

```dataview
list from "09_Tasks"
where project = "Trading App" and status = "in-progress"

```