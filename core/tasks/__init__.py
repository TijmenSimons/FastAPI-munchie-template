from datetime import datetime, timedelta
import os
import glob
import importlib.util
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import config

from core.tasks.base_task import BaseTask
from core.helpers import bcolors
from dotenv import load_dotenv

load_dotenv()


def get_tasks(session) -> list[BaseTask]:
    """
    Find and import task modules starting with "task_" from the tasks directory
    and return a list of instantiated task objects with the provided session and
    capture_exceptions arguments.

    Args:
        session: A SQLAlchemy database session object.

    Returns:
        A list of instantiated task objects.

    Raises:
        Any exceptions raised by the imported task modules.
    """
    paths_to_tasks = glob.glob(f"{os.getcwd()}\\core\\tasks\\task_*.py")
    tasks: list[BaseTask] = []

    for path_to_task in paths_to_tasks:
        # https://stackoverflow.com/questions/67631

        spec = importlib.util.spec_from_file_location("module.name", path_to_task)
        module = importlib.util.module_from_spec(spec)

        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        tasks.append(
            module.Task(
                session=session, capture_exceptions=config.TASK_CAPTURE_EXCEPTIONS
            )
        )

    return tasks


def start_tasks() -> None:
    """
    Create a SQLAlchemy database engine and session, retrieve tasks using the
    get_tasks() function and start each task, printing a message for each task
    with the task name and start time.

    Returns:
        None

    Raises:
        None
    """
    if config.ENV == "test":
        print("Cannot run tasks in test environment")
        return

    # Not using the config's connection string as that uses async.
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DU')}:{os.getenv('DP')}@{os.getenv('H')}:{os.getenv('P')}/{os.getenv('DB')}"
    )
    Session = sessionmaker(engine)

    with Session() as session:
        tasks = get_tasks(session)

        for task in tasks:
            task.start()

            next_iteration = datetime.today() + timedelta(seconds=task.countdown)
            next_iteration = next_iteration.replace(microsecond=0)

            print(
                f"{bcolors.OKGREEN}INFO{bcolors.ENDC}:  "
                f"Task {bcolors.BOLD}{task.name}{bcolors.ENDC}"
                f" starts at: {bcolors.BOLD}{next_iteration}{bcolors.ENDC}"
            )
