#!/usr/bin/env python3
"""
Python CLI Todo Application

A command-line interface application that allows users to manage their tasks.
Features include adding, deleting, updating, viewing, and marking tasks as complete.
All data is stored in-memory only and resets when the application exits.
"""

import cmd
import sys
import signal
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """
    Represents a single task in the todo list.
    """
    def __init__(self, task_id: int, title: str, completed: bool = False):
        self.id = task_id
        self.title = title
        self.completed = completed
        self.created_at = datetime.now()

    def __str__(self):
        status = "X" if self.completed else "O"
        return f"[{status}] [{self.id}] {self.title}"

    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True

    def update_title(self, new_title: str):
        """Update the task title."""
        self.title = new_title


class TodoApp(cmd.Cmd):
    """
    Main CLI application for managing todo tasks.
    Inherits from cmd.Cmd to provide a command-line interface.
    """
    
    intro = 'Welcome to the Python CLI Todo App! Type help or ? to list commands.\n'
    prompt = '(todo) '
    
    def __init__(self):
        super().__init__()
        self.tasks: List[Task] = []
        self.next_id = 1
        self.history: List[str] = []
        
        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C interruption."""
        print("\nReceived interrupt signal. Use 'exit' command to quit safely.")
    
    def _add_to_history(self, command: str):
        """Add command to history."""
        self.history.append(f"{datetime.now().strftime('%H:%M:%S')} - {command}")
    
    def _validate_task_id(self, task_id: str) -> Optional[int]:
        """Validate that the task ID is a valid integer."""
        try:
            task_num = int(task_id)
            if task_num <= 0:
                print(f"Error: Task ID must be a positive integer")
                return None
            if task_num > len(self.tasks) or task_num < 1:
                print(f"Error: Task with ID {task_num} does not exist")
                return None
            return task_num
        except ValueError:
            print(f"Error: '{task_id}' is not a valid task ID")
            return None
    
    def do_add(self, arg: str):
        """
        Add a new task to the list.
        
        Usage: add <task_title>
        Example: add Buy groceries
        """
        if not arg.strip():
            print("Error: Task title cannot be empty")
            return
        
        if len(arg.strip()) < 1:
            print("Error: Task title must be at least 1 character long")
            return
        
        task = Task(self.next_id, arg.strip())
        self.tasks.append(task)
        print(f"Added task: {task}")
        self.next_id += 1
        self._add_to_history(f"add {arg}")
    
    def help_add(self):
        """Help for the add command."""
        print("Usage: add <task_title>")
        print("Add a new task to the list.")
        print("Example: add Buy groceries")
    
    def do_delete(self, arg: str):
        """
        Delete a task by its ID.
        
        Usage: delete <task_id>
        Example: delete 1
        """
        if not arg:
            print("Error: Please specify a task ID to delete")
            return
        
        task_num = self._validate_task_id(arg)
        if task_num is None:
            return
        
        # Find the task with the given ID
        task_to_delete = None
        for i, task in enumerate(self.tasks):
            if task.id == task_num:
                task_to_delete = i
                break
        
        if task_to_delete is not None:
            deleted_task = self.tasks.pop(task_to_delete)
            # Update IDs of remaining tasks
            for i, task in enumerate(self.tasks):
                if task.id > deleted_task.id:
                    task.id = i + 1
            self.next_id -= 1
            print(f"Deleted task: {deleted_task}")
            self._add_to_history(f"delete {arg}")
        else:
            print(f"Error: Task with ID {task_num} does not exist")
    
    def help_delete(self):
        """Help for the delete command."""
        print("Usage: delete <task_id>")
        print("Delete a task by its ID.")
        print("Example: delete 1")
    
    def do_update(self, arg: str):
        """
        Update a task title by its ID.
        
        Usage: update <task_id> <new_title>
        Example: update 1 Buy groceries and cook dinner
        """
        if not arg:
            print("Error: Please specify a task ID and new title")
            return
        
        parts = arg.split(maxsplit=1)
        if len(parts) != 2:
            print("Error: Please specify both a task ID and new title")
            print("Usage: update <task_id> <new_title>")
            return
        
        task_id, new_title = parts
        if not new_title.strip():
            print("Error: New title cannot be empty")
            return
        
        task_num = self._validate_task_id(task_id)
        if task_num is None:
            return
        
        # Find and update the task
        for task in self.tasks:
            if task.id == task_num:
                old_title = task.title
                task.update_title(new_title.strip())
                print(f"Updated task {task_num}: '{old_title}' -> '{task.title}'")
                self._add_to_history(f"update {task_id} {new_title}")
                return
        
        print(f"Error: Task with ID {task_num} does not exist")
    
    def help_update(self):
        """Help for the update command."""
        print("Usage: update <task_id> <new_title>")
        print("Update a task title by its ID.")
        print("Example: update 1 Buy groceries and cook dinner")
    
    def do_view(self, arg: str):
        """
        View all tasks in the list.
        
        Usage: view
        """
        if not self.tasks:
            print("No tasks in the list.")
        else:
            print("Current tasks:")
            for task in self.tasks:
                print(f"  {task}")
        self._add_to_history("view")
    
    def help_view(self):
        """Help for the view command."""
        print("Usage: view")
        print("View all tasks in the list.")
    
    def do_complete(self, arg: str):
        """
        Mark a task as complete by its ID.
        
        Usage: complete <task_id>
        Example: complete 1
        """
        if not arg:
            print("Error: Please specify a task ID to mark as complete")
            return
        
        task_num = self._validate_task_id(arg)
        if task_num is None:
            return
        
        for task in self.tasks:
            if task.id == task_num:
                if task.completed:
                    print(f"Task {task_num} is already marked as complete")
                else:
                    task.mark_complete()
                    print(f"Marked task {task_num} as complete: {task}")
                self._add_to_history(f"complete {arg}")
                return
        
        print(f"Error: Task with ID {task_num} does not exist")
    
    def help_complete(self):
        """Help for the complete command."""
        print("Usage: complete <task_id>")
        print("Mark a task as complete by its ID.")
        print("Example: complete 1")
    
    def do_history(self, arg: str):
        """
        Show command history.
        
        Usage: history
        """
        if not self.history:
            print("No command history available.")
        else:
            print("Command history:")
            for entry in self.history:
                print(f"  {entry}")
    
    def help_history(self):
        """Help for the history command."""
        print("Usage: history")
        print("Show command history.")
    
    def do_exit(self, arg: str):
        """
        Exit the application.
        
        Usage: exit
        """
        print("Thank you for using the Python CLI Todo App. Goodbye!")
        return True  # Returning True exits the cmd loop
    
    def help_exit(self):
        """Help for the exit command."""
        print("Usage: exit")
        print("Exit the application.")
    
    def do_EOF(self, arg: str):
        """
        Handle EOF (Ctrl+D) to exit the application.
        """
        print("\nReceived EOF. Exiting...")
        return True
    
    def help_EOF(self):
        """Help for the EOF command."""
        print("Usage: Ctrl+D (EOF)")
        print("Exit the application.")
    
    def default(self, line: str):
        """
        Handle unknown commands.
        """
        print(f"Unknown command: {line}")
        print("Type 'help' or '?' for a list of available commands.")
    
    def emptyline(self):
        """
        Handle empty input lines.
        """
        print("Error: Please enter a command")
        return False


if __name__ == '__main__':
    # Start the todo application
    TodoApp().cmdloop()