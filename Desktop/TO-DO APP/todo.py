tasks = []

def show_tasks():
    if tasks:
        print("Tasks to do:")
        for index, task in enumerate(tasks, 1):
            print(f"{index}. {task}")
    else:
        print("No tasks to show!")

def add_task(task):
    tasks.append(task)
    print(f"Task '{task}' added.")

def remove_task(index):
    try:
        task = tasks.pop(index - 1)
        print(f"Task '{task}' removed.")
    except IndexError:
        print("Invalid task number.")

def main():
    while True:
        print("\nTo-Do App")
        print("1. Show tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_tasks()
        elif choice == "2":
            task = input("Enter the task: ")
            add_task(task)
        elif choice == "3":
            show_tasks()
            try:
                task_number = int(input("Enter the task number to remove: "))
                remove_task(task_number)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            print("Exiting the app!")
            break
        else:
            print("Invalid choice. Please try again!")

if __name__ == "__main__":
    main()
