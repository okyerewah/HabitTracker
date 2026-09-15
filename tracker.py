from datetime import date
import repository
from habit import Habit


class Tracker:
    """
    Handles creation, updating, deletion, and retrieval of habits.
    """
  
    def __init__(self):
        """Load existing habits from the repository."""
        self.habits = repository.load_habits()

    def _next_id(self):
        """Generates the next available ID for a habit."""
        return max((h.habit_id for h in self.habits), default=0) + 1

    def _find(self, habit_id):
        """Finds a habit using its ID. Returns None if not found."""
        for h in self.habits:
            if h.habit_id == habit_id:
                return h
        return None

    def add_habit(self, name, periodicity):
        """Creates a new habit and saves it to the repository."""
        habit = Habit(self._next_id(), name, periodicity)
        self.habits.append(habit)
        repository.save_habits(self.habits)
        return habit

    def delete_habit(self, habit_id):
        """Deletes a habit specified by an ID."""
        habit = self._find(habit_id)
        if habit is None:
            raise ValueError(f"No habit with ID {habit_id}.")
        self.habits.remove(habit)
        repository.save_habits(self.habits)

    def complete_task(self, habit_id, completion_date=None):
        """Marks a habit as completed for a given date (defaults to today)."""
        habit = self._find(habit_id)
        if habit is None:
            raise ValueError(f"No habit with ID {habit_id}.")
        d = completion_date or date.today()
        already_done = d in habit.completions 
        if not already_done: 
            habit.completions.append(d)
        repository.save_habits(self.habits)
        return not already_done  

    def view_habits(self):
        """Returns a list of all tracked habits."""
        return list(self.habits)
