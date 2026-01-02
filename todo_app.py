#!/usr/bin/env python3
"""
Python Console Todo Application

A command-line interface application that allows users to manage their tasks.
Features include adding, deleting, updating, viewing, and marking tasks as complete.
All data is stored in-memory only and resets when the application exits.
"""

import sys
from datetime import datetime
from typing import List, Optional


class Task:
    """
    Represents a single task in the todo list.
    """
    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"ID: {self.id} | Title: {self.title} | Description: {self.description or 'N/A'} | Status: {status}"

    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True

    def mark_pending(self):
        """Mark the task as pending."""
        self.completed = False

    def update_task(self, title: str = None, description: str = None):
        """Update the task title and/or description."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description


class TodoApp:
    """
    Main application class for managing todo tasks.
    """
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1
        self.running = True

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("           PYTHON TODO APPLICATION")
        print("="*50)
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View Tasks")
        print("5. Mark Task Complete")
        print("6. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """Get and validate user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-6): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6']:
                    return choice
                else:
                    print("Error: Please enter a number between 1 and 6.")
            except (EOFError, KeyboardInterrupt):
                print("\n\nReceived interrupt. Exiting application...")
                sys.exit(0)

    def add_task(self):
        """Add a new task to the list."""
        print("\n--- ADD TASK ---")
        title = input("Enter task title: ").strip()
        
        if not title:
            print("Error: Task title cannot be empty.")
            return
        
        description = input("Enter task description (optional, press Enter to skip): ").strip()
        
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        print(f"Task added successfully! Task ID: {self.next_id}")
        self.next_id += 1

    def delete_task(self):
        """Delete a task by its ID."""
        print("\n--- DELETE TASK ---")
        if not self.tasks:
            print("No tasks available to delete.")
            return
        
        self.view_tasks()
        
        try:
            task_id = int(input("Enter the ID of the task to delete: "))
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return
        
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            print(f"Task with ID {task_id} has been deleted.")
            # Update IDs of remaining tasks
            for i, t in enumerate(self.tasks, start=1):
                t.id = i
            self.next_id = len(self.tasks) + 1
        else:
            print(f"Error: Task with ID {task_id} does not exist.")

    def update_task(self):
        """Update a task by its ID."""
        print("\n--- UPDATE TASK ---")
        if not self.tasks:
            print("No tasks available to update.")
            return
        
        self.view_tasks()
        
        try:
            task_id = int(input("Enter the ID of the task to update: "))
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return
        
        task = self.find_task_by_id(task_id)
        if task:
            print(f"Current task: {task}")
            new_title = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
            new_description = input(f"Enter new description (current: '{task.description}', press Enter to keep current): ").strip()
            
            # Use current values if user doesn't provide new ones
            updated_title = new_title if new_title else task.title
            updated_description = new_description if new_description else task.description
            
            task.update_task(updated_title, updated_description)
            print(f"Task with ID {task_id} has been updated.")
        else:
            print(f"Error: Task with ID {task_id} does not exist.")

    def view_tasks(self):
        """View all tasks in the list."""
        print("\n--- VIEW TASKS ---")
        if not self.tasks:
            print("No tasks in the list.")
            return
        
        print("\nAll Tasks:")
        print("-" * 80)
        for task in self.tasks:
            print(task)
        print("-" * 80)
        print(f"Total tasks: {len(self.tasks)}")

    def mark_task_complete(self):
        """Mark a task as complete or pending by its ID."""
        print("\n--- MARK TASK COMPLETE ---")
        if not self.tasks:
            print("No tasks available to mark.")
            return
        
        self.view_tasks()
        
        try:
            task_id = int(input("Enter the ID of the task to mark: "))
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return
        
        task = self.find_task_by_id(task_id)
        if task:
            if task.completed:
                task.mark_pending()
                print(f"Task with ID {task_id} has been marked as Pending.")
            else:
                task.mark_complete()
                print(f"Task with ID {task_id} has been marked as Completed.")
        else:
            print(f"Error: Task with ID {task_id} does not exist.")

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def exit_app(self):
        """Exit the application."""
        print("\nThank you for using the Python Todo Application. Goodbye!")
        self.running = False

    def run(self):
        """Main application loop."""
        print("Welcome to the Python Console Todo Application!")
        
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.delete_task()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.view_tasks()
            elif choice == '5':
                self.mark_task_complete()
            elif choice == '6':
                self.exit_app()
            
            # Pause to let user see the result before showing the menu again
            if self.running:  # Don't pause if we're exiting
                input("\nPress Enter to continue...")


if __name__ == '__main__':
    # Start the todo application
    app = TodoApp()
    app.run()