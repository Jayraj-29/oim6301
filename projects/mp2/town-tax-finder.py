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

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 2

    Save it in your course repository as `projects/mp2/<your-tool>.py`, named for what it does, such as `town-tax-finder.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Your functions, and the code that uses them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Your result table, printed with `print` and f-strings with the columns lined up, and one sentence that answers the question in section 1 with the numbers in it. Print the sentence from code with an f-string, so that it changes when the data does.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Reach at least one result a second way, in this notebook, and show that the two agree. Write a cell that gets the same number from other fields, or open the raw reply in your browser and find each number of one row of your table there. For instance: an average bill is close to the average value times the tax rate divided by 1,000; an order's total equals the sum of its lines; the number of records you collected equals the total the API reports. **At least one of those checks runs as code**, and shows both numbers.
    """)
    return


@app.cell
def _():
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
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    What you tried past the main task, what you found, and where it is in the notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
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
 
    """)
    return


if __name__ == "__main__":
    app.run()
