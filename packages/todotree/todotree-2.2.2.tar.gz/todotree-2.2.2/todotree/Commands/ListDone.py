from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.DoneFileNotFound import DoneFileNotFound


class ListDone(AbstractCommand):
    def run(self):
        try:
            self.taskManager.list_done()
        except DoneFileNotFound as e:
            e.echo_and_exit(self.config)
