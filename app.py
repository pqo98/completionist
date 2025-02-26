import json
import os

# Data structure with hierarchical nesting
completionist = {
    "ultimate": [],  # Just a name, no XP or completion
    "main": []       # Each main goal has "objectives", each objective has "tasks"
}
stats = {"xp": 0}

def save_data():
    with open("completionist.json", "w") as f:
        json.dump({"completionist": completionist, "stats": stats}, f)

def load_data():
    global completionist, stats
    default_completionist = {"ultimate": [], "main": []}
    default_stats = {"xp": 0}
    
    if os.path.exists("completionist.json"):
        try:
            with open("completionist.json", "r") as f:
                data = json.load(f)
                loaded_completionist = data.get("completionist", default_completionist)
                stats = data.get("stats", default_stats)
                completionist["ultimate"] = loaded_completionist.get("ultimate", [])
                completionist["main"] = loaded_completionist.get("main", [])
        except (json.JSONDecodeError, FileNotFoundError):
            completionist.update(default_completionist)
            stats.update(default_stats)
    else:
        completionist.update(default_completionist)
        stats.update(default_stats)

def clear_data():
    global completionist, stats
    completionist = {"ultimate": [], "main": []}
    stats = {"xp": 0}
    if os.path.exists("completionist.json"):
        os.remove("completionist.json")
    print("All data cleared!")

def get_choice(max_option):
    print("\n-----")
    print("> Select choice (1-{}) or Cancel (0): ".format(max_option), end="")
    return input()

def view_main_goal(main_idx):
    goal = completionist["main"][main_idx]
    print(f"\nMain Goal: {goal['name']} ({goal['xp']} XP) [{'Done' if goal['completed'] else 'Pending'}]")
    for i, obj in enumerate(goal.get("objectives", [])):
        status = "[Done]" if obj["completed"] else "[Pending]"
        print(f"  {i}. Objective: {obj['name']} ({obj['xp']} XP, Due: {obj['due_date']}) {status}")
        for task in obj.get("tasks", []):
            task_status = "[Done]" if task["completed"] else "[Pending]"
            print(f"    - {task['name']} ({task['xp']} XP, Due: {task['due_date']}) {task_status}")

