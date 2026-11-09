"""Writes one CSV file per table for the BabsonAI Labs database into projects/db/data/.

Run it with: uv run python projects/db/make_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

# A fixed seed means this script writes the same files every time it runs.
random.seed(42)
Faker.seed(42)
fake = Faker()

AS_OF = date(2026, 11, 8)
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------- people ---
# Two founders report to nobody. Four managers report to a founder.
# Everybody else reports to a manager. Writing the rows in this order means
# every manager already exists in the file before the people who report to them.

FOUNDER_TITLES = ["CEO", "CTO"]
MANAGER_TITLES = ["VP of Engineering", "VP of Product", "Engineering Manager", "Project Manager"]
IC_TITLES = [
    "ML Engineer",
    "Data Engineer",
    "Data Scientist",
    "Software Engineer",
    "Business Analyst",
    "Designer",
    "QA Engineer",
]

used_emails = set()


def make_email(first_name, last_name):
    base = (first_name + "." + last_name).lower().replace(" ", "")
    email = base + "@babsonailabs.com"
    counter = 2
    while email in used_emails:
        email = base + str(counter) + "@babsonailabs.com"
        counter += 1
    used_emails.add(email)
    return email


people_rows = []
all_person_ids = []
manager_ids = []
people_start = {}

for i in range(2):
    person_id = i + 1
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = make_email(first_name, last_name)
    start_date = AS_OF - timedelta(days=random.randint(365 * 4, 365 * 6))
    people_rows.append([person_id, first_name, last_name, email, FOUNDER_TITLES[i], start_date.isoformat(), ""])
    all_person_ids.append(person_id)
    people_start[person_id] = start_date

for i in range(4):
    person_id = i + 3
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = make_email(first_name, last_name)
    start_date = AS_OF - timedelta(days=random.randint(365 * 2, 365 * 4))
    manager_id = random.choice([1, 2])
    people_rows.append([person_id, first_name, last_name, email, MANAGER_TITLES[i], start_date.isoformat(), manager_id])
    all_person_ids.append(person_id)
    manager_ids.append(person_id)
    people_start[person_id] = start_date

for i in range(19):
    person_id = i + 7
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = make_email(first_name, last_name)
    title = random.choice(IC_TITLES)
    start_date = AS_OF - timedelta(days=random.randint(90, 365 * 2))
    manager_id = random.choice(manager_ids)
    people_rows.append([person_id, first_name, last_name, email, title, start_date.isoformat(), manager_id])
    all_person_ids.append(person_id)
    people_start[person_id] = start_date

with open(DATA_DIR / "people.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["person_id", "first_name", "last_name", "work_email", "title", "start_date", "manager_id"])
    for row in people_rows:
        writer.writerow(row)


# -------------------------------------------------------------- projects ---

CATEGORIES = ["LLM app", "data pipeline", "internal tool"]
STATUSES = ["planned", "active", "paused", "done"]
STATUS_WEIGHTS = [0.2, 0.4, 0.15, 0.25]
PROJECT_COUNT = 14

projects_rows = []
project_ids = []
project_start_by_id = {}

for i in range(PROJECT_COUNT):
    project_id = i + 1
    category = random.choice(CATEGORIES)
    name = fake.catch_phrase()
    if category == "internal tool":
        client_name = ""
    else:
        client_name = fake.company()
    budget = round(random.uniform(20000, 500000), 2)
    start_date = AS_OF - timedelta(days=random.randint(60, 365 * 2))
    status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
    projects_rows.append([project_id, name, client_name, category, budget, start_date.isoformat(), status])
    project_ids.append(project_id)
    project_start_by_id[project_id] = start_date

with open(DATA_DIR / "projects.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["project_id", "name", "client_name", "category", "budget", "start_date", "status"])
    for row in projects_rows:
        writer.writerow(row)


# ----------------------------------------------------------- assignments ---

ROLES = ["Project Lead", "ML Engineer", "Data Engineer", "Business Analyst", "Designer", "QA Engineer"]

assignments_rows = []
project_team = {}

for project_id in project_ids:
    project_start = project_start_by_id[project_id]
    team_size = random.randint(2, 6)
    team = random.sample(all_person_ids, team_size)
    project_team[project_id] = team
    for person_id in team:
        role = random.choice(ROLES)
        hours_per_week = random.randint(2, 38)
        earliest = max(project_start, people_start[person_id])
        joined_date = earliest + timedelta(days=random.randint(0, 45))
        if joined_date > AS_OF:
            joined_date = AS_OF
        assignments_rows.append([project_id, person_id, role, hours_per_week, joined_date.isoformat()])

with open(DATA_DIR / "assignments.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["project_id", "person_id", "role", "hours_per_week", "joined_date"])
    for row in assignments_rows:
        writer.writerow(row)


# ----------------------------------------------------------------- tasks ---

TASK_VERBS = ["Build", "Design", "Review", "Test", "Document", "Fix", "Deploy", "Research", "Refactor", "Optimize"]
TASK_NOUNS = [
    "the data pipeline",
    "the chatbot prompts",
    "the client dashboard",
    "the labeling workflow",
    "the model evaluation",
    "the onboarding flow",
    "the API integration",
    "the billing report",
    "the training data",
    "the deployment script",
]

tasks_rows = []
next_task_id = 1

for project_id in project_ids:
    project_start = project_start_by_id[project_id]
    team = project_team[project_id]
    task_count = random.randint(16, 22)
    for _ in range(task_count):
        description = random.choice(TASK_VERBS) + " " + random.choice(TASK_NOUNS)

        # Pick who the task goes to before picking its created_date, so a
        # task is never created before that person's start_date.
        if random.random() < 0.8:
            assigned_to = random.choice(team)
            earliest_create = max(project_start, people_start[assigned_to])
        else:
            assigned_to = ""
            earliest_create = project_start

        days_since_earliest = (AS_OF - earliest_create).days
        if days_since_earliest < 1:
            days_since_earliest = 1
        created_date = earliest_create + timedelta(days=random.randint(0, days_since_earliest))
        due_date = created_date + timedelta(days=random.randint(3, 45))

        completed_date = ""
        if due_date <= AS_OF:
            if random.random() < 0.7:
                latest_complete = due_date + timedelta(days=10)
                if latest_complete > AS_OF:
                    latest_complete = AS_OF
                span = (latest_complete - created_date).days
                if span < 0:
                    span = 0
                completed_date = (created_date + timedelta(days=random.randint(0, span))).isoformat()
        else:
            if random.random() < 0.3:
                span = (AS_OF - created_date).days
                if span < 0:
                    span = 0
                completed_date = (created_date + timedelta(days=random.randint(0, span))).isoformat()

        tasks_rows.append(
            [next_task_id, project_id, description, created_date.isoformat(), assigned_to, due_date.isoformat(), completed_date]
        )
        next_task_id += 1

# Break the rule checked by business question 7 ("a task is assigned only to
# somebody who works on its project") on purpose, in exactly two rows.
assigned_rows = []
for row in tasks_rows:
    if row[4] != "":
        assigned_rows.append(row)

broken_rows = random.sample(assigned_rows, 2)
broken_notes = []
for row in broken_rows:
    project_id = row[1]
    team = project_team[project_id]
    outsiders = []
    for person_id in all_person_ids:
        if person_id not in team:
            outsiders.append(person_id)
    outsider = random.choice(outsiders)
    row[4] = outsider
    broken_notes.append(f"task_id {row[0]} (project_id {project_id}) is now assigned to person_id {outsider}, who is not on that project's team")

with open(DATA_DIR / "tasks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["task_id", "project_id", "description", "created_date", "assigned_to", "due_date", "completed_date"])
    for row in tasks_rows:
        writer.writerow(row)


# -------------------------------------------------------------- expenses ---

EXPENSE_CATEGORIES = ["GPU cloud", "data labeling", "software", "travel"]
EXPENSE_NOTES = {
    "GPU cloud": ["Model training run", "Inference hosting", "Extra GPU hours"],
    "data labeling": ["Vendor labeling batch", "Quality review pass", "Annotation guideline update"],
    "software": ["SaaS subscription", "Dev tool license", "Monitoring service"],
    "travel": ["Client site visit", "Conference trip", "Team offsite"],
}
# Each category has its own price range. A first version drew every
# category's amount from the same 80-55000 range, which made a business
# trip look as expensive as a month of GPU training; this range instead
# matches what each category plausibly costs.
EXPENSE_AMOUNT_RANGES = {
    "GPU cloud": (2000, 55000),
    "data labeling": (500, 20000),
    "software": (80, 5000),
    "travel": (200, 6000),
}

# Leave three projects out entirely, so business question 5 has an answer.
no_expense_project_ids = random.sample(project_ids, 3)

expenses_rows = []
next_expense_id = 1
window_start = AS_OF - timedelta(days=365)

while len(expenses_rows) < 160:
    project_id = random.choice(project_ids)
    if project_id in no_expense_project_ids:
        continue
    category = random.choice(EXPENSE_CATEGORIES)
    note = random.choice(EXPENSE_NOTES[category])
    low, high = EXPENSE_AMOUNT_RANGES[category]
    amount = round(random.uniform(low, high), 2)
    expense_date = window_start + timedelta(days=random.randint(0, 365))
    if expense_date > AS_OF:
        expense_date = AS_OF
    expenses_rows.append([next_expense_id, project_id, expense_date.isoformat(), amount, category, note])
    next_expense_id += 1

with open(DATA_DIR / "expenses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["expense_id", "project_id", "expense_date", "amount", "category", "note"])
    for row in expenses_rows:
        writer.writerow(row)


# ---------------------------------------------------------------- report ---

print(f"people: {len(people_rows)}")
print(f"projects: {len(projects_rows)}")
print(f"assignments: {len(assignments_rows)}")
print(f"tasks: {len(tasks_rows)}")
print(f"expenses: {len(expenses_rows)}")
print(f"projects with no expenses: {no_expense_project_ids}")
print("Rows that break the 'assignee works on the project' rule on purpose:")
for note in broken_notes:
    print(" - " + note)
