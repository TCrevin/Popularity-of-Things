# Copied from:
# https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
# Using to prevent unnecessary prints in installed libraries when needed.
import os, sys


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
