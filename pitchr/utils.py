from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull
import shutil
from pitchr import *


LILYPOND = "lilypond"
LILYPOND_MISSING_ERROR = "Error. You need lilypond in your PATH to export."

@contextmanager
def _suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


def _verify_lilypond_in_path():
    if shutil.which(LILYPOND) is None:
        raise PitcherException(LILYPOND_MISSING_ERROR)
