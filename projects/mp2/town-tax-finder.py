# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 2.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo
    import requests

    return mo, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 2

    Save it in your course repository as `projects/mp2/<your-tool>.py`, named for what it does, such as `town-tax-finder.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A couple searching for a place to live wants to know which communities in Middlesex County have both affordable housing and low property taxes. This tool will tell them which towns have an average cost per single family home of $700,000 or less and the average tax bill is under $8,000 per year and display them from least to most expensive.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, open the API's address in your browser and read what comes back. Then write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these:*

    - *Which functions will your tool need? For each, what goes in and what comes out?*
    - *Which addresses will they request?*
    - *How will you know you have every record?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit with the message `mp2: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I would first open the town's address in my browser and look at the result a list of all towns with their code, name, some numbers, and quantity of towns. After that, I would look at the documentation to see what each column stands for.
    My approach would be to pull all the towns in Middlesex County (making sure to get all results and not only the first 50). For each town, I would look at its history and find the row with the year 2026. After that, I would eliminate all the options except the ones with a home value of $700,000 or less and a bill is under $8,000. Finally, I would sort the remaining options by the cheapest bill and output the table.

    1) Functions that need to be created: One function for getting all the towns in a county (input: county name, output: list of towns), and one for getting one town's numbers for one year (input: town code and year, output: value, rate, bill).

    2) Addresses used: the towns list address, and the history address for each town.

    3) How can you tell when you have every town? Compare the number you got to the total that the API says is there.

    4) Check section 6's math: value rate / 1000 should be close to the bill.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every input in one cell.
    """)
    return


@app.cell
def _(mo):
    base_url = "https://oim.zhili.dev/ma"
    county = mo.ui.text(value="Middlesex", label="County")
    budget_dollars = mo.ui.number(value=700000, label="Budget ($)")
    tax_limit_dollars = mo.ui.number(value=8000, label="Max tax bill ($/year)")
    fiscal_year = mo.ui.number(value=2026, label="Fiscal year")

    mo.vstack([county, budget_dollars, tax_limit_dollars, fiscal_year])
    return base_url, budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell
def _(base_url, requests):
    def get_towns(county_name):
        """Given a county name, return a list of every town record in it."""
        towns = []
        page = 1
        while True:
            response = requests.get(
                f"{base_url}/towns",
                params={"county": county_name, "page": page, "per_page": 100},
            )
            data = response.json()
            towns = towns + data["items"]
            if not data["pagination"]["has_next"]:
                break
            page = page + 1
        return towns, data["pagination"]["total"]


    def get_year_record(dor_code, year):
        """Given a town code and a fiscal year, return that year's record (value, rate, bill), or None if missing."""
        response = requests.get(f"{base_url}/towns/{dor_code}/history")
        data = response.json()
        for year_record in data["years"]:
            if year_record["fiscal_year"] == year:
                return year_record
        return None

    return get_towns, get_year_record


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Your functions, and the code that uses them.
    """)
    return


@app.cell
def _(
    budget_dollars,
    county,
    fiscal_year,
    get_towns,
    get_year_record,
    tax_limit_dollars,
):
    def get_bill(town_record):
        """Return just the bill field of a town record, used for sorting."""
        return town_record["bill"]


    all_towns, total_towns = get_towns(county.value)

    all_town_records = []
    passing_towns = []
    for _town in all_towns:
        _record = get_year_record(_town["dor_code"], fiscal_year.value)
        if _record is None:
            continue
        _town_record = {
            "name": _town["name"],
            "dor_code": _town["dor_code"],
            "value": _record["average_single_family_value_dollars"],
            "rate": _record["residential_rate_per_thousand"],
            "bill": _record["average_single_family_bill_dollars"],
        }
        all_town_records.append(_town_record)
        if _record["average_single_family_value_dollars"] <= budget_dollars.value and _record["average_single_family_bill_dollars"] < tax_limit_dollars.value:
            passing_towns.append(_town_record)

    passing_towns_sorted = sorted(passing_towns, key=get_bill)

    len(all_towns), total_towns, len(passing_towns_sorted)
    return all_town_records, passing_towns_sorted


@app.cell
def _(all_town_records, county, fiscal_year):
    import json
    import os

    os.makedirs("projects/mp2/data", exist_ok=True)
    _save_path = f"projects/mp2/data/{county.value.lower()}_{fiscal_year.value}_towns.json"
    with open(_save_path, "w") as _file:
        json.dump(all_town_records, _file, indent=2)

    print(f"Saved {len(all_town_records)} town records to {_save_path}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Your result table, printed with `print` and f-strings with the columns lined up, and one sentence that answers the question in section 1 with the numbers in it. Print the sentence from code with an f-string, so that it changes when the data does.
    """)
    return


