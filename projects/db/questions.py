# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "altair",
# ]
# ///
"""BabsonAI Labs database: Part B, the business questions.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from datetime import date

    import altair as alt
    import duckdb
    import polars as pl

    return alt, date, duckdb, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs: The Business Questions

    This notebook asks `database.duckdb`, the database `build.py` built, the questions a founder of BabsonAI Labs would actually ask: where the budget is going, who is overloaded, which tasks are late, and which rows break a rule no `CHECK` can hold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One Date for Every Question

    `make_data.py` covers the 12 months up to one date, `as_of`. Every "last 90 days" or "last month" below counts back from it, so the questions all agree on what "now" means.
    """)
    return


@app.cell
def _(date):
    as_of = date(2026, 11, 8)
    as_of
    return (as_of,)


@app.cell
def _(mo, duckdb):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *The eight questions on the BabsonAI Labs list, and two of my own, are below. Each one has the question in plain words, the query, the result, and a sentence that answers it with the numbers in it.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1 · How much of each project's budget is already spent?

    This is the view `build.py` created, `project_spend_vs_budget`: for every project, what it has spent so far against its budget, largest share first.
    """)
    return


@app.cell
def _(ask):
    q1_result = ask("""
        SELECT * FROM project_spend_vs_budget ORDER BY spent_percent DESC
    """)
    q1_result
    return (q1_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Persistent multi-tasking extranet` has spent the largest share of its budget, 147.9%, meaning it has already gone 47.9% over budget even though its status is `done`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2 · Which tasks are late and still not done?

    Tasks whose due date has already passed, as of `as_of`, and that have no completed date yet, with the project and the person assigned.
    """)
    return


@app.cell
def _(ask, as_of):
    q2_result = ask(f"""
        SELECT
            t.task_id,
            p.name AS project_name,
            t.due_date,
            pe.first_name || ' ' || pe.last_name AS assigned_to
        FROM tasks t
        JOIN projects p ON p.project_id = t.project_id
        LEFT JOIN people pe ON pe.person_id = t.assigned_to
        WHERE t.completed_date IS NULL AND t.due_date < DATE '{as_of}'
        ORDER BY t.due_date
    """)
    q2_result
    return (q2_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    88 tasks are past their due date and still not marked complete, as of 2026-11-08; a few, such as task 204, have no assignee at all, so nobody currently owns finishing them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3 · Who is over-committed on active projects?

    Each person's hours a week added up across their currently **active** projects, keeping the people above 40. I read "active projects" as the project's `status`, not every project a person has ever joined, since a paused or finished project no longer takes a weekly commitment.
    """)
    return


@app.cell
def _(ask):
    q3_result = ask("""
        SELECT
            a.person_id,
            pe.first_name || ' ' || pe.last_name AS person,
            sum(a.hours_per_week) AS hours_per_week
        FROM assignments a
        JOIN projects p ON p.project_id = a.project_id
        JOIN people pe ON pe.person_id = a.person_id
        WHERE p.status = 'active'
        GROUP BY a.person_id, pe.first_name, pe.last_name
        ORDER BY hours_per_week DESC
    """)
    q3_result
    return (q3_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reading "active" as the project's `status = 'active'`, 4 people are committed above 40 hours a week across their active projects: Jeremy Roberts leads at 105, well above a single full-time week, followed by Jeffrey Lawrence at 69, Susan Rogers at 55 and Danielle Johnson at 49.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4 · Which expense categories are above average, in the last 90 days?

    Total spend by category in the 90 days before `as_of`, keeping only the categories whose own total is above the average of those (last-90-day) category totals — not an all-time average, since the question is scoped to the last 90 days throughout.
    """)
    return


@app.cell
def _(ask, as_of):
    q4_result = ask(f"""
        WITH by_category AS (
            SELECT category, sum(amount) AS total
            FROM expenses
            WHERE expense_date >= DATE '{as_of}' - INTERVAL 90 DAY
            GROUP BY category
        )
        SELECT category, total
        FROM by_category
        WHERE total > (SELECT avg(total) FROM by_category)
        ORDER BY total DESC
    """)
    q4_result
    return (q4_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only `GPU cloud` is above average in the last 90 days, at $301,088.57, well above the four categories' average of about $116,757 — the other three (data labeling, travel, software) all fall below it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5 · Which projects have no expenses charged to them at all?
    """)
    return


@app.cell
def _(ask):
    q5_result = ask("""
        SELECT project_id, name
        FROM projects
        WHERE project_id NOT IN (SELECT project_id FROM expenses)
    """)
    q5_result
    return (q5_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3 projects have never had an expense charged to them: `Visionary zero-defect approach`, `Open-architected encompassing architecture` and `Distributed responsive complexity`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6 · For each project, how many tasks and how much has it spent?

    One row per project with its task count and its total expenses, each counted on its own rather than through a single three-table join, which would multiply tasks by expenses for the same project. Section 3 below walks through exactly that fan-out.
    """)
    return


