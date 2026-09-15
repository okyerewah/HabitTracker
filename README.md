# Habit Tracker

A command-line application built in Python that allows a user to create habits and track them through completions.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/okyerewah/HabitTracker.git
   cd HabitTracker
   ```

2. Install pytest (needed to run the test suite):

   ```bash
   pip install pytest
   ```

## Usage

Run the app from the project directory:

```bash
python main.py
```

The following menu will be displayed:

```
Habit Tracker

 1. Add habit
 2. Complete a task
 3. Delete habit
 4. View all habits
 5. View habits by periodicity
 6. View current streaks
 7. View longest streak for a habit
 8. View longest streak across all habits
 9. Load demo data
 0. Exit
```

Select an option by typing its number and pressing Enter.

- **Add habit (1):** enter a name and a periodicity (`daily` or `weekly`) to create a new habit.
- **Complete a task (2):** enter the ID of the habit you want to check off for today. Completing the same habit twice on the same day only counts once.
- **Delete habit (3):** remove a habit permanently by its ID.
- **View all habits / by periodicity (4, 5):** list habits, optionally filtered to `daily` or `weekly`.
- **View current streaks (6):** shows every habit's current consecutive-period streak.
- **Longest streak for a habit / across all habits (7, 8):** shows the best streak ever achieved.
- **Load demo data (9):** loads the 5 predefined habits with 4 weeks of example completions.

## Running the tests

The test suite uses `pytest` and runs against a temporary, isolated JSON file so it never touches your real `habits.json`:

```bash
pytest test_habits.py
```

## Project structure

```
.
├── main.py          # CLI entry point and menu loop
├── habit.py          # Habit class: stores habit data and streak logic
├── tracker.py         # Tracker class: create/delete/complete/view habits
├── repository.py       # JSON persistence (save/load habits.json)
├── analytics.py        # Functional-programming analytics module
├── fixtures.py         # Predefined habits + 4 weeks of example completion data
├── test_habits.py       # pytest unit test suite
└── habits.json         # Stored habit data (created/updated automatically)
```
