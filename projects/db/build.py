# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "altair",
# ]
# ///
"""BabsonAI Labs database: builds database.duckdb from the CSV files in data/.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import altair as alt
    import duckdb
    import polars as pl

    return alt, duckdb, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs Database

    This notebook builds `database.duckdb` from the CSV files in `data/`, the way notebook 6 built `ma-towns.duckdb`. It deletes the old file, creates every table with its keys and rules, loads the CSV files, creates one view, and then asks the database a few questions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables

    Five tables, matching `README.md`'s diagram: `people`, `projects`, `assignments` (who works on which project), `tasks` and `expenses`.

    - `person_id`, `project_id`, `task_id` and `expense_id` are surrogate keys: numbers the database assigns, not something the business already had. `work_email` looks like a natural key, but the scenario says it changes when somebody changes title, so it is `UNIQUE` instead of the primary key.
    - `assignments` has no single-column key: one row is one person on one project, so its primary key is the pair `(project_id, person_id)`.
    - `manager_id` in `people` references `people` itself, and is nullable because the two founders report to nobody.
    - `assigned_to` in `tasks` is nullable, because a new task may be unassigned. `completed_date` is nullable until the task is done, and its `CHECK` refuses a completion date before the task's creation date.
    - `category` and `status` columns use `CHECK ... IN (...)` to hold the scenario's fixed lists of values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data

    `make_data.py` writes one CSV file per table into `data/`, with a fixed random seed so it writes the same files every run: about 25 people, 14 projects, 276 tasks and 160 expenses, covering the 12 months up to 2026-11-08.

    **Two rows break a rule on purpose**, for business question 7 ("every task checked against the rule that its assignee works on its project"). No `CHECK` can hold that rule, because it compares `tasks` against `assignments` across tables; question 7 is how the database is checked instead. Running `make_data.py` prints which two:

    - task 151 (project 8) assigned to person 14, who is not on project 8's team
    - task 130 (project 7) assigned to person 6, who is not on project 7's team

    **Three projects get no expenses at all** on purpose, for business question 5.

    **`people.manager_id` references `people` itself**, so each row has to load after its manager, one `INSERT` at a time. `make_data.py` writes the founders first, then the four managers, then everybody else, so inserting the rows in file order always satisfies the foreign key.
    """)
    return


@app.cell
def _(mo, pl):
    _data_dir = mo.notebook_dir() / "data"
    # null_values=[""] turns the blank cells (a founder's manager, an
    # unassigned task, an unfinished task's completed_date) into real NULLs
    # instead of empty text.
    people_rows = pl.read_csv(_data_dir / "people.csv", try_parse_dates=True, null_values=[""])
    projects_rows = pl.read_csv(_data_dir / "projects.csv", try_parse_dates=True, null_values=[""])
    assignments_rows = pl.read_csv(_data_dir / "assignments.csv", try_parse_dates=True, null_values=[""])
    tasks_rows = pl.read_csv(_data_dir / "tasks.csv", try_parse_dates=True, null_values=[""])
    expenses_rows = pl.read_csv(_data_dir / "expenses.csv", try_parse_dates=True, null_values=[""])
    people_rows.shape, projects_rows.shape, assignments_rows.shape, tasks_rows.shape, expenses_rows.shape
    return assignments_rows, expenses_rows, people_rows, projects_rows, tasks_rows


