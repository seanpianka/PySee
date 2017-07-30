"""
error
~~~~~

Allow for custom error messages when handling PySee

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None
"""


class PySeeError(BaseException):
    def __init__(self, message, status_code=1):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return "PyseeError[Errno %s]: %s" % (self.status_code, self.message)


pysee_errors = {'1': PySeeError("No screenshot tool was located on system", 1),
                '2': PySeeError("Unable to upload screenshot to selected image host", 2),
                '3': PySeeError("Failed to process or execute screenshot command", 3),
                '4': PySeeError("Unable to locate the desired image file", 4),
                '5': PySeeError("No clipboard tool was located on the system", 5),
                '6': PySeeError("OS race condition detected", 6),
                '7': PySeeError("Unable to parse configuration file", 7),
                '8': PySeeError("Keyboard interrupt detected", 8),
                '9': PySeeError("Image host detected an error in image upload attempt", 9)}
