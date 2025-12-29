import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

MAX_BYTES = 3 * 1024 * 1024  # 3 MB
MAX_FILES = 5
LOG_PREFIX = "app"


class NumberedRotatingFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_file = self._log_path(1)

    def _log_path(self, index):
        return os.path.join(LOG_DIR, f"{LOG_PREFIX}{index}.log")

    def _should_rotate(self):
        return (
            os.path.exists(self.log_file)
            and os.path.getsize(self.log_file) >= MAX_BYTES
        )

    def _rotate(self):
        # Delete oldest
        oldest = self._log_path(MAX_FILES)
        if os.path.exists(oldest):
            os.remove(oldest)

        # Shift logs up (4 → 5, 3 → 4, ...)
        for i in range(MAX_FILES - 1, 0, -1):
            src = self._log_path(i)
            dst = self._log_path(i + 1)
            if os.path.exists(src):
                os.rename(src, dst)

        # Create new app1.log
        open(self._log_path(1), "w").close()

    def emit(self, record):
        try:
            if self._should_rotate():
                self._rotate()

            msg = self.format(record)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")

        except Exception:
            self.handleError(record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = NumberedRotatingFileHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False
    return logger
