"""
exceptions
~~~~~~~~~~

Allow for custom error messages when handling PySee

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None
"""


class PySeeError(BaseException):
    pass

"""
PySeeError("Unable to upload screenshot to selected image host", 2)
PySeeError("Unable to locate the desired image file", 4)
PySeeError("No clipboard tool was located on the system", 5)
PySeeError("Image host detected an error in image upload attempt", 9)
"""
