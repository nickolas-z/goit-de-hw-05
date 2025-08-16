import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(level=logging.INFO, log_to_file=True, out_dir=None, suppress_console=False):
    """
    Colored console logging plus optional file logging into `out/`.
    By default writes logs to `out/app-YYYYmmdd-HHMMSS.log` with rotation.
    """
    class ColorFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': '\x1b[36m',   # cyan
            'INFO': '\x1b[32m',    # green
            'WARNING': '\x1b[33m', # yellow
            'ERROR': '\x1b[31m',   # red
            'CRITICAL': '\x1b[41m',# red background
        }
        RESET = '\x1b[0m'

        def format(self, record):
            levelname = record.levelname
            color = self.COLORS.get(levelname, '')
            record.levelname = f"{color}{levelname}{self.RESET}"
            return super().format(record)

    root = logging.getLogger()
    # clear existing handlers to avoid duplicate logs
    for h in list(root.handlers):
        root.removeHandler(h)

    # console handler
    fmt = '%(asctime)s %(levelname)s %(message)s'
    if not suppress_console:
        ch = logging.StreamHandler()
        ch.setFormatter(ColorFormatter(fmt))
        root.addHandler(ch)

    # file handler
    if log_to_file:
        if out_dir is None:
            out_dir = os.path.join(os.getcwd(), 'out')
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        logfile = os.path.join(out_dir, f'app-{ts}.log')
        fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=5_000_000, backupCount=3, encoding='utf-8')
        fh.setFormatter(logging.Formatter(fmt))
        root.addHandler(fh)

    root.setLevel(level)

    return root
