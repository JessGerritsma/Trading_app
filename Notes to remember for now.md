---
status: todo
priority: high
due: 2025-07-05
tags: [backend, api]
---
put the above into task or project notes can customize the fields to relevant info

### How to organize:

| Content Type                         | Where to put it                                                                            | Example or Purpose                                                                                  |                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Markdown** (tasks, notes, queries) | Inside your `project_todo.md` or other `.md` notes in `/09_Tasks/` folder                  | Contains your task lists and Dataview queries to display/filter them dynamically.                   | # Project TODO List<br><br>```dataview<br>table status, priority, due<br>from "09_Tasks"<br>where status != "done"<br>sort due asc<br>                                                                                                                                                                                                                                           |
| **YAML frontmatter**                 | At the very top of each Markdown note where you want metadata (e.g. task status, priority) | Helps Dataview filter and organize your notes/tasks. Example: `--- status: todo priority: high ---` | <br>This will show a table of all notes under `09_Tasks` folder where `status` is not done, sorted by due date.<br><br>---<br><br>## ✅ Step 4: Use Inline Task Queries<br><br>You can also show all tasks with a specific tag or priority:<br><br>```markdown<br>```dataview<br>task from "09_Tasks"<br>where contains(tags, "backend") and !completed<br>sort priority desc<br> |
| **SQL**                              | Not used directly in Obsidian (Dataview doesn’t run SQL)                                   | Ignore SQL unless you use an external DB; Dataview uses its own query language inside Markdown.     | <br>---<br><br>## ✅ Step 5: Tag & Update Tasks in Your Notes<br><br>In any note inside your task folder, write tasks like this:<br><br>```markdown<br>- [ ] Implement API client #backend #priority-high<br>- [x] Write AI trading logic #backend #done<br>                                                                                                                      |

This will show a table of all notes under `09_Tasks` folder where `status` is not done, sorted by due date.

---

