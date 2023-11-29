import click

from todotree.Commands.AbstractCommand import AbstractCommand


class Edit(AbstractCommand):
    def run(self):
        # Disable fancy imports.
        self.config.enable_project_folder = False
        click.edit(filename=str(self.config.paths.todo_file))
        self.config.git.commit_and_push("edit")
