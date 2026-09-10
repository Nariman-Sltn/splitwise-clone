# 💰 Splitwise Clone

A web application for splitting expenses among groups of people, inspired by Splitwise.

🔗 **Live Demo:** [splitwise-clone-sepia.vercel.app](https://splitwise-clone-sepia.vercel.app)
📁 **GitHub:** [github.com/Nariman-Sltn/splitwise-clone](https://github.com/Nariman-Sltn/splitwise-clone)

---

## ✨ Features

- **User Authentication** — Sign up, log in, log out, and delete account
- **Group Management** — Create groups with passwords, join existing groups, leave or delete groups
- **Expense Tracking** — Add, edit, and delete expenses with equal splitting among participants
- **Debt Simplification** — Greedy algorithm to minimize the number of transactions needed to settle debts
- **Settlement System** — Record payments between members and update balances in real time
- **Activity Log** — Track all group activity with a filterable history
- **Ownership Transfer** — When a group owner leaves, ownership transfers to the next member automatically
- **RTL Support** — Full Persian (Farsi) UI support with Bootstrap RTL

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13 + Django 5.x |
| Database | PostgreSQL (Supabase) |
| Frontend | Bootstrap 5 RTL |
| Deployment | Vercel |
| Version Control | Git + GitHub |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Nariman-Sltn/splitwise-clone.git
cd splitwise-clone

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

Tests cover:
- Balance calculation with multiple expenses
- Settlement reducing and clearing debt
- Debt simplification algorithm

---

## 📁 Project Structure

```
splitwise-clone/
├── config/          # Django settings, URLs, WSGI
├── expenses/        # Main app
│   ├── models.py    # Group, Expense, Settlement, ActivityLog
│   ├── views.py     # All views
│   ├── services.py  # Business logic (balance calculation, debt simplification)
│   ├── forms.py     # Django forms
│   ├── utils.py     # Helper functions (log_activity)
│   └── tests.py     # Unit tests
└── templates/       # HTML templates
```

---

## 💡 Key Design Decisions

- **Business logic in `services.py`** — Separated from views for cleaner architecture
- **Greedy debt simplification** — Minimizes transactions needed to settle all debts
- **`GroupMembership` as a through-model** — Allows storing extra data like `joined_at`
- **Hashed group passwords** — Using Django's `make_password`/`check_password`