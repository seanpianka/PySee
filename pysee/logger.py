import logging
import sys


class PySeeFormatter(logging.Formatter):
    err_fmt  = "[*] ERROR: %(msg)s"
    dbg_fmt  = "[-] DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "[+] %(msg)s"

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = PySeeFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = PySeeFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = PySeeFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


class PySeeLogger(logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formatter = PySeeFormatter()
        handler = logging.StreamHandler(sys.stdout)
        #logger = logging.Logger(__name__)
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(logging.INFO)