@app.cell
def _(budget_dollars, county, passing_towns_sorted, tax_limit_dollars):
    print(f"{'Town':<20}{'Value ($)':>12}{'Rate':>8}{'Bill ($)':>10}")
    for _passing_town in passing_towns_sorted:
        print(f"{_passing_town['name']:<20}{_passing_town['value']:>12,}{_passing_town['rate']:>8.2f}{_passing_town['bill']:>10,}")

    print()
    print(f"In {county.value} County, {len(passing_towns_sorted)} towns have an average home at or under ${budget_dollars.value:,} and an average tax bill under ${tax_limit_dollars.value:,}, the cheapest being {passing_towns_sorted[0]['name']} at ${passing_towns_sorted[0]['bill']:,} per year.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Reach at least one result a second way, in this notebook, and show that the two agree. Write a cell that gets the same number from other fields, or open the raw reply in your browser and find each number of one row of your table there. For instance: an average bill is close to the average value times the tax rate divided by 1,000; an order's total equals the sum of its lines; the number of records you collected equals the total the API reports. **At least one of those checks runs as code**, and shows both numbers.
    """)
    return


@app.cell
def _(passing_towns_sorted):
    print(f"{'Town':<20}{'Bill from API':>16}{'Value x Rate / 1000':>22}")
    for _checked_town in passing_towns_sorted:
        _computed_bill = _checked_town["value"] * _checked_town["rate"] / 1000
        print(f"{_checked_town['name']:<20}{_checked_town['bill']:>16,}{_computed_bill:>22,.0f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.* If the agent got it right the first time: *What did you do to verify that?* Pointing to your check in section 6 is enough.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The agent first wrote the sort step as a lambda (sorted(passing_towns, key=lambda t: t["bill"])). I had not learned lambda at this point, so I had it rewritten as a named function, get_bill(town_record), which simply returns the bill field, and to use the key = get_bill instead. I knew to ask for this because lambda is not something we were taught in class, and the named function accomplishes the same thing that the lambda did in an equally understandable manner, from my knowledge of what it does.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    Pick two functions in your notebook that your agent wrote or helped write. For each, write in your own words what goes in, what comes out, and one line you had to ask about. Then choose one change to what the tool does, such as another county, another week or another rule. Changing one value in your Inputs cell is enough. Write what you expect to change in the answer. Commit with the message `mp2: prediction`, make the change, run it, and write what happened and whether it matched.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1) get_towns(county_name): in county name Out all the town records for that county, and the count from the API (using a loop to get all of them, since the API only gives you 100 per page). The line that I had to ask about was data["pagination"]["has_next"], which pulls the "has_next" part of a record within a record to tell the loop to stop.

    2) get_year_record(dor_code, year): in the code of the town and the number of the fiscal year. As an output, it returns the record of the indicated year in the given town (value, rate, bill), or None if the town does not have any data for that year. The line that I had to trace was the for year_record in data["years"]: loop, which simply iterates over every record in the years list until the required year is found.

    Change I'll try: decreasing the budget to $500,000 instead of $700,000, leaving the rest as default. The result I expect: a lower number of towns that would pass the test, since it's now harder to stay under the threshold, hence a shorter list, but again in cheapest-first order, with Malden on top for having the lowest taxes.

    What happened: I changed budget_dollars to 500000 in the Inputs cell and reran the notebook. The list shrank from 12 towns to 4 (Malden, Everett, Ashby, Townsend), still sorted cheapest bill first, and Malden stayed on top at $4,952, exactly as I predicted. The other 8 towns that passed before, like Waltham and Dracut, dropped out because their average home value was above $500,000, even though their bills were still under the $8,000 limit. This matched my prediction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    What you tried past the main task, what you found, and where it is in the notebook.
    """)
    return


@app.cell
def _(base_url, passing_towns_sorted, requests):
    # Pull the full history for the 3 towns with the lowest bill, and keep only the last 10 fiscal years
    top_three = passing_towns_sorted[0:3]

    bill_history = []
    skipped_rows = 0
    for _top_town in top_three:
        _response = requests.get(f"{base_url}/towns/{_top_town['dor_code']}/history")
        _data = _response.json()
        _recent_years = _data["years"][-10:]
        for _year_record in _recent_years:
            if _year_record["average_single_family_bill_dollars"] is None:
                skipped_rows = skipped_rows + 1
                continue
            bill_history.append({
                "name": _top_town["name"],
                "year": _year_record["fiscal_year"],
                "bill": _year_record["average_single_family_bill_dollars"],
            })

    print(f"{'Town':<15}{'Year':>8}{'Bill ($)':>12}")
    for _row in bill_history:
        print(f"{_row['name']:<15}{_row['year']:>8}{_row['bill']:>12,}")

    print()
    print(f"Skipped {skipped_rows} year(s) with no bill on record.")
    return (bill_history,)


@app.cell
def _(bill_history):
    import altair as alt

    chart = alt.Chart(alt.Data(values=bill_history)).mark_line(point=True).encode(
        x=alt.X("year:O", title="Fiscal Year"),
        y=alt.Y("bill:Q", title="Average Bill ($)"),
        color=alt.Color("name:N", title="Town"),
        tooltip=["name:N", "year:O", "bill:Q"],
    ).properties(
        title="10-Year Bill History for the 3 Cheapest Towns",
        width=500,
        height=300,
    )
    chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the 3 towns with the cheapest bill on my list (Malden, Waltham, Dracut), I pulled their last 10 fiscal years of history and charted the bill over time, two cells above this one. Dracut's bill has climbed steadily every year. Malden and Waltham are missing several years of bill data (10 rows skipped in total, reported in the cell's output), but in the years they do have, Waltham's bill dipped slightly before climbing again, while Malden rose steadily. None of the three ever came close to the $8,000 limit in the last decade, so the couple's budget has some room before these towns would price them out.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    About how many hours this project took you outside class, as one number. It is not graded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Outside the class it took me 2 hrs to finish my project
    """)
    return


if __name__ == "__main__":
    app.run()
