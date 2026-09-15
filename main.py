from tracker import Tracker
import analytics
from fixtures import load_fixtures


def print_habits(habits):
    """Displays a list of habits in a table format."""
    if not habits:
        print("No habits found.")
        return
    print(f"\n{'ID':<5} {'Name':<20} {'Period':<10}")
    print("-" * 35)
    for h in habits:
        print(f"{h.habit_id:<5} {h.name:<20} {h.periodicity:<10}")


def main():
    """Runs the habit tracker from the command-line interface."""
    tracker = Tracker()
    print("Habit Tracker")

    while True:
        print("\n 1. Add habit")
        print(" 2. Complete a task")
        print(" 3. Delete habit")
        print(" 4. View all habits")
        print(" 5. View habits by periodicity")
        print(" 6. View current streaks")
        print(" 7. View longest streak for a habit")
        print(" 8. View longest streak across all habits")
        print(" 9. Load demo data")
        print(" 0. Exit")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            name = input("Habit name: ").strip()
            period = input("Periodicity (daily/weekly): ").strip().lower()
            if period not in ("daily", "weekly"):
                print("Periodicity must be 'daily' or 'weekly'.")
                continue
            h = tracker.add_habit(name, period)
            print(f"Added '{h.name}' ({h.periodicity}).")

        elif choice == "2":
            print_habits(tracker.view_habits())
            try:
                hid = int(input("Habit ID: "))
                newly_added = tracker.complete_task(hid) 
                if newly_added:  
                    print("Marked complete for today.") 
                else:  
                    print("Already marked complete for today.")  
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            print_habits(tracker.view_habits())
            try:
                hid = int(input("Habit ID to delete: "))
                tracker.delete_habit(hid)
                print("Deleted.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            print_habits(tracker.view_habits())

        elif choice == "5":
            period = input("Periodicity (daily/weekly): ").strip().lower()
            try:  
                filtered = analytics.get_habits_by_periodicity(tracker.view_habits(), period)
                print_habits(filtered)
            except ValueError as e:  
                print(f"Error: {e}")  
    

        elif choice == "6":
            streaks = analytics.track_habits(tracker.view_habits())
            if not streaks:
                print("No habits found.")
            else:
                print(f"\n{'Name':<20} {'Period':<10} {'Current Streak':<15}") 
                print("-" * 45)  
                for name, period, streak in streaks:  
                    print(f"{name:<20} {period:<10} {streak:<15}")  

        elif choice == "7":
            print_habits(tracker.view_habits())
            try:
                hid = int(input("Habit ID: "))
                habit = next((h for h in tracker.view_habits() if h.habit_id == hid), None)
                if habit is None:
                    print("Habit not found.")
                else:
                    _, streak = analytics.get_longest_streak_for_habit(habit)  
                    print(f"Longest streak for '{habit.name}': {streak}")  
            except ValueError:
                print("Invalid ID.")

        elif choice == "8":
            result = analytics.get_longest_streak_all(tracker.view_habits())  
            if result is None: 
                print("No habits found.")
            else:
                name, period, streak = result  
                unit = "day(s)" if period == "daily" else "week(s)"  
                print(f"Longest streak: '{name}' with {streak} {unit}.")  

        elif choice == "9":
            load_fixtures(tracker)
            print("Demo data loaded.")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