def main():
    load_data()
    while True:
        print("\nCompletionist")
        print("1. View Dashboard")
        print("2. Add Goal")
        print("3. Finish Goal")
        print("4. Clear All Data")
        print("5. Exit")
        choice = get_choice(5)
        
        if choice == "1":
            level = stats["xp"] // 100
            ultimate = completionist["ultimate"][0] if completionist["ultimate"] else {"name": "Not set"}
            print("\n-- Dashboard --")
            print(f"Ultimate Goal: {ultimate['name']}")
            print(f"Stats: XP = {stats['xp']}, Level = {level}")
            print("\nMain Goals:")
            for i, goal in enumerate(completionist["main"]):
                status = "[Done]" if goal["completed"] else "[Pending]"
                print(f"{i + 1}. {goal['name']} ({goal['xp']} XP) {status}")
            
            if completionist["main"]:
                sub_choice = get_choice(len(completionist["main"]))
                if sub_choice == "0":
                    continue
                try:
                    main_idx = int(sub_choice) - 1
                    if 0 <= main_idx < len(completionist["main"]):
                        view_main_goal(main_idx)
                    else:
                        print("Invalid Main Goal!")
                except ValueError:
                    print("Invalid input!")
            else:
                print("\nNo Main Goals yet.")
        elif choice == "2":
            print("\nGoal Types: 1. Ultimate  2. Main  3. Objective  4. Task")
            type_choice = get_choice(4)
            
            if type_choice == "0":
                continue
            elif type_choice in ["1", "2", "3", "4"]:
                name = input("Enter goal name: ")
                if type_choice == "1":
                    if completionist["ultimate"]:
                        print("Ultimate Goal already set! Replacing it.")
                    completionist["ultimate"] = [{"name": name}]
                elif type_choice == "2":
                    xp = int(input("Enter XP value: "))
                    completionist["main"].append({"name": name, "xp": xp, "completed": False, "objectives": []})
                elif type_choice == "3":
                    if not completionist["main"]:
                        print("Add a Main Goal first!")
                        continue
                    print("\nMain Goals:")
                    for i, goal in enumerate(completionist["main"]):
                        print(f"{i}. {goal['name']}")
                    main_idx = int(input("Select Main Goal to add Objective to (number): "))
                    if 0 <= main_idx < len(completionist["main"]):
                        xp = int(input("Enter XP value: "))
                        due_date = input("Enter due date (YYYY-MM-DD): ")
                        completionist["main"][main_idx]["objectives"] = completionist["main"][main_idx].get("objectives", [])
                        completionist["main"][main_idx]["objectives"].append({"name": name, "xp": xp, "due_date": due_date, "completed": False, "tasks": []})
                    else:
                        print("Invalid Main Goal!")
                        continue
                elif type_choice == "4":
                    if not completionist["main"]:
                        print("Add a Main Goal first!")
                        continue
                    print("\nMain Goals:")
                    for i, goal in enumerate(completionist["main"]):
                        print(f"{i}. {goal['name']}")
                    main_idx = int(input("Select Main Goal (number): "))
                    if not (0 <= main_idx < len(completionist["main"])):
                        print("Invalid Main Goal!")
                        continue
                    if not completionist["main"][main_idx].get("objectives", []):
                        print("Add an Objective first!")
                        continue
                    print("\nObjectives:")
                    for i, obj in enumerate(completionist["main"][main_idx]["objectives"]):
                        print(f"{i}. {obj['name']}")
                    obj_idx = int(input("Select Objective to add Task to (number): "))
                    if 0 <= obj_idx < len(completionist["main"][main_idx]["objectives"]):
                        xp = int(input("Enter XP value: "))
                        due_date = input("Enter due date (YYYY-MM-DD): ")
                        completionist["main"][main_idx]["objectives"][obj_idx]["tasks"] = completionist["main"][main_idx]["objectives"][obj_idx].get("tasks", [])
                        completionist["main"][main_idx]["objectives"][obj_idx]["tasks"].append({"name": name, "xp": xp, "due_date": due_date, "completed": False})
                    else:
                        print("Invalid Objective!")
                        continue
                print(f"Added '{name}'!")
            else:
                print("Invalid type!")
        elif choice == "3":
            print("\nSelect goal type: 1. Main  2. Objective  3. Task")
            type_choice = get_choice(3)
            
            if type_choice == "0":
                continue
            elif type_choice in ["1", "2", "3"]:
                if not completionist["main"]:
                    print("No Main Goals to finish!")
                    continue
                print("\nMain Goals:")
                for i, goal in enumerate(completionist["main"]):
                    print(f"{i}. {goal['name']} ({goal['xp']} XP) [{'Done' if goal['completed'] else 'Pending'}]")
                main_idx = int(input("Select Main Goal (number): "))
                if not (0 <= main_idx < len(completionist["main"])):
                    print("Invalid Main Goal!")
                    continue
                
                if type_choice == "1":
                    goal = completionist["main"][main_idx]
                    if not goal["completed"]:
                        goal["completed"] = True
                        stats["xp"] += goal["xp"]
                        print(f"Finished '{goal['name']}'! +{goal['xp']} XP")
                    else:
                        print("Already done!")
                elif type_choice == "2":
                    if not completionist["main"][main_idx].get("objectives"):
                        print("No Objectives to finish!")
                        continue
                    print("\nObjectives:")
                    for i, obj in enumerate(completionist["main"][main_idx]["objectives"]):
                        print(f"{i}. {obj['name']} ({obj['xp']} XP, Due: {obj['due_date']}) [{'Done' if obj['completed'] else 'Pending'}]")
                    obj_idx = int(input("Select Objective (number): "))
                    if 0 <= obj_idx < len(completionist["main"][main_idx]["objectives"]):
                        obj = completionist["main"][main_idx]["objectives"][obj_idx]
                        if not obj["completed"]:
                            obj["completed"] = True
                            stats["xp"] += obj["xp"]
                            print(f"Finished '{obj['name']}'! +{obj['xp']} XP")
                        else:
                            print("Already done!")
                    else:
                        print("Invalid Objective!")
                elif type_choice == "3":
                    if not any(obj.get("tasks") for obj in completionist["main"][main_idx].get("objectives", [])):
                        print("No Tasks to finish!")
                        continue
                    print("\nObjectives:")
                    for i, obj in enumerate(completionist["main"][main_idx]["objectives"]):
                        print(f"{i}. {obj['name']}")
                    obj_idx = int(input("Select Objective (number): "))
                    if not (0 <= obj_idx < len(completionist["main"][main_idx]["objectives"])):
                        print("Invalid Objective!")
                        continue
                    if not completionist["main"][main_idx]["objectives"][obj_idx].get("tasks"):
                        print("No Tasks to finish!")
                        continue
                    print("\nTasks:")
                    for i, task in enumerate(completionist["main"][main_idx]["objectives"][obj_idx]["tasks"]):
                        print(f"{i}. {task['name']} ({task['xp']} XP, Due: {task['due_date']}) [{'Done' if task['completed'] else 'Pending'}]")
                    task_idx = int(input("Select Task (number): "))
                    if 0 <= task_idx < len(completionist["main"][main_idx]["objectives"][obj_idx]["tasks"]):
                        task = completionist["main"][main_idx]["objectives"][obj_idx]["tasks"][task_idx]
                        if not task["completed"]:
                            task["completed"] = True
                            stats["xp"] += task["xp"]
                            print(f"Finished '{task['name']}'! +{task['xp']} XP")
                        else:
                            print("Already done!")
                    else:
                        print("Invalid Task!")
            else:
                print("Invalid type!")
        elif choice == "4":
            clear_data()
        elif choice == "5":
            save_data()
            print("Catch you later!")
            break
        elif choice == "0":
            continue
        else:
            print("Invalid choice, try again.")
            
if __name__ == "__main__":
    main()