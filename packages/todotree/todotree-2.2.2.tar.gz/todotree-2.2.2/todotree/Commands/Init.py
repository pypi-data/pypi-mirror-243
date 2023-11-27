from pathlib import Path

import click
import xdg_base_dirs

from todotree.Config.Config import Config
from todotree.Config.ConsolePrefixesInit import ConsolePrefixesInit
from todotree.Errors.GitError import GitError


class Init:
    # Note: Does not inherit AbstractCommand!

    def __init__(self):
        self.config: Config = Config()
        """Configuration."""
        self.action_queue: list[Path] = [Path("config.yaml")]
        """List of actions to execute."""
        self.homework: list[str] = []
        """List of actions the user has to do after todotree init writes the files."""
        self.console: ConsolePrefixesInit = ConsolePrefixesInit.from_console_prefixes(self.config.console)

    def run(self):
        self.intro()
        is_git_cloned = False  # self.git_clone()
        if not is_git_cloned:
            self.determine_console_prefixes()
            self.determine_config_location()
            self.determine_folder_location()
            self.enable_git()
            self.enable_project()
            self.example_todo()
        # Write results of the answers to the locations.
        self.console.warning("The content of config.yaml is generated.")
        self.console.warning("Todotree will overwrite the following files, destroying any existing content in the files.")
        self.console.warning(", ".join([str(x.resolve()) for x in self.action_queue]))
        answer = self.console.confirm("Are you *sure* you want to continue?")
        if answer:
            self.config.write_config()
            if self.config.paths.todo_file in self.action_queue:
                self.write_example_todo()
        else:
            self.console.error("Aborted the initialization, please run `todotree init` again.")
        # Homework section.
        self.console.info("Written the files.")
        if self.homework:
            self.console.info("The following things need to be configured yet.")
        for task in self.homework:
            self.console.info(task)

    def intro(self):
        self.console.info("This will configure todotree and generate the necessary files to run it.")
        self.console.info("If at any point you wish to stop, you can do so with Ctrl-C.")
        self.console.info("Also, all options can be changed afterwards in the config.yaml if you change your mind.")

    def determine_config_location(self):
        question = "Where do you want to store config.yaml?"
        answers = [
            Path(xdg_base_dirs.xdg_config_home() / "todotree" / "config.yaml"),
            Path(xdg_base_dirs.xdg_data_home() / "todotree" / "config.yaml"),
        ]
        answer = self.console.prompt_menu(question, answers,
                                          "Custom location (Note: you'll need to supply it each time "
                                          "with the --config-file option).")
        if isinstance(answer, int):
            self.config.config_file = answers[answer]
        else:
            self.config.config_file = Path(answer)
            self.console.warning(
                "Note: You need to supply todotree each time with the config location using --config-file"
            )
            self.console.warning("It is advised to alias this in your profile for example in ~/.profile or $PROFILE.")
            self.homework.append("Custom config file: Configure $PROFILE or ~/.profile have --config-file.")
        self.console.info(f"Set the config location to {self.config.config_file}")

    def determine_console_prefixes(self):
        self.console.enable_colors = self.console.confirm(text="Do you want colors on your console?")
        self.config.console.enable_colors = self.console.enable_colors
        question = "How do you want the decorations?"
        answer: int = -1
        if self.console.enable_colors:
            confirmed = False
            while not confirmed:
                answer, confirmed = self.__prompt_prefix_colors(question)
        else:
            answers = [
                (f"Default      | {self.console.info_prefix} | {self.console.warning_prefix} |"
                    f" {self.console.error_prefix} |"),
                "Gentoo Style |  *  |  *  |  *  |",
            ]
            answer = int(self.console.prompt_menu(question, answers))
        if answer == 1:
            # Then we set gentoo style in both current shell and config.
            (self.console.info_prefix, self.console.warning_prefix, self.console.error_prefix,
             self.config.console.info_prefix, self.config.console.warning_prefix, self.config.console.error_prefix) \
                = [" * "] * 6

    def __prompt_prefix_colors(self, question):
        """Displays the options in color as well."""
        self.console.warning(question)

        def first():
            click.secho("[0]", fg=self.console.info_color, nl=False)
            click.echo(" Default      | ", nl=False)
            click.secho(self.console.info_prefix, fg=self.console.info_color, nl=False)
            click.echo(" | ", nl=False)
            click.secho(self.console.warning_prefix, fg=self.console.warn_color, nl=False)
            click.echo(" | ", nl=False)
            click.secho(self.console.error_prefix, fg=self.console.error_color)

        def second():
            click.secho("[1]", fg=self.console.info_color, nl=False)
            click.echo(" Gentoo Style | ", nl=False)
            click.secho(" * ", fg=self.console.info_color, nl=False)
            click.echo(" | ", nl=False)
            click.secho(" * ", fg=self.console.warn_color, nl=False)
            click.echo(" | ", nl=False)
            click.secho(" * ", fg=self.console.error_color)

        first()
        second()
        # Ask the question.
        answer = int(self.console.prompt(text="Your Answer", type=click.Choice(["0", "1"])))
        first() if answer == 0 else second()
        confirmed = self.console.confirm(text=f"Is above correct?")
        return answer, confirmed

    def determine_folder_location(self):
        question = "Where do you want to store the other files?"
        answers = [
            Path(xdg_base_dirs.xdg_config_home() / "todotree"),
            Path(xdg_base_dirs.xdg_data_home() / "todotree"),
        ]
        answer = self.console.prompt_menu(question, answers, custom_answer="Custom folder location.")
        if isinstance(answer, int):
            self.config.paths.todo_folder = answers[answer]
        else:
            self.config.paths.todo_folder = Path(answer).resolve()
        self.console.info(f"Set the folder location to {self.config.paths.todo_folder}")

    def enable_git(self):
        enable_git = self.console.confirm(text="Do you want to enable git?")
        if not enable_git:
            git_mode = "disabled"
        else:
            enable_remote = self.console.confirm(text="Do you want to work with a remote repo as well?")
            git_mode = "full" if enable_remote else "local"
            if git_mode == "full":
                self.config.console.warning("You will need to configure the remote repo later.")
                self.homework.append("Configure remote git repo.")
        try:
            self.config.git.git_mode = git_mode
        except GitError as e:
            self.console.error("Setting git raised an error, you'll need to fix this later. The error is:")
            self.console.error(str(e))
            self.homework.append("Configure git itself.")

    def example_todo(self):
        if self.console.confirm("Do you want to have your todo file filled with some examples?"):
            self.action_queue.append(self.config.paths.todo_file)

    def write_example_todo(self):
        """Write the example task file to the configured location."""
        from importlib import resources as import_resources
        from .. import examples
        example_todo_path = import_resources.files(examples) / "todo.txt"

        example_contents = example_todo_path.read_text()
        self.config.paths.todo_file.parent.mkdir(parents=True, exist_ok=True)
        self.config.paths.todo_file.write_text(example_contents)

    def enable_project(self):
        self.console.info("The project_directory functionality adds the projects in a given folder.")
        self.console.info("It will also add tasks if there is no task with the given project name in todo.txt,")
        self.console.info("reminding you that that project is stalled.")
        self.config.enable_project_folder = self.console.confirm(
            "Do you want to enable the project_directory functionality?"
        )
        confirmed = False
        while not confirmed:
            if self.config.enable_project_folder:
                answer = self.console.prompt(
                   "What will the location of your projects be?", default=self.config.paths.project_tree_folder
                )
                self.config.project_tree_folder = Path(answer).resolve()
            if not Path(self.config.paths.todo_folder).exists():
                self.console.warning("Project folder does not exist yet.")
            confirmed = self.console.confirm("Is the project directory correct?")
        if not Path(self.config.paths.todo_folder).exists():
            self.homework.append(f"Create a project folder at {self.config.project_tree_folder} and add projects.")

    def git_clone(self):
        answer = self.console.confirm("Do you already have an existing todotree folder on git?")
        if answer:
            self.console.prompt("Please enter the git clone url to clone from.")
            # FUTURE: implement git clone.
        return answer
