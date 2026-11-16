# BabsonAI Labs Database

## 1. The Scenario

**A. BabsonAI Labs.** A 25-person startup that builds AI tools for small businesses. It tracks who works on what, where the money goes, and who is overloaded: its people and who they report to, its projects and their budgets, who works on which project and how many hours a week, the tasks on each project and who they are assigned to, and the expenses charged to each project.

## 2. The ERD

```mermaid
erDiagram
    PEOPLE }o--|o PEOPLE : "reports to"
    PEOPLE ||--o{ ASSIGNMENTS : "works on"
    PROJECTS ||--o{ ASSIGNMENTS : includes
    PROJECTS ||--o{ TASKS : has
    PEOPLE |o--o{ TASKS : "is assigned"
    PROJECTS ||--o{ EXPENSES : has

    PEOPLE {
        int person_id PK
        string first_name
        string last_name
        string work_email UK
        string title
        date start_date
        int manager_id FK
    }
    PROJECTS {
        int project_id PK
        string name
        string client_name
        string category
        decimal budget
        date start_date
        string status
    }
    ASSIGNMENTS {
        int project_id PK "FK"
        int person_id PK "FK"
        string role
        int hours_per_week
        date joined_date
    }
    TASKS {
        int task_id PK
        int project_id FK
        string description
        date created_date
        int assigned_to FK
        date due_date
        date completed_date
    }
    EXPENSES {
        int expense_id PK
        int project_id FK
        date expense_date
        decimal amount
        string category
        string note
    }
```

## 3. What One Row Means

*(To do, by hand: one sentence per table, in the way Northwind's would read, e.g. "One row of `orders` is one order placed by one customer." Tables: `people`, `projects`, `assignments`, `tasks`, `expenses`.)*

## 4. Design Choices

**The key.** *(To do, by hand: which key you chose where the business already had one, such as an email, and why.)*

**Optional relationships.** *(To do, by hand: which relationships are optional, and what in the scenario tells you so.)*

**The rule the tables cannot hold.** *(To do, by hand: which of the scenario's rules your tables cannot hold with a `CHECK`, and how you check it instead.)*

**Working with the agent.** *(To do, by hand: one thing your agent proposed for the design that you changed or did not take, and why; if you designed it alone, one thing you checked in the ERD your agent drew.)*