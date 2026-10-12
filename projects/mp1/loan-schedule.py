# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
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
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
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
    I am going to make a tool that will generate a month-by-month repayment schedule that shows the monthly payment, interest, principal, and remaining balance. I am working on this tool because I have a friend who is borrowing $ 400,000 for a condo and needs to compare a 30-year mortgage at 7.03% vs. a 15-year mortgage at 6.42%.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 1: Define Inputs $400000 loan and the dictionary of rates for 15 and 30 years.
    Step 2: Create a function or loop that calculates the fixed monthly payment using the provided formula .
    Step 3: Use the above-written formula to calculate the monthly payment before scheduling the calculations for each month.
    Step 4: Schedule the loop to iterate for the number of months specified (i.e., 1 to n).
    Step 5: Calculate the interest for one month by multiplying the monthly rate by the outstanding loan amount balance.
    Step 6:Calculate the principal paid for one month by subtracting the monthly interest from the monthly payment.
    Step 7: Update the outstanding loan balance by subtracting the principal paid from the previous month’s ending balance.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Answer-1 The main variable the loop carries forward is the remaining loan amount. Each month, that amount gets smaller as the next payment is due, and the next iteration carries that new total into the calculation of the next interest charge. I will also carry forward the amount of total interest paid.
    Answer-2 I will provide you with the total amount paid over the life of the loan. In section 6, the sum of all monthly payments of principal must equal the initial loan amount ($400,000).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    r30 = annual_rates[30] / 12
    n30 = 30 * 12
    payment_30 =  round(loan_amount * r30 /(1- (1 + r30)**- n30),2)
    payment_30
    return n30, payment_30, r30


@app.cell
def _(annual_rates, loan_amount):
    r15 = annual_rates[15] / 12
    n15 = 15 * 12
    payment_15 = round(loan_amount * r15 / (1 - (1 + r15) ** -n15), 2)
    payment_15
    return n15, payment_15, r15


@app.cell
def _(loan_amount, n30, payment_30, r30):
    balance_30 = loan_amount
    total_interest_30 = 0
    total_principal_30 = 0
    print(f"{'Month':>5} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>10}")
    for month in range(1, n30 + 1):
        interest = round(balance_30 * r30, 2)
        if month == n30:
            principal = balance_30
            payment_this_month = balance_30 + interest
        else:
            payment_this_month = payment_30
            principal = payment_this_month - interest
        balance_30 = round(balance_30 - principal, 2)
        total_interest_30 = total_interest_30 + interest
        total_principal_30 = total_principal_30 + principal
        print(f"{month:>5} {payment_this_month:>10,.2f} {interest:>10,.2f} {principal:>10,.2f} {balance_30:>10,.2f}")
    return total_interest_30, total_principal_30


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Although the 15-year loan has  a higher monthly payment ($3,466.86 vs $2,669.27), it saves my friend ($336,906.69) in total interest over the life of the loan ($224,035.34 vs $560,942.03), making in the better choice if he can afford the higher payment.
    """)
    return


@app.cell
def _(loan_amount, n15, payment_15, payment_30, r15, total_interest_30):
    def _():
        balance_15 = loan_amount
        total_interest_15 = 0
        total_principal_15 = 0
        print(f"{'Month':>5} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>10}")
        for month in range(1, n15 + 1):
            interest = round(balance_15 * r15, 2)
            if month == n15:
                principal = balance_15
                payment_this_month = balance_15 + interest
            else:
                payment_this_month = payment_15
                principal = payment_this_month - interest
            balance_15 = round(balance_15 - principal, 2)
            total_interest_15 = total_interest_15 + interest
            total_principal_15 = total_principal_15 + principal
            print(f"{month:>5} {payment_this_month:>10,.2f} {interest:>10,.2f} {principal:>10,.2f} {balance_15:>10,.2f}")

        print(f"30-year loan: monthly payment ${payment_30:,.2f}, total interest ${total_interest_30:,.2f}")
        return print(f"15-year loan: monthly payment ${payment_15:,.2f}, total interest ${total_interest_15:,.2f}")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(loan_amount, total_principal_30):
    print(f"Sum of principal paid (30-year): ${total_principal_30:,.2f}")
    print(f"Original loan amount: ${loan_amount:,.2f}")
    print(f"Do they match? {round(total_principal_30, 2) == loan_amount}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I summed each month's principal payment for the 30-year mortgage and compared this amount to the initial loan amount ($400,000), and they were equal, which means the schedule is accurate and does not miss or add any money.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When creating the 15-year schedule in section 4, the AI provided me with code that redefined a variable I had already used for the 30-year schedule, which is not permitted in marimo; a variable can only be defined once in one's notebook. This resulted in an error, which I resolved by eliminating the redefined variable in that section. After doing so, I noticed that the error message indicated that there was a problem with the same variable name in two different cells; thus, running this cell again worked without error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(loan_amount, n30, payment_30, r30, total_interest_30):
    def _():
        extra_payment = 100
        balance_extra = loan_amount
        total_interest_extra = 0
        months_used = 0

        for month in range(1, n30 + 1):
            if balance_extra > 0:
                interest = round(balance_extra * r30, 2)
                payment_this_month = payment_30 + extra_payment
                principal = payment_this_month - interest
                if principal > balance_extra:
                    principal = balance_extra
                balance_extra = round(balance_extra - principal, 2)
                total_interest_extra = total_interest_extra + interest
                months_used = months_used + 1

        print(f"With an extra ${extra_payment} a month, the 30-year loan is paid off in {months_used} months instead of {n30}.")
        print(f"Total interest paid: ${total_interest_extra:,.2f}, compared to ${total_interest_30:,.2f} without the extra payment.")
        print(f"Interest saved: ${total_interest_30 - total_interest_extra:,.2f}")


    _()
    return


@app.cell
def _(mo):
    mo.md(r"""
    I tried adding an extra $100 to every monthly payment on the 30-year loan, to see if a small habit makes a real difference. It paid off the loan in 321 months instead of 360 (about 3 years sooner), and saved $73,421.70 in total interest. The code is in the cell above, in Section 8.
    """)
    return


@app.cell
def _(mo):
    payoff_years_input = mo.ui.slider(start=5, stop=30, value=20, step=1, label="Years to pay off the 30-year loan")
    payoff_years_input
    return (payoff_years_input,)


@app.cell
def _(loan_amount, payment_30, payoff_years_input, r30, total_interest_30):
    def _():
        payoff_months = payoff_years_input.value * 12
        payoff_payment = round(loan_amount * r30 / (1 - (1 + r30) ** -payoff_months), 2)

        balance_payoff = loan_amount
        total_interest_payoff = 0
        for month in range(1, payoff_months + 1):
            interest = round(balance_payoff * r30, 2)
            if month == payoff_months:
                principal = balance_payoff
                payment_this_month = balance_payoff + interest
            else:
                payment_this_month = payoff_payment
                principal = payment_this_month - interest
            balance_payoff = round(balance_payoff - principal, 2)
            total_interest_payoff = total_interest_payoff + interest

        print(f"To pay off the loan in {payoff_years_input.value} years, the monthly payment would be ${payoff_payment:,.2f}.")
        print(f"That compares to ${payment_30:,.2f} a month on the original 30-year schedule.")
        print(f"Total interest paid: ${total_interest_payoff:,.2f}, compared to ${total_interest_30:,.2f} over the full 30 years.")
        print(f"Interest saved: ${total_interest_30 - total_interest_payoff:,.2f}")


    _()
    return


if __name__ == "__main__":
    app.run()
