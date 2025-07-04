
Project: AI Trading App  
Vault Path: `D:/Trading_app/obsidian`  
Task Folder: `09_Tasks/`

---
 ## ✅ Status Overview
---
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

```dataview

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
```dataviewjs
const tasks = dv.pages('"09_Tasks"')
    .where(p => p.project === "Trading App");

const grouped = {
    Frontend: [],
    Backend: [],
    Other: []
};

for (let task of tasks) {
    const tags = task.tags || [];
    if (tags.includes("frontend")) {
        grouped.Frontend.push(task);
    } else if (tags.includes("backend")) {
        grouped.Backend.push(task);
    } else {
        grouped.Other.push(task);
    }
}

// Display the table for each group
for (let [area, items] of Object.entries(grouped)) {
    dv.header(3, `📁 ${area}`);
    dv.table(["Task", "Due", "Status"],
        items.map(p => [p.file.link, p.due, p.status]));
}
```

```dataview
list from "09_Tasks"
where project = "Trading App" and status = "in-progress"


```

```dataview
table due, priority
from "09_Tasks"
where project = "Trading App" and date(due) < date(today) and status != "done"
sort due asc

```

