from abc import ABC

from todotree.Config.Config import Config
from todotree.Taskmanager import Taskmanager


class AbstractCommand(ABC):

    def __init__(self, config: Config, task_manager: Taskmanager):
        """
        Initializes a new AbstractCommand.
        :param config: The configuration of the application.
        :param task_manager: The task manager.
        """
        self.taskManager = task_manager
        self.config = config

