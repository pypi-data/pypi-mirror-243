from typing import Tuple, List

import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Errors.TodoFileNotFound import TodoFileNotFound


class Do(AbstractCommand):

    def run(self, task_numbers: List[Tuple]):
        # Convert to ints. Task numbers is a list of tuples. Each tuple contains one digit of the number.
        new_numbers: List[int] = []
        for task_tuple in task_numbers:
            new_number: str = ""
            for task_digit in task_tuple:
                new_number += task_digit
            new_numbers.append(int(new_number))
        # Write back to old value.
        task_numbers = new_numbers
        # Marking something as Done cannot be done with fancy imports
        # So we disable them.
        self.config.enable_project_folder = False
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)
        try:
            completed_tasks = self.taskManager.mark_as_done(task_numbers)
        except DoneFileNotFound as e:
            e.echo_and_exit(self.config)
            exit(1)  # For IDE hinting.
        # Print the results
        self.config.console.info("Tasks marked as done:")
        for task in completed_tasks:
            click.echo(task)
        self.config.git.commit_and_push("do")
