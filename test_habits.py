import pytest
from datetime import date, timedelta, datetime

from habit import Habit
import repository
from tracker import Tracker
import analytics
from fixtures import load_fixtures, PREDEFINED  


@pytest.fixture(autouse=True)
def isolate_repository_file(tmp_path, monkeypatch):
    """Point repository.FILE at a temporary file to avoid affecting real habit data."""
    test_file = tmp_path / "test_habits.json"
    monkeypatch.setattr(repository, "FILE", str(test_file))


# Habit tests

def test_habit_creation():
    h = Habit(1, "Run", "daily")
    assert h.habit_id == 1
    assert h.name == "Run"
    assert h.periodicity == "daily"
    assert h.created_at is not None
    assert h.completions == []


def test_current_streak():
    today = date.today()
    h = Habit(1, "Run", "daily")
    h.completions = [today - timedelta(days=i) for i in range(4)]
    assert h.current_streak() == 4


def test_longest_streak():
    today = date.today()
    h = Habit(1, "Run", "daily")
    h.completions = (
        [today - timedelta(days=20 + i) for i in range(5)]
        + [today - timedelta(days=1), today - timedelta(days=2)]
    )
    assert h.longest_streak() == 5


def test_invalid_periodicity_raises():  
    with pytest.raises(ValueError):  
        Habit(1, "Bad", "monthly")  


def test_streaks_zero_with_no_completions(): 
    h = Habit(1, "Empty", "daily")  
    assert h.current_streak() == 0 
    assert h.longest_streak() == 0 


def test_broken_streak_resets_to_zero():  
    today = date.today()  
    h = Habit(1, "Run", "daily", completions=[today - timedelta(days=10), today - timedelta(days=11)])  
    assert h.current_streak() == 0  


# Tracker tests

def test_add_habit():
    tracker = Tracker()
    tracker.habits = []
    habit = tracker.add_habit("Run", "daily")
    assert len(tracker.habits) == 1
    assert tracker.habits[0].name == "Run"


def test_delete_habit():
    tracker = Tracker()
    tracker.habits = []
    h = tracker.add_habit("Run", "daily")
    tracker.delete_habit(h.habit_id)
    assert len(tracker.habits) == 0


def test_complete_task():
    tracker = Tracker()
    tracker.habits = []
    h = tracker.add_habit("Run", "daily")
    today = date.today()
    tracker.complete_task(h.habit_id, today)
    assert today in tracker.habits[0].completions


def test_view_habits():
    tracker = Tracker()
    tracker.habits = []
    tracker.add_habit("Run", "daily")
    tracker.add_habit("Read", "daily")
    tracker.add_habit("Meditate", "daily")
    assert len(tracker.view_habits()) == 3


def test_delete_nonexistent_habit_raises():  
    tracker = Tracker() 
    tracker.habits = [] 
    with pytest.raises(ValueError):  
        tracker.delete_habit(999) 


def test_complete_task_nonexistent_habit_raises():  
    tracker = Tracker()  
    tracker.habits = []  
    with pytest.raises(ValueError):  
        tracker.complete_task(999)  


def test_duplicate_completion_not_added_twice():  
    tracker = Tracker() 
    tracker.habits = []  
    habit = tracker.add_habit("Dup", "daily")  
    today = date.today()  
    first = tracker.complete_task(habit.habit_id, today)  
    second = tracker.complete_task(habit.habit_id, today)
    assert len(habit.completions) == 1
    assert first is True   
    assert second is False  


# Repository tests

def test_save_and_load_habits():
    today = date.today()
    habits = [
        Habit(1, "Run", "daily", datetime.now(), [today]),
        Habit(2, "Review", "weekly"),
    ]
    repository.save_habits(habits)
    loaded = repository.load_habits()
    assert loaded[0].name == "Run"
    assert loaded[0].completions == [today]
    assert loaded[1].periodicity == "weekly"


# Analytics tests

def test_track_habits():
    today = date.today()
    habits = [
        Habit(1, "Run", "daily", datetime.now(), [today - timedelta(days=i) for i in range(5)]),
        Habit(2, "Read", "daily", datetime.now(), [today - timedelta(days=i) for i in range(3)]),
    ]
    result = analytics.track_habits(habits)
    assert len(result) == 2
    assert all(isinstance(streak, int) for _, _, streak in result)


def test_get_habits_by_periodicity():
    daily1 = Habit(1, "Run", "daily")
    daily2 = Habit(2, "Read", "daily")
    weekly1 = Habit(3, "Review", "weekly")
    habits = [daily1, daily2, weekly1]
    assert len(analytics.get_habits_by_periodicity(habits, "daily")) == 2
    assert len(analytics.get_habits_by_periodicity(habits, "weekly")) == 1


def test_get_longest_streak_for_habit():
    today = date.today()
    h = Habit(1, "Run", "daily", datetime.now(), [today - timedelta(days=i) for i in range(5)])
    name, streak = analytics.get_longest_streak_for_habit(h)
    assert name == "Run"
    assert streak == 5


def test_get_longest_streak_all():
    today = date.today()
    daily1 = Habit(1, "Run", "daily", datetime.now(), [today - timedelta(days=i) for i in range(5)])
    daily2 = Habit(2, "Read", "daily", datetime.now(), [today - timedelta(days=i) for i in range(3)])
    weekly1 = Habit(3, "Review", "weekly", datetime.now(), [today - timedelta(weeks=i) for i in range(4)])
    name, period, streak = analytics.get_longest_streak_all([daily1, daily2, weekly1])
    assert name == "Run"


def test_get_longest_streak_all_empty():  
    assert analytics.get_longest_streak_all([]) is None  


# Fixtures tests

def test_fixtures_load():
    tracker = Tracker()
    tracker.habits = []
    load_fixtures(tracker)
    for h in tracker.habits:
        assert len(h.completions) > 0


def test_fixtures_count():
    tracker = Tracker()
    tracker.habits = []
    load_fixtures(tracker)
    assert len(tracker.habits) == 5


def test_fixture_mix():
    tracker = Tracker()
    tracker.habits = []
    load_fixtures(tracker)
    periodicities = {h.periodicity for h in tracker.habits}
    assert "daily" in periodicities
    assert "weekly" in periodicities


def test_load_fixtures_twice_no_duplicates(): 
    tracker = Tracker()  
    tracker.habits = []  
    load_fixtures(tracker) 
    load_fixtures(tracker)  
    assert len(tracker.habits) == len(PREDEFINED)  