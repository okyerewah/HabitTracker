from datetime import date, timedelta


PREDEFINED = [
    ("Exercise", "daily"),
    ("Feed pets", "daily"),
    ("Meditate", "daily"),
    ("Swim lessons", "weekly"),
    ("Weekly Review", "weekly"),
]

# 28-day completion data (1 = done, 0 = missed)
HISTORY = {
    "Exercise":      [1,1,1,0,1,1,1, 1,0,1,1,1,1,0, 1,0,0,0,0,0,0, 1,1,0,1,1,1,1],
    "Feed pets":     [1,1,0,1,1,1,1, 0,1,1,1,0,1,1, 1,1,1,1,1,0,1, 0,1,1,1,1,1,1],
    "Meditate":      [1,0,1,1,1,0,1, 1,1,0,1,1,1,1, 0,1,1,1,1,1,0, 1,1,1,0,1,1,1],
    "Swim lessons":  [0,0,0,0,0,0,0, 0,0,1,0,0,0,0, 0,0,0,1,0,0,0, 0,0,0,1,0,0,0],
    "Weekly Review": [1,0,0,0,0,0,0, 1,0,0,0,0,0,0, 1,0,0,0,0,0,0, 1,0,0,0,0,0,0],
}


def load_fixtures(tracker):
    """ Loads predefined habits and completion data into the tracker after checking if they already exist first. """
    today = date.today()
  
    #Prevent duplicates
    existing_names = {h.name for h in tracker.view_habits()}
    for name, periodicity in PREDEFINED:
        if name in existing_names:  
            continue
          
        habit = tracker.add_habit(name, periodicity)
        for i, done in enumerate(HISTORY[name]):
            if done:
                day = today - timedelta(days=27 - i)
                tracker.complete_task(habit.habit_id, day)