@app.cell
def _(ask):
    q6_result = ask("""
        WITH task_counts AS (
            SELECT project_id, count(*) AS task_count FROM tasks GROUP BY project_id
        ), expense_totals AS (
            SELECT project_id, sum(amount) AS total_expenses FROM expenses GROUP BY project_id
        )
        SELECT
            p.project_id,
            p.name,
            coalesce(tc.task_count, 0) AS task_count,
            coalesce(et.total_expenses, 0) AS total_expenses
        FROM projects p
        LEFT JOIN task_counts tc ON tc.project_id = p.project_id
        LEFT JOIN expense_totals et ON et.project_id = p.project_id
        ORDER BY p.project_id
    """)
    q6_result
    return (q6_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Universal foreground data-warehouse` (project 7) has the most tasks, 22, and the highest total expenses, $183,129.58; the 3 projects from question 5 show up here too, with a task count but $0 in expenses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7 · Which tasks are assigned to somebody not on that project's team?

    This checks the rule no `CHECK` can hold: a task's assignee has to be on the `assignments` team for that same project. `make_data.py` breaks this rule on purpose in exactly two rows.
    """)
    return


@app.cell
def _(ask):
    q7_result = ask("""
        SELECT
            t.task_id,
            p.name AS project_name,
            pe.first_name || ' ' || pe.last_name AS assigned_to
        FROM tasks t
        JOIN people pe ON pe.person_id = t.assigned_to
        JOIN projects p ON p.project_id = t.project_id
        LEFT JOIN assignments a ON a.project_id = t.project_id AND a.person_id = t.assigned_to
        WHERE t.assigned_to IS NOT NULL AND a.person_id IS NULL
    """)
    q7_result
    return (q7_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Exactly 2 tasks break the rule, the same 2 `make_data.py` names under Part A's section 2: task 78 on `Persistent homogeneous flexibility`, assigned to Danielle Johnson, and task 203 on `Multi-lateral directional challenge`, assigned to Anthony Gonzalez — neither is on that project's team.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 8 · For each manager, how many people report to them and how many hours have those people committed?
    """)
    return


@app.cell
def _(ask):
    q8_result = ask("""
        SELECT
            m.person_id AS manager_id,
            m.first_name || ' ' || m.last_name AS manager,
            count(DISTINCT pe.person_id) AS direct_reports,
            coalesce(sum(a.hours_per_week), 0) AS total_hours_per_week
        FROM people m
        JOIN people pe ON pe.manager_id = m.person_id
        LEFT JOIN assignments a ON a.person_id = pe.person_id
        GROUP BY m.person_id, m.first_name, m.last_name
        ORDER BY direct_reports DESC
    """)
    q8_result
    return (q8_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Jill Rhodes and Robert Johnson are tied for the most direct reports, 6 each; reading "overloaded" by hours rather than headcount instead, Jill Rhodes's reports have committed more total hours a week, 312 against Robert Johnson's 228.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 9 · How long does a task typically take to finish, by project category? *(my own question)*

    For completed tasks only, the average number of days from `created_date` to `completed_date`, by project category. A manager choosing which kind of work to take on next would want to know this before quoting a client a timeline. I read "typically take to finish" as counting only tasks that have actually finished; a still-open task has no completion date, so it has no finish time to average in yet.
    """)
    return


@app.cell
def _(ask):
    q9_result = ask("""
        SELECT
            p.category,
            round(avg(date_diff('day', t.created_date, t.completed_date)), 1) AS avg_days_to_complete,
            count(*) AS completed_tasks
        FROM tasks t
        JOIN projects p ON p.project_id = t.project_id
        WHERE t.completed_date IS NOT NULL
        GROUP BY p.category
        ORDER BY avg_days_to_complete DESC
    """)
    q9_result
    return (q9_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting only tasks that have actually finished, LLM app tasks take the longest on average, 17.9 days over 58 completed tasks, against 17.3 days for data pipeline tasks and 13.3 days for internal tools, which finish noticeably faster.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 10 · Which clients are we spending the most on, in GPU cloud costs? *(my own question)*

    Total `GPU cloud` expenses charged to each paying client's projects, largest first. I read "clients" as `client_name`, so internal projects (which have none) are left out of this ranking rather than grouped in as a client of their own; a manager asking this wants to know which external client relationship is the most compute-hungry.
    """)
    return


@app.cell
def _(ask):
    q10_result = ask("""
        SELECT
            p.client_name,
            round(sum(e.amount), 2) AS gpu_cloud_spend
        FROM expenses e
        JOIN projects p ON p.project_id = e.project_id
        WHERE e.category = 'GPU cloud' AND p.client_name IS NOT NULL
        GROUP BY p.client_name
        ORDER BY gpu_cloud_spend DESC
    """)
    q10_result
    return (q10_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reading "clients" as paying clients only, leaving out internal projects, `Mack-Peterson` is by far our most GPU-cloud-intensive client, at $171,992.40, well ahead of the next closest, `Wong, Lynch and Jackson` at $118,881.22.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    Two checks, each reaching an answer above a second way and showing the two agree.

    **Check A, as code.** Question 6's `task_count` column, summed across all 14 projects, has to equal the plain `count(*)` of `tasks` on its own — every task belongs to exactly one project, so the two totals must match. The cell below asserts it, and fails if they do not: change question 6's query to, say, only count tasks with an `assigned_to`, and this check breaks.
    """)
    return


@app.cell
def _(ask, q6_result):
    check_a_from_question_6 = int(q6_result["task_count"].sum())
    check_a_from_tasks_alone = int(ask("SELECT count(*) AS n FROM tasks")["n"][0])
    assert check_a_from_question_6 == check_a_from_tasks_alone, (
        f"{check_a_from_question_6} (summed in question 6) != {check_a_from_tasks_alone} (counted directly)"
    )
    check_a_from_question_6, check_a_from_tasks_alone
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Check B, as code.** Question 5 found 3 projects with no expenses at all. Question 1's view, `project_spend_vs_budget`, computes `spent` independently, with a `LEFT JOIN` and `coalesce(sum(...), 0)`. If the two questions are both right, the projects with `spent = 0` in the view have to be exactly the same 3 projects question 5 found.
    """)
    return


@app.cell
def _(ask, q5_result):
    check_b_from_question_1 = sorted(ask("SELECT project_id FROM project_spend_vs_budget WHERE spent = 0")["project_id"].to_list())
    check_b_from_question_5 = sorted(q5_result["project_id"].to_list())
    assert check_b_from_question_1 == check_b_from_question_5, (
        f"{check_b_from_question_1} (spent = 0 in the view) != {check_b_from_question_5} (question 5's answer)"
    )
    check_b_from_question_1, check_b_from_question_5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    My first draft of question 10 was not "which clients cost the most in GPU cloud spend" — it was "which people are on a project's team but have never been given a single task on any project." My agent wrote the anti-join for it (`assignments` LEFT JOIN `tasks` on `person_id`, keeping the unmatched rows), and I ran it expecting a short list of idle teammates. It came back empty: 0 rows. I did not accept that as the answer, because an empty result for a "which people" question is a sign the question was the wrong one to ask of this data, not that nobody is ever idle — with 263 tasks spread over only 24 people, everybody has been assigned something, somewhere, at some point, so the question as worded could never find anybody. I replaced it with the GPU-cloud-spend-by-client question instead, which does return a real, varied answer (7 clients, from \$171,992 down to \$32,334). The replacement is the `q10_result` cell in this notebook, committed in `0e258cf`, "db: answer the 10 business questions and add the How I Know, Working With the Agent, Reading It Back follow-up, Going Further and Time Spent sections."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    *(To do, by hand: pick a question from the list above tagged "three tables or more," name it here, and write your prediction — how many rows you expect its joins to produce before any `GROUP BY`, and why — before you run the joins below. Commit this paragraph alone with the message `db: prediction`, before running the query below.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Running the joins alone**, with no `GROUP BY`, to count the fan-out directly. *(This query joins `projects`, `tasks` and `expenses`, for question 6 — swap the tables below if you pick a different question.)*
    """)
    return


@app.cell
def _(ask):
    reading_it_back_joined_rows = ask("""
        SELECT count(*) AS joined_rows
        FROM projects p
        JOIN tasks t ON t.project_id = p.project_id
        JOIN expenses e ON e.project_id = p.project_id
    """)
    reading_it_back_joined_rows
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *(To do, by hand: did your prediction match the number above? Why, or why not? Then write, in your own words, what one row of the final, grouped result means.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further

    Two things past the 10 questions:

    1. **A chart.** Question 10's answer (GPU cloud spend by client) as a bar chart, below, so a founder can see the gap between clients at a glance instead of reading a table.
    2. **A control.** A dropdown of every project, below the chart, that re-runs question 1's query filtered to just that project, so anybody could check one project's budget status without touching any SQL.
    """)
    return


@app.cell
def _(alt, mo, q10_result):
    going_further_chart = mo.ui.altair_chart(
        q10_result.plot.bar(
            y=alt.Y("client_name", sort="-x", title="Client"),
            x=alt.X("gpu_cloud_spend", title="GPU cloud spend ($)"),
        ).properties(title="GPU cloud spend by client")
    )
    going_further_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Mack-Peterson` stands out as almost 1.5 times the next client, `Wong, Lynch and Jackson` — a founder deciding where to negotiate a better GPU rate would start there.
    """)
    return


@app.cell
def _(ask, mo):
    project_picker = mo.ui.dropdown(
        options=ask("SELECT project_id || ': ' || name AS label FROM projects ORDER BY project_id")["label"].to_list(),
        value="1: Multi-layered heuristic database",
        label="Pick a project",
    )
    project_picker
    return (project_picker,)


@app.cell
def _(ask, project_picker):
    going_further_picked_id = int(project_picker.value.split(":")[0])
    going_further_picked_result = ask(f"""
        SELECT * FROM project_spend_vs_budget WHERE project_id = {going_further_picked_id}
    """)
    going_further_picked_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent

    *(To do: about how many hours the whole project took you outside class, as one number. Not graded.)*
    """)
    return


if __name__ == "__main__":
    app.run()
