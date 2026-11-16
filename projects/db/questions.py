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

    *(Answers below, worked through after the prediction in section 3.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    *(To do, after the answers above.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    *(To do, after the answers above.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    **The question I picked, before answering anything above:** business question 6, *"One row per project with its number of tasks and its total expenses, each checked against counting it on its own."* It is tagged *(three tables or more)* on the list, and it joins `projects`, `tasks` and `expenses`.

    **My prediction.** Part A's Row Counts section says there are 263 rows in `tasks` and 160 in `expenses`, and business question 5 says 3 of the 14 projects have no expenses at all, so only 11 projects have both. If I chain `projects JOIN tasks ... JOIN expenses ...` on `project_id` in one query, `project_id` is not unique in either `tasks` or `expenses`, so the join matches every task row of a project against every expense row of that same project, the same fan-out the notebook showed for `orders` and `order_details`. Spread evenly, that is about 263 ÷ 14 ≈ 19 tasks and 160 ÷ 11 ≈ 14.5 expenses for each of the 11 projects with both, so I expect roughly 19 × 14.5 × 11 ≈ 3,030 rows before any `GROUP BY` — far more than 263 or 160 alone, because the 3-table join counts every pairing, not every task or every expense.

    *(Committed as `db: prediction`, before running the query below.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further

    *(To do, after the answers above.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent

    *(To do.)*
    """)
    return


if __name__ == "__main__":
    app.run()
