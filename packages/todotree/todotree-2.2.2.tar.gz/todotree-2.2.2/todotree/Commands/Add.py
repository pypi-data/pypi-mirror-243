from typing import Tuple

import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFound import TodoFileNotFound


class Add(AbstractCommand):

    def run(self, task: Tuple):
        # Convert tuple to string
        task: str = " ".join(map(str, task))
        try:
            # Disable fancy imports, because they are not needed.
            self.config.enable_project_folder = False
            # Import tasks.
            self.taskManager.import_tasks()
            # Add task
            new_number = self.taskManager.add_tasks_to_file([task.strip() + "\n"])
            self.config.console.info("Task added:")
            click.echo(f"{new_number} {task}")
            self.config.git.commit_and_push("add")
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)
