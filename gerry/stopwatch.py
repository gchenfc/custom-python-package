from time import perf_counter
from typing import Optional


class Stopwatch:
    def __init__(self,
                 name: Optional[str] = None,
                 msg: Optional[str] = None,
                 print: Optional[bool] = None,
                 print_start_and_end: bool = False):
        """Creates a new Stopwatch object.

        Args:
            name: The name of the stopwatch (used in msg). (Default: None, aka "Took 1.234s")
            msg: The message to print when the stopwatch is done (Default: "[name] took 1.234s")
            print: Whether to print the message when the stopwatch is done (Default: True, unless msg and name are both None)
            print_start_and_end: If True, prints "Starting {name}... Finished in 1.234s" (Default: False)
        """
        if print is None:
            print = (msg is not None) or (name is not None)
        if msg is None:
            if name is not None:
                msg = '{name} took {:.3f}s'
            else:
                msg = 'Took {:.3f}s'
        if print_start_and_end:
            msg = 'Finished {name} in {:.3f}s'
        self.name = name
        self.msg = msg
        self.print = print
        self.print_start_and_end = print_start_and_end

    def __enter__(self):
        if self.print_start_and_end:
            print(f'Starting {self.name}...', end=' ⏳ ')
        self.start = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.start
        if self.print:
            print(self)

    def __repr__(self):
        return self.msg.format(self.time, name=self.name)

    def __float__(self):
        return self.time
