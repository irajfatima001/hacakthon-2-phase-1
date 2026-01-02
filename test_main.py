#!/usr/bin/env python3
"""
Unit tests for the Python CLI Todo Application.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the main module to the path so we can import it
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import TodoApp, Task


class TestTask(unittest.TestCase):
    """Test cases for the Task class."""
    
    def test_task_initialization(self):
        """Test that a task is initialized correctly."""
        task = Task(1, "Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertFalse(task.completed)
    
    def test_task_completion(self):
        """Test marking a task as complete."""
        task = Task(1, "Test task")
        self.assertFalse(task.completed)
        task.mark_complete()
        self.assertTrue(task.completed)
    
    def test_task_update_title(self):
        """Test updating a task's title."""
        task = Task(1, "Old title")
        task.update_title("New title")
        self.assertEqual(task.title, "New title")
    
    def test_task_string_representation(self):
        """Test the string representation of a task."""
        task = Task(1, "Test task")
        self.assertEqual(str(task), "[O] [1] Test task")

        task.mark_complete()
        self.assertEqual(str(task), "[X] [1] Test task")


class TestTodoApp(unittest.TestCase):
    """Test cases for the TodoApp class."""
    
    def setUp(self):
        """Set up a fresh TodoApp instance for each test."""
        self.app = TodoApp()
    
    def test_add_task(self):
        """Test adding a task."""
        self.app.do_add("Buy groceries")
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0].title, "Buy groceries")
        self.assertEqual(self.app.tasks[0].id, 1)
    
    def test_add_empty_task(self):
        """Test adding an empty task (should fail)."""
        # Capture print output
        with patch('builtins.print') as mock_print:
            self.app.do_add("")
            mock_print.assert_called_with("Error: Task title cannot be empty")
    
    def test_delete_task(self):
        """Test deleting a task."""
        self.app.do_add("Task 1")
        self.app.do_add("Task 2")
        initial_count = len(self.app.tasks)
        
        # Delete the first task
        with patch('builtins.print'):
            self.app.do_delete("1")
        
        self.assertEqual(len(self.app.tasks), initial_count - 1)
        self.assertEqual(self.app.tasks[0].title, "Task 2")
        self.assertEqual(self.app.tasks[0].id, 1)  # ID should be updated
    
    def test_delete_invalid_task_id(self):
        """Test deleting a task with an invalid ID."""
        self.app.do_add("Task 1")
        
        with patch('builtins.print') as mock_print:
            self.app.do_delete("5")
            # Check that an error message was printed
            error_calls = [call for call in mock_print.call_args_list 
                          if 'does not exist' in str(call)]
            self.assertTrue(len(error_calls) > 0)
    
    def test_update_task(self):
        """Test updating a task."""
        self.app.do_add("Old task")
        
        with patch('builtins.print'):
            self.app.do_update("1 New task title")
        
        self.assertEqual(self.app.tasks[0].title, "New task title")
    
    def test_update_invalid_task_id(self):
        """Test updating a task with an invalid ID."""
        self.app.do_add("Task 1")
        
        with patch('builtins.print') as mock_print:
            self.app.do_update("5 New title")
            # Check that an error message was printed
            error_calls = [call for call in mock_print.call_args_list 
                          if 'does not exist' in str(call)]
            self.assertTrue(len(error_calls) > 0)
    
    def test_complete_task(self):
        """Test marking a task as complete."""
        self.app.do_add("Task 1")
        self.assertFalse(self.app.tasks[0].completed)
        
        with patch('builtins.print'):
            self.app.do_complete("1")
        
        self.assertTrue(self.app.tasks[0].completed)
    
    def test_complete_already_completed_task(self):
        """Test marking an already completed task."""
        self.app.do_add("Task 1")
        self.app.do_complete("1")  # Mark as complete
        
        with patch('builtins.print') as mock_print:
            self.app.do_complete("1")  # Try to mark again
            # Should print that it's already complete
            already_complete_calls = [call for call in mock_print.call_args_list 
                                    if 'already marked as complete' in str(call)]
            self.assertTrue(len(already_complete_calls) > 0)
    
    def test_view_tasks(self):
        """Test viewing tasks."""
        self.app.do_add("Task 1")
        self.app.do_add("Task 2")
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            self.app.do_view("")
            # Check that the tasks were printed
            calls = [str(call) for call in mock_print.call_args_list]
            task_calls = [call for call in calls if 'Task 1' in call or 'Task 2' in call]
            self.assertEqual(len(task_calls), 2)
    
    def test_empty_task_list(self):
        """Test viewing an empty task list."""
        with patch('builtins.print') as mock_print:
            self.app.do_view("")
            # Should print "No tasks in the list."
            no_tasks_calls = [call for call in mock_print.call_args_list 
                            if 'No tasks in the list.' in str(call)]
            self.assertTrue(len(no_tasks_calls) > 0)
    
    def test_history_command(self):
        """Test the history command."""
        self.app.do_add("Test task")
        self.app.do_view("")
        
        with patch('builtins.print') as mock_print:
            self.app.do_history("")
            # Should print history
            history_calls = [call for call in mock_print.call_args_list 
                           if 'Command history:' in str(call)]
            self.assertTrue(len(history_calls) > 0)
    
    def test_exit_command(self):
        """Test the exit command."""
        # The do_exit method should return True to exit the cmd loop
        result = self.app.do_exit("")
        self.assertTrue(result)
    
    def test_EOF_command(self):
        """Test the EOF command."""
        # The do_EOF method should return True to exit the cmd loop
        result = self.app.do_EOF("")
        self.assertTrue(result)
    
    def test_invalid_command(self):
        """Test handling of invalid commands."""
        with patch('builtins.print') as mock_print:
            self.app.default("invalidcommand")
            # Should print unknown command message
            unknown_calls = [call for call in mock_print.call_args_list 
                           if 'Unknown command' in str(call)]
            self.assertTrue(len(unknown_calls) > 0)
    
    def test_empty_line(self):
        """Test handling of empty input."""
        with patch('builtins.print') as mock_print:
            result = self.app.emptyline()
            # Should print error message and return False
            error_calls = [call for call in mock_print.call_args_list 
                          if 'Please enter a command' in str(call)]
            self.assertTrue(len(error_calls) > 0)
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()