"""
Script for testing the codebase on linting with a threshold
"""

import sys
from pylint import lint

from core.helpers import bcolors

THRESHOLD = 9

if len(sys.argv) < 2:
    raise Exception("Module to evaluate needs to be the first argument") # pylint: disable=broad-exception-raised

run = lint.Run([sys.argv[1]], do_exit=False)
score = round(run.linter.stats.global_note, 2)

if score <= THRESHOLD:
    print(f"Linter score is too low: {bcolors.FAIL}{bcolors.BOLD}{score}{bcolors.ENDC}")
    sys.exit(1)

else:
    print(f"{bcolors.OKGREEN}Linting approved!{bcolors.ENDC}")
