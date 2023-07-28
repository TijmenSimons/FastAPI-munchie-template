from datetime import datetime, timedelta
import logging
import threading
import time

from core.helpers import bcolors
from core.helpers.logger import get_logger


class BaseTask:
    """
    A base class for defining recurring tasks.

    ## Args:
        `session` (Session): The session used for querying the database.
        `name` (str, optional): The name of the task. Defaults to "Unnamed Task".

    ## Attributes:
        `name` (str): The name of the task.
        `_timer` (threading.Timer): The timer object used for scheduling task runs.
        `_running` (bool): A flag indicating whether the task is currently running.

    ## Methods:
        `start()`: Starts the task.
        `stop()`: Stops the task.
        `run()`: Runs the task.
        `exec()`: Placeholder method for defining task behavior.
        `countdown()`: Placeholder property method that returns the time interval between task runs in seconds.
    """

    def __init__(
        self, session, capture_exceptions: bool = True, name: str = "Unnamed Task"
    ) -> None:
        """
        Initializes a new BaseTask instance.

        ## Args:
            `session` (Session): The session used for querying the database.
            `name` (str, optional): The name of the task. Defaults to "Unnamed Task".
        """
        self.session = session
        self.capture_exceptions = capture_exceptions
        self.name = name
        self._timer: threading.Timer
        self._running = True

    @property
    def countdown(self) -> int:
        """
        Placeholder propery; returns the time interval between task runs in seconds.
        """
        raise Exception(f"Countdown on '{self.name}' is undefined")

    def start(self) -> None:
        """
        Starts the task.
        """
        self._running = True
        self._timer = threading.Timer(self.countdown, self.run)
        self._timer.start()

    def stop(self):
        """
        Stops the task.
        """
        self._running = False
        if hasattr(self, "_timer"):
            self._timer.cancel()

    def run(self) -> None:
        """
        Runs the task and prints task status and execution time.
        """
        if not self._running:
            return

        try:
            start = time.time()
            self.exec()

            end = time.time()
            time_spent = end - start

            next_iteration = datetime.today() + timedelta(
                seconds=round(self.countdown, 2)
            )
            next_iteration = next_iteration.replace(microsecond=0)

            success_message = (
                f"{bcolors.OKGREEN}TASK SUCCESSFUL{bcolors.ENDC}"
                f"{bcolors.BOLD}: {self.name}{bcolors.ENDC}"
                f" - Time spent: {bcolors.BOLD}{str(round(time_spent, 2))}{bcolors.ENDC}s"
                f" - Next iteration: {bcolors.BOLD}{next_iteration}{bcolors.ENDC}s"
            )
            print(success_message)

        except Exception as exc:
            get_logger("task-failed_" + str(exc))
            logging.exception(exc)

            if self.capture_exceptions:
                end = time.time()
                time_spent = end - start

                failure_message = (
                    f"{bcolors.FAIL}{bcolors.BOLD}{bcolors.UNDERLINE}TASK FAILED{bcolors.ENDC}"
                    f"{bcolors.ENDC}{bcolors.BOLD}: {self.name}{bcolors.ENDC}"
                    f" - Time spent: {bcolors.BOLD}{str(round(time_spent, 2))}{bcolors.ENDC}s"
                    f" - Error: {exc}"
                )
                print(failure_message)
                logging.info(failure_message)
                self.stop()
                return exc

            raise exc

        if self._running:
            self._timer = threading.Timer(self.countdown, self.run)
            self._timer.start()

    def exec(self) -> None:
        """
        Placeholder method for defining task behavior.
        """
        ...


# NOTE: Example task.

class Task(BaseTask):
    def __init__(self, session, capture_exceptions) -> None:
        name = "Example Task"
        super().__init__(session, capture_exceptions, name)

    @property
    def countdown(self) -> int:
        # Run every 0 seconds (instantly, aka continuesly)
        return 0

    def exec(self) -> None:
        ...
