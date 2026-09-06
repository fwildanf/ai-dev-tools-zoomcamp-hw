# Django Build Backlog

Small, dependency-ordered backlog for the shared household chores MVP.

## Development Setup

- Install dependencies with `uv sync`.
- Run Django commands with `uv run python manage.py <command>`.

## 1. Resolve Persistence and App Configuration

**Status:** Done

- Django's local SQLite database replaces browser local storage for the MVP.
- The `chores` app is registered in `household_chores/settings.py`.
- The chores app is available at `/chores/`.

**Done when:** The chosen persistence approach is documented and the app has a reachable URL.

## 2. Create Household Member Models

**Status:** Done

- Add a `HouseholdMember` model with a name and timestamps.
- Add admin registration.
- Create and run migrations.

**Done when:** Members can be created, renamed, and removed through Django's admin or app UI.

## 3. Create Chore and Schedule Models

**Status:** Done

- Add a `Chore` model with name, assignee, due date, frequency, completion state, and timestamps.
- Support one-time, daily, weekly, and monthly schedules.
- Add validation for required names, valid dates, and one assignee per chore.
- Create and run migrations.

**Done when:** The database can represent every chore type defined in the plan.

## 4. Build Household and Chore Management Views

**Status:** Done

- Add pages and forms to list, create, edit, and delete members.
- Add pages and forms to list, create, edit, and delete chores.
- Include predefined chore choices while allowing custom names.

**Done when:** A household can manage its members and chores without using the Django admin.

## 5. Implement Assignment Rotation

**Status:** Done

- Add a service or model method that selects the next household member for a recurring chore.
- Advance the assignee when a recurring chore is completed and the next occurrence is created.
- Keep exactly one assignee on every chore occurrence.

**Done when:** Repeated completion of a recurring chore distributes assignments across members in order.

## 6. Add Completion, History, and Overdue Behavior

**Status:** Done

- Allow any household member to mark a chore complete.
- Preserve completed occurrences in a recent history view.
- Mark incomplete chores past their due date as overdue.
- Generate the next occurrence for recurring chores.

**Done when:** Completion updates status, history remains visible, overdue chores are labeled, and recurring work continues.

## 7. Build Workload Dashboard and Filtering

**Status:** Done

- Create a mobile-friendly dashboard grouped by household member.
- Show open, completed, and overdue chores.
- Add filtering by assignee.

**Done when:** The main screen makes each person's current workload easy to compare.

## 8. Add Automated Tests and MVP Verification

**Status:** Done

- Test member and chore validation.
- Test CRUD views and permissions implied by shared access.
- Test rotation, completion, history, overdue labels, and recurring occurrences.
- Verify the success criteria in `plan.md` manually.

**Done when:** The test suite passes and each MVP success criterion has a corresponding test or verification note.

## Not Planned for MVP

- Accounts or authentication
- Email or push notifications
- Points, streaks, leaderboards, or rewards
- Skipping, deferring, or swapping chores
- Multi-household support
