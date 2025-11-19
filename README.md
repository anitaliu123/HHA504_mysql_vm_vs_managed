# HHA504 – MySQL on VM vs Managed (GCP + SQLAlchemy + pandas)

This repo implements the HHA504 assignment comparing:

1. **Self-managed MySQL on a Google Compute Engine VM**
2. **Managed MySQL using Cloud SQL for MySQL**

Both are accessed from Python using **SQLAlchemy + pandas**. 
Each script:

- Loads credentials from `.env`
- Ensures a database exists
- Creates a `visits` table via `pandas.to_sql`
- Inserts 5 rows
- Reads back the row count with `pd.read_sql`

---

## 1. Cloud & Region

- **Cloud:** Google Cloud Platform  
- **VM zone:** `us-central1-a` 
- **Cloud SQL region:** `us-central1`  

## 2. Repository Layout

```text
HHA504_mysql_vm_vs_managed/
├─ README.md
├─ .gitignore                  # Make sure to ignore your .env 
├─ .env.example                # Do NOT commit real secrets
├─ scripts/
│   ├─ vm_demo.py              # SQLAlchemy+pandas against VM MySQL
│   └─ managed_demo.py         # SQLAlchemy+pandas against managed MySQL
├─ sql/
│   └─ init.sql                # Optional: user/db bootstrap you ran on VM
├─ screenshots/
│   ├─ vm/                     # VM portal, firewall, daemon status, CLI, etc.
│   └─ managed/                # Managed service creation, connection details
└─ docs/
    ├─ setup_notes_vm.md
    ├─ setup_notes_managed.md
    └─ comparison.md           # timing & difficulty comparison
