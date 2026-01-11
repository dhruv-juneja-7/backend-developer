## Database.py

**How to remember the basic syntax**

- How to talk to database - _engine_
- How to open and close conversations - _session_
- How to create tables - _Base_

```
DATABASE_URL
   ↓
engine
   ↓
SessionLocal
   ↓
Base
```

**ORM vs Database Models**
Decision checklist (use this every time)

Ask:

**1️⃣ Am I defining a DB constraint?**

➡️ Use table.column

**2️⃣ Am I defining Python object navigation?**

➡️ Use class name
