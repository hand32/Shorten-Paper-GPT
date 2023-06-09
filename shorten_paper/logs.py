import logging
import os
import random
import re
import time
from logging import LogRecord

from colorama import Fore, Style

from shorten_paper.singletone import Singleton


class Logger(metaclass=Singleton):
    """
    Logger that handle titles in different colors.
    Outputs log in console, activity.log, and errors.log
    For console handler: simulates typing
    """

    def __init__(self, log_to_file=False):
        # create log directory if it doesn't exist
        if log_to_file:
            this_files_dir_path = os.path.dirname(__file__)
            log_dir = os.path.join(this_files_dir_path, "../logs")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            log_file = "activity.log"
            error_file = "error.log"

            # Info handler in activity.log
            self.file_handler = logging.FileHandler(
                os.path.join(log_dir, log_file), "a", "utf-8"
            )
            self.file_handler.setLevel(logging.DEBUG)
            info_formatter = AutoFormatter(
                "%(asctime)s %(levelname)s %(title)s %(message_no_color)s"
            )
            self.file_handler.setFormatter(info_formatter)

            # Error handler error.log
            error_handler = logging.FileHandler(
                os.path.join(log_dir, error_file), "a", "utf-8"
            )
            error_handler.setLevel(logging.ERROR)
            error_formatter = AutoFormatter(
                "%(asctime)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(title)s"
                " %(message_no_color)s"
            )
            error_handler.setFormatter(error_formatter)

        console_formatter = AutoFormatter("%(title_color)s %(message)s")

        # Create a handler for console which simulate typing
        self.typing_console_handler = TypingConsoleHandler()
        self.typing_console_handler.setLevel(logging.INFO)
        self.typing_console_handler.setFormatter(console_formatter)

        # Create a handler for console without typing simulation
        self.console_handler = ConsoleHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(console_formatter)

        self.typing_logger = logging.getLogger("TYPER")
        self.typing_logger.addHandler(self.typing_console_handler)
        if log_to_file:
            self.typing_logger.addHandler(self.file_handler)
            self.typing_logger.addHandler(error_handler)
        self.typing_logger.setLevel(logging.DEBUG)

        self.logger = logging.getLogger("LOGGER")
        self.logger.addHandler(self.console_handler)
        if log_to_file:
            self.logger.addHandler(self.file_handler)
            self.logger.addHandler(error_handler)
        self.logger.setLevel(logging.DEBUG)

    def typewriter_log(
        self, title="", title_color="", content="", level=logging.INFO
    ):
        if content:
            if isinstance(content, list):
                content = " ".join(content)
        else:
            content = ""

        self.typing_logger.log(
            level, content, extra={"title": title, "color": title_color}
        )

    def debug(
        self,
        message,
        title="",
        title_color="",
    ):
        self._log(title, title_color, message, logging.DEBUG)

    def warn(
        self,
        message,
        title="",
        title_color="",
    ):
        self._log(title, title_color, message, logging.WARN)

    def error(self, title, message=""):
        self._log(title, Fore.RED, message, logging.ERROR)

    def _log(self, title="", title_color="", message="", level=logging.INFO):
        if message:
            if isinstance(message, list):
                message = " ".join(message)
        self.logger.log(level, message, extra={"title": title, "color": title_color})

    def set_level(self, level):
        self.logger.setLevel(level)
        self.typing_logger.setLevel(level)

    def double_check(self, additional_text=None):
        if not additional_text:
            additional_text = (
                "Please ensure you've setup and configured everything"
                " correctly."
            )
        self.typewriter_log("DOUBLE CHECK CONFIGURATION", Fore.YELLOW, additional_text)


"""
Output stream to console using simulated typing
"""


class TypingConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        min_typing_speed = 0.05
        max_typing_speed = 0.005

        msg = self.format(record)
        try:
            words = msg.split()
            for i, word in enumerate(words):
                print(word, end="", flush=True)
                if i < len(words) - 1:
                    print(" ", end="", flush=True)
                typing_speed = random.uniform(min_typing_speed, max_typing_speed)
                time.sleep(typing_speed)
                # type faster after each word
                min_typing_speed = min_typing_speed * 0.95
                max_typing_speed = max_typing_speed * 0.95
            print()
        except Exception:
            self.handleError(record)


class ConsoleHandler(logging.StreamHandler):
    def emit(self, record) -> None:
        msg = self.format(record)
        try:
            print(msg)
        except Exception:
            self.handleError(record)


class AutoFormatter(logging.Formatter):
    """
    Allows to handle custom placeholders 'title_color' and 'message_no_color'.
    To use this formatter, make sure to pass 'color', 'title' as log extras.
    """

    def format(self, record: LogRecord) -> str:
        if hasattr(record, "color"):
            record.title_color = (
                getattr(record, "color")
                + getattr(record, "title")
                + " "
                + Style.RESET_ALL
            )
        else:
            record.title_color = getattr(record, "title")
        if hasattr(record, "msg"):
            record.message_no_color = remove_color_codes(getattr(record, "msg"))
        else:
            record.message_no_color = ""
        return super().format(record)


def remove_color_codes(s: str) -> str:
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", s)


logger = Logger()
