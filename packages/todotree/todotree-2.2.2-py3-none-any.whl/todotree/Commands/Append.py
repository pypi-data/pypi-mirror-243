from typing import Tuple

import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFound import TodoFileNotFound


class Append(AbstractCommand):
    def run(self, task_nr: int, append_string: Tuple[str]):
        # Disable fancy imports, because they are not needed.
        self.config.enable_project_folder = False
        # Import tasks.
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)
        # Convert tuple to string.
        append_string = " ".join(append_string)
        # Append task.
        self.config.console.info("The new task is: ")
        click.echo(self.taskManager.append_to_task(task_nr, append_string.strip()))
        self.config.git.commit_and_push("append")
