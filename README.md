# AI Dev Tools Zoomcamp Homework

## Projects

### `01-ai-native-workflow` - Shared Household Chores

The `01-ai-native-workflow` project is a local Django web app for managing shared household chores. It supports up to five household members, recurring chores, automatic assignment rotation, completion history, overdue labels, and workload filtering.

#### Features

- Add, rename, and remove household members
- Create predefined or custom chores
- Assign one member to each chore
- Schedule one-time, daily, weekly, or monthly chores
- Rotate recurring assignments automatically
- Mark chores complete and preserve completion history
- Identify overdue chores
- View workload by member and filter the chore list

#### Technology

- Python 3.14+
- Django 5.2
- SQLite for local persistence
- `uv` for dependency management

#### Setup

From the project directory:

```bash
cd 01-ai-native-workflow
uv sync
uv run python manage.py migrate
```

#### Run the Development Server

```bash
uv run python manage.py runserver
```

Open the chores app at <http://127.0.0.1:8000/chores/>.

#### Run Tests

Run all Django tests:

```bash
uv run python manage.py test
```

Run only the chores app tests:

```bash
uv run python manage.py test chores
```

#### Project Documentation

- [Product plan](01-ai-native-workflow/_docs/plan.md)
- [Django backlog](01-ai-native-workflow/_docs/backlog.md)

#### MVP Boundaries

The current version has no user accounts, notifications, rewards, chore swapping, or external production database. It is intended for local household use with shared access and a local SQLite database.