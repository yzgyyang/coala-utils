import glob
import os

# GNU readline is not available for Windows
try:
    import readline
except ImportError:  # pragma Linux: no cover
    import pyreadline as readline


def path_completer(text, state):
    """
    Completer method for system paths.
    """
    return [x if os.path.isfile(x) else (x + os.sep)
            for x in glob.glob(text + '*')][state]


class FilePathCompleter:
    """
    Provides tab completion for the filesystem paths.
    """

    def __init__(self,
                 delimiters=', \t\n\\',
                 bind_keys=['tab'],
                 completion_method=path_completer):
        """
        :param delimiters:
            String containing the delimiters for the user input.
        :bind_keys:
            list of keys that would trigger the completion.
        :completion_method:
            function to be used for suggesting values for completion
            based on the input text.
        """
        self.delimiters = delimiters
        self.bind_keys = bind_keys
        self.completion_method = completion_method

    def activate(self, seed_dir=os.getcwd()):
        """
        :param seed_dir:
            The initial directory path relative to which all the
            filepaths will be suggested and completed.
        """
        readline.set_completer_delims(self.delimiters)
        self.initial_dir = os.getcwd()
        os.chdir(seed_dir)
        for key in self.bind_keys:
            readline.parse_and_bind("{}: complete".format(key))
        readline.set_completer(self.completion_method)

    def deactivate(self):
        for key in self.bind_keys:
            readline.parse_and_bind("{}: self-insert".format(key))
        readline.set_completer()
        os.chdir(self.initial_dir)
