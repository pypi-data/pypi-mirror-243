import datetime
import math
import os
import pathlib
import shutil
from tempfile import (  # https://docs.python.org/3/library/tempfile.html
    NamedTemporaryFile,
)
from typing import Callable

from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Errors.ProjectFolderError import ProjectFolderError
from todotree.Task.ConsoleTask import ConsoleTask
from todotree.Task.Task import Task
from todotree.Tree import Tree
from todotree.Config.Config import Config
from todotree.Task.DoneTask import DoneTask


class Taskmanager:
    """Manages the tasks."""

    @property
    def number_of_digits(self) -> int:
        """Property which defines the number of digits of the task in the task list with the highest number."""
        maxi = max([x.i for x in self.task_list])
        return int(math.ceil(math.log(maxi + 1, 10)))

    def __init__(self, configuration: Config):
        """Initializes a task manager, which manages the tasks."""

        self.task_list: list[Task] = []
        """List Without empty lines"""

        self.config: Config = configuration
        """Configuration settings for the application."""

    # Imports

    def import_tasks(self):
        """
        Import the tasks and projects from files.
        """
        self._import_from_todo_txt()
        if self.config.enable_project_folder:
            self._import_project_folder()

    def _import_from_todo_txt(self):
        """
        Imports the todos from the file to the Taskmanager object.
        """
        try:
            with self.config.paths.todo_file.open('r') as f:
                content = f.readlines()
                self.task_list = []
                for i, task in enumerate(content):
                    # Skip empty lines.
                    if task.strip() == "":
                        continue
                    self.task_list.append(Task(i + 1, task.strip()))
        except FileNotFoundError as e:
            raise TodoFileNotFound("Todo not found.") from e

    def filter_t_date(self):
        """Removes Tasks from the Taskmanager where the t:date is later than today."""
        self.task_list = [t for t in self.task_list if t.t_date is None or t.t_date <= datetime.date.today()]

    def filter_block(self):
        """
        Removes Tasks from the Taskmanager where the task is blocked by some other task.
        """
        # Detect all block items.
        block_list_items = [y for x in self.task_list for y in x.blocks]
        # Blocked / Blocked by filtering
        for task in self.task_list.copy():
            # Check if there is a task which is blocked by another task.
            if any(filter(lambda x: x in block_list_items, task.blocked)):
                self.task_list.remove(task)

    def _import_project_folder(self):
        """
        Adds the directory to the project tree.
        """
        try:
            for i in pathlib.Path(self.config.paths.project_tree_folder).glob("*/"):
                proj = os.path.basename(i)
                # Check if there is a task with that project.
                if not any(proj in x.projects for x in self.task_list):
                    tmp_task = Task(-1, self.config.emptyProjectString)
                    tmp_task.projects = [proj]
                    self.task_list.append(tmp_task)
        except FileNotFoundError as e:
            raise ProjectFolderError(f"An error occurred while processing the projects folder: {e}")

    def list_done(self):
        """
        List the done.txt with numbers to revive them.
        """
        try:
            with self.config.paths.done_file.open(mode="r") as f:
                lines = f.readlines()
        except FileNotFoundError as e:
            raise DoneFileNotFound from e
        for i, line in reversed(list(enumerate(lines))):
            print(i, line, end="")

    def print_tree(self, key):
        """Prints a tree representation of the task list.
        :key: The key of the task used for the first line."""
        self.filter_t_date()
        self.filter_block()
        tasks = [ConsoleTask(task.i, task.task_string, total_digits=self.number_of_digits) for task in self.task_list]

        print_function: Callable[[str, ConsoleTask], str]
        match key:
            case "projects":
                def print_function(project_to_exclude, task):
                    return task.print_project(project_to_exclude)
                root_name = "Projects"
                empty_string = self.config.noProjectString
            case "contexts":
                def print_function(context_to_exclude, task):
                    return task.print_context(context_to_exclude)
                root_name = "Contexts"
                empty_string = self.config.noContextString
            case "due":
                def print_function(_, task):
                    return task.print_due()
                root_name = "Due Dates"
                key = "due_date_band"
                empty_string = "default"
            case _:
                raise NotImplementedError(key)
        return str(Tree(tasks, key, treeprint=self.config.tree_print,
                        print_func=print_function, root_name=root_name, empty_string=empty_string))

    def write_todo_to_file(self):
        """
        Write the entire todo.txt file.
        """
        # Write to new file.
        self.task_list.sort(key=lambda x: x.i)
        #  Delete=false is needed for windows, I hope that somebodies temp folder won't be clobbered with this...
        try:
            with NamedTemporaryFile("w+t", newline="", delete=False) as temp_file:
                # may strip new lines by using task list.
                for n in self.task_list:
                    temp_file.write(str(n.task_string))
                    temp_file.write("\n")
                temp_file.flush()
                shutil.copy(temp_file.name, self.config.paths.todo_file)
        except FileNotFoundError as e:
            raise TodoFileNotFound from e

    def add_or_update_task(self, task_number, func: Callable, *args, **kwargs):
        """
        Runs `func` on the task with `task_number`.
        :param task_number: The task number.
        :param func: The Task function.
        :param args: passed to func.
        :param kwargs: passed to func.
        :return: The updated task.
        """
        func(self.task_list[task_number - 1], *args, **kwargs)
        self.write_todo_to_file()
        return self.task_list[task_number - 1]

    def add_tasks_to_file(self, tasks: list[str]) -> (int, list[Task]):
        """Append multiple tasks to the todotxt file."""
        return_list = []
        try:
            with self.config.paths.todo_file.open(mode="a") as f:
                for i, task in enumerate(tasks):
                    f.write(task)
                    return_list.append(Task(len(self.task_list) + 1 + i, task))
        except FileNotFoundError as e:
            raise TodoFileNotFound from e
        return (len(self.task_list) + 1), return_list

    def append_to_task(self, task_number: int, task_string: str) -> str:
        """
        Appends `task_string` to the task defined by `task_number`.
        :param task_string: The string to append
        :param task_number: The number of the existing task.
        :return: The new merged task.
        """
        self.task_list[task_number - 1] = self.task_list[task_number - 1] + task_string
        self.write_todo_to_file()
        return self.task_list[task_number - 1].task_string

    def mark_as_done(self, line_numbers):
        """
        Marks the task as done, removes it from the task file and adds it to done.txt
        :param line_numbers: The task numbers to mark as done.
        :return: The tasks marked as done.
        """
        # Get and remove completed task
        completed_tasks = []
        line_numbers.sort()
        # Delete the tasks from the end to the start.
        line_numbers.reverse()
        for num in line_numbers:
            completed_tasks.append(self.task_list[num - 1])
            del self.task_list[num - 1]
        # Save the new task list.
        self.write_todo_to_file()
        # Convert completed tasks to done tasks.
        done_tasks = [DoneTask.task_to_done(x) for x in completed_tasks]
        # Append the results to done.txt
        try:
            with self.config.paths.done_file.open(mode="a") as f:
                for completed_task in done_tasks:
                    f.write(completed_task + "\n")
        except FileNotFoundError as e:
            raise DoneFileNotFound from e
        return done_tasks

    def revive_task(self, line_number):
        """
        Gets task from done.txt and adds it to the task file.
        The task does not get removed from the done file..
        :param line_number: The done number to revive.
        :return: The revived task.
        """
        # Fetch Task
        try:
            with self.config.paths.done_file.open() as f:
                done_tasks = f.readlines()
                print(done_tasks, line_number)
        except FileNotFoundError as e:
            raise DoneFileNotFound from e
        # Add task.
        new_task = DoneTask.task_to_undone(done_tasks[line_number - 1])
        new_task_number = self.add_tasks_to_file([new_task])
        return ConsoleTask(new_task_number, new_task)

    def __str__(self, filter_string=None):
        """
        Filters the task list by whether `filter_string` occurred in the task.
        """
        # Prepare the lists.
        self.filter_t_date()
        self.filter_block()
        if filter_string:
            self.task_list = [item for item in self.task_list if filter_string in item.task_string]
        self.task_list.sort(key=lambda x: x.priority)
        # Output the list.
        s = ""
        for tsk in [ConsoleTask(task.i, task.task_string, self.number_of_digits) for task in self.task_list]:
            s += str(tsk) + "\n"
        return s