@app.cell
def _(assignments_rows, duckdb, expenses_rows, mo, people_rows, projects_rows, tasks_rows):
    _file = mo.notebook_dir() / "database.duckdb"
    _file.unlink(missing_ok=True)

    with duckdb.connect(_file) as _con:
        _con.execute("""
            CREATE TABLE people (
                person_id  INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name  VARCHAR NOT NULL,
                work_email VARCHAR NOT NULL UNIQUE,
                title      VARCHAR NOT NULL,
                start_date DATE NOT NULL,
                manager_id INTEGER REFERENCES people(person_id)
            )
        """)
        _con.execute("""
            CREATE TABLE projects (
                project_id  INTEGER PRIMARY KEY,
                name        VARCHAR NOT NULL,
                client_name VARCHAR,
                category    VARCHAR NOT NULL CHECK (category IN ('LLM app', 'data pipeline', 'internal tool')),
                budget      DECIMAL(10, 2) NOT NULL CHECK (budget > 0),
                start_date  DATE NOT NULL,
                status      VARCHAR NOT NULL CHECK (status IN ('planned', 'active', 'paused', 'done'))
            )
        """)
        _con.execute("""
            CREATE TABLE assignments (
                project_id     INTEGER NOT NULL REFERENCES projects(project_id),
                person_id      INTEGER NOT NULL REFERENCES people(person_id),
                role           VARCHAR NOT NULL,
                hours_per_week INTEGER NOT NULL CHECK (hours_per_week BETWEEN 1 AND 40),
                joined_date    DATE NOT NULL,
                PRIMARY KEY (project_id, person_id)
            )
        """)
        _con.execute("""
            CREATE TABLE tasks (
                task_id        INTEGER PRIMARY KEY,
                project_id     INTEGER NOT NULL REFERENCES projects(project_id),
                description    VARCHAR NOT NULL,
                created_date   DATE NOT NULL,
                assigned_to    INTEGER REFERENCES people(person_id),
                due_date       DATE NOT NULL,
                completed_date DATE CHECK (completed_date IS NULL OR completed_date >= created_date)
            )
        """)
        _con.execute("""
            CREATE TABLE expenses (
                expense_id   INTEGER PRIMARY KEY,
                project_id   INTEGER NOT NULL REFERENCES projects(project_id),
                expense_date DATE NOT NULL,
                amount       DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
                category     VARCHAR NOT NULL CHECK (category IN ('GPU cloud', 'data labeling', 'software', 'travel')),
                note         VARCHAR
            )
        """)

        _con.execute("INSERT INTO projects SELECT * FROM projects_rows")

        for _row in people_rows.iter_rows():
            _con.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)", list(_row))

        _con.execute("INSERT INTO assignments SELECT * FROM assignments_rows")
        _con.execute("INSERT INTO tasks SELECT * FROM tasks_rows")
        _con.execute("INSERT INTO expenses SELECT * FROM expenses_rows")

        _con.execute("""
            CREATE VIEW project_spend_vs_budget AS
                SELECT
                    p.project_id,
                    p.name,
                    p.status,
                    p.budget,
                    coalesce(sum(e.amount), 0) AS spent,
                    round(coalesce(sum(e.amount), 0) * 100.0 / p.budget, 1) AS spent_percent
                FROM projects p
                LEFT JOIN expenses e ON e.project_id = p.project_id
                GROUP BY p.project_id, p.name, p.status, p.budget
        """)

    database = _file
    database.name
    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Every other cell asks through `ask`.** It opens the file only to read, runs one query, hands back the result as a table, and closes the file again.
    """)
    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data

    The first version of `make_data.py` drew every expense category's amount from the same $80-$55,000 range, which made a business trip look as expensive as a month of GPU training. The chart below is after the fix: each category now has its own range, so GPU cloud and data labeling average far more than software and travel, which is how an AI startup's bills really look.
    """)
    return


@app.cell
def _(expenses_rows, pl):
    expense_amount_by_category = (
        expenses_rows.group_by("category")
        .agg(pl.col("amount").mean().alias("average_amount"))
        .sort("average_amount", descending=True)
    )
    expense_amount_by_category
    return (expense_amount_by_category,)


@app.cell
def _(alt, expense_amount_by_category, mo):
    expense_category_chart = mo.ui.altair_chart(
        expense_amount_by_category.plot.bar(
            y=alt.Y("category", sort="-x", title="Expense category"),
            x=alt.X("average_amount", title="Average expense amount ($)"),
        ).properties(title="Average expense amount by category")
    )
    expense_category_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'people' AS table_name, count(*) AS rows FROM people
        UNION ALL SELECT 'projects', count(*) FROM projects
        UNION ALL SELECT 'assignments', count(*) FROM assignments
        UNION ALL SELECT 'tasks', count(*) FROM tasks
        UNION ALL SELECT 'expenses', count(*) FROM expenses
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses

    An expense of $0 breaks `CHECK (amount > 0)`. `ask()` only reads, so this opens its own short write connection, the way notebook 6's checks do, inside `try`/`except`, so the rest of the notebook still runs.
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("INSERT INTO expenses VALUES (9999, 1, '2026-11-01', 0, 'software', 'should be refused')")
        zero_amount_check = "accepted"
    except duckdb.ConstraintException as _error:
        zero_amount_check = str(_error).splitlines()[0]
    zero_amount_check
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew

    Three queries whose answers I knew before running them, because `make_data.py` was written to produce exactly these numbers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""*Check yourself: 25, one row per person `make_data.py` wrote.*""")
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS people FROM people")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""*Check yourself: 3, the projects `make_data.py` left out of `expenses.csv` on purpose.*""")
    return


@app.cell
def _(ask):
    ask("""
        SELECT count(*) AS projects_with_no_expenses
        FROM projects
        WHERE project_id NOT IN (SELECT project_id FROM expenses)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""*Check yourself: 2, the two tasks `make_data.py` reassigned on purpose to break business question 7's rule.*""")
    return


@app.cell
def _(ask):
    ask("""
        SELECT count(*) AS tasks_assigned_off_project
        FROM tasks t
        LEFT JOIN assignments a
            ON a.project_id = t.project_id AND a.person_id = t.assigned_to
        WHERE t.assigned_to IS NOT NULL AND a.person_id IS NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View

    `project_spend_vs_budget`, created in the cell that builds the database, is the question a project manager would ask every week: how much of each project's budget is already spent. Part B's answer to business question 1 asks for it by name.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM project_spend_vs_budget ORDER BY spent_percent DESC LIMIT 5")
    return


if __name__ == "__main__":
    app.run()
