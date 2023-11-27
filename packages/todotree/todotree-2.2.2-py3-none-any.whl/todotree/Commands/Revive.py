import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Errors.TodoFileNotFound import TodoFileNotFound


class Revive(AbstractCommand):
    def run(self, done_number: int):
        try:
            click.echo(self.taskManager.revive_task(done_number))
        except TodoFileNotFound as e:
            e.echo_and_exit(self.config)
        except DoneFileNotFound as e:
            e.echo_and_exit(self.config)
        self.config.git.commit_and_push("revive")
