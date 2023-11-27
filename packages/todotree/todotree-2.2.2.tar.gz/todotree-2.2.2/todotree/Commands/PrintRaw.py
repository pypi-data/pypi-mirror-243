import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFound import TodoFileNotFound


class PrintRaw(AbstractCommand):

    def run(self):
        try:
            click.echo(self.taskManager.config.paths.todo_file.read_text())
        except FileNotFoundError:
            TodoFileNotFound("").echo_and_exit(self.config)
