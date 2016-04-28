class PySeeError(Exception):
    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return "PyseeError: [Errno %s] %s" % (self.status_code,
                                                  self.error_message)
        else:
            return self.error_message

pysee_errors = {
    '1': PySeeError("No screenshot tool was located on system", 1),
    '2': PySeeError("Unable to upload screenshot to selected image host", 2),
    '3': PySeeError("Failed to process or execute screenshot command", 3),
    '4': PySeeError("Unable to locate the desired image file", 4),
    '5': PySeeError("No clipboard tool was located on the system", 6),
    '6': PySeeError("OS race condition detected", 7),
    '7': PySeeError("Unable to parse configuration file", 8),
    '8': PySeeError("Keyboard interrupt detected", 9),
}
