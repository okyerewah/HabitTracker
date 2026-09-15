from habit import VALID_PERIODICITIES

def track_habits(habits):
    """Returns all habits with their current streaks."""
    return list(map(lambda h: (h.name, h.periodicity, h.current_streak()), habits))


def get_habits_by_periodicity(habits, periodicity):
    """Filters habits by periodicity (daily or weekly)."""
    if periodicity not in VALID_PERIODICITIES:  
        raise ValueError(f"Periodicity must be 'daily' or 'weekly', not {periodicity!r}.")  
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def get_longest_streak_all(habits):
    """Returns the habit with the longest streak and its value."""
    if not habits:
        return None
    best = max(habits, key=lambda h: h.longest_streak())
    return best.name, best.periodicity, best.longest_streak() 


def get_longest_streak_for_habit(habit):
    """Returns the longest streak for a single habit."""
    return habit.name, habit.longest_streak()