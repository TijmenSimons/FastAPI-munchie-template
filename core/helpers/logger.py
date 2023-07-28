import logging
import os
from datetime import datetime
from pathlib import Path

import unicodedata
import re


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "-", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def get_logger(exc: Exception | str = None):
    """Initializes logger and generates log name."""

    Path(os.getcwd() + "/logs").mkdir(parents=True, exist_ok=True)

    log_name = "_".join(
        [
            datetime.now().strftime("%m%d%Y-%H%M%S"),
            (slugify(str(exc)[:50]) or "untitled"),
        ]
    ).lower()

    logging.basicConfig(
        filename=f"logs/{log_name}.log",
        format="%(levelname)s\t%(asctime)s: %(message)s",
        encoding="utf-8",
        level=logging.INFO,
        force=True,
    )

    return log_name
