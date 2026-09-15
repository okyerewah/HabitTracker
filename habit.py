from datetime import datetime, date, timedelta


DAILY = "daily"
WEEKLY = "weekly"
VALID_PERIODICITIES = (DAILY, WEEKLY)


class Habit:
    """
    Represents a habit being tracked in the application.

    Attributes:
       habit_id: Unique ID for the habit.
       name: Name of the habit.
       periodicity: Habit frequency, either "daily" or "weekly".
       created_at: Date and time the habit was created.
       completions: List of dates the habit was completed on.
    """
    def __init__(self, habit_id, name, periodicity, created_at=None, completions=None):
      
        if periodicity not in VALID_PERIODICITIES:
            raise ValueError("Periodicity must be 'daily' or 'weekly'.")
          
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.completions = completions or []      
        

    def current_streak(self):
        """Returns the number of consecutive completions starting from the current day"""
        if not self.completions:
            return 0

        today = date.today()
        streak = 0

        if self.periodicity == DAILY:
            check = today

            if check not in self.completions:      
                check -= timedelta(days=1)
          
            while check in self.completions:
                streak += 1
                check -= timedelta(days=1)
        else:
            week_starts = set()
            for d in self.completions:
                week_starts.add(d - timedelta(days=d.weekday()))

            check = today - timedelta(days=today.weekday())
            if check not in week_starts:          
                check -= timedelta(weeks=1)
            while check in week_starts:
                streak += 1
                check -= timedelta(weeks=1)

        return streak


    def longest_streak(self):
        """Returns the longest number of consecutive completions ever achieved for this habit"""
        if not self.completions:
            return 0

        longest = 1
        current = 1

        if self.periodicity == DAILY:
            dates = sorted(set(self.completions))
            for i in range(1, len(dates)):
                if (dates[i] - dates[i - 1]).days == 1:
                    current += 1
                    if current > longest:
                        longest = current
                else:
                    current = 1
        else:
            week_starts = set()
            for d in self.completions:
                week_starts.add(d - timedelta(days=d.weekday()))

            weeks = sorted(week_starts)
            for i in range(1, len(weeks)):
                if (weeks[i] - weeks[i - 1]).days == 7:
                    current += 1
                    if current > longest:
                        longest = current
                else:
                    current = 1

        return longest


    def to_dict(self):
        """Converts a habit object into a dictionary object to allow it to be saved in JSON storage."""
        return {
            "habit_id": self.habit_id,
            "name": self.name,
            "periodicity": self.periodicity,
            "created_at": self.created_at.isoformat(),
            "completions": [d.isoformat() for d in self.completions],
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Habit object from a dictionary object when loading from JSON."""
        return cls(
            habit_id=data["habit_id"],
            name=data["name"],
            periodicity=data["periodicity"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completions=[date.fromisoformat(d) for d in data["completions"]],
        )
