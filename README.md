# 💰 Splitwise Clone

A full-featured expense splitting web application built with Django — inspired by Splitwise.

🔗 **Live Demo:** [narimansltn.pythonanywhere.com](https://narimansltn.pythonanywhere.com)

---

## ✨ Features

- **User Authentication** — Signup, login, logout, and account deletion
- **Group Management** — Create groups with passwords, join existing groups, leave or delete groups
- **Expense Tracking** — Add, edit, and delete expenses with equal splitting among participants
- **Debt Simplification** — Greedy algorithm to minimize the number of transactions needed to settle all debts
- **Settlement System** — Record payments between members and automatically update balances
- **Activity Log** — Full history of group activity, with admin delete control
- **Responsive UI** — Clean Bootstrap RTL interface

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.1 |
| Database | SQLite |
| Frontend | Bootstrap 5 (RTL) |
| Auth | Django built-in authentication |
| Deployment | PythonAnywhere |

---

## ⚙️ Local Setup

```bash
# Clone the repository
git clone https://github.com/Nariman-Sltn/splitwise-clone.git
cd splitwise-clone

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Then open [http://localhost:8000](http://localhost:8000)

---

## 🧪 Running Tests

```bash
python manage.py test
```

5 unit tests covering:
- Basic balance calculation
- Multi-expense balance aggregation
- Settlement impact on balances
- Full debt clearance via settlement
- Debt simplification algorithm

---

## 📁 Project Structure

```
splitwise-clone/
├── config/              # Django project settings
├── expenses/            # Main app
│   ├── models.py        # Group, Expense, Settlement, ActivityLog
│   ├── views.py         # All views
│   ├── services.py      # Business logic (balance calculation, debt simplification)
│   ├── forms.py         # Django forms
│   ├── utils.py         # Helper functions (log_activity)
│   └── templates/       # HTML templates
├── manage.py
└── requirements.txt
```

---

## 🧠 Key Design Decisions

- **Business logic in `services.py`** — kept separate from views for maintainability
- **`GroupMembership` as a through model** — allows storing join date and future extensibility
- **Greedy debt simplification** — minimizes number of transactions needed to settle all balances
- **Hashed group passwords** — using Django's `make_password` / `check_password`

---

## 👨‍💻 Author

**Nariman Soltani**
[GitHub](https://github.com/Nariman-Sltn)
