# PySee
A lightweight screenshot tool for Linux and OSx, built in Python, with automatic Imgur uploading and system clipboard copying.

# Operation
The script will check for valid installations of known screenshot tools from
popular desktop managers and use a given list of commands to perform the
screenshots. There is currently no method for changing the type of screenshot
performed (currently set to area screenshot with pointer shown), but eventually
there will be a way to switch between a variety of options.

After taking the screenshot, the file is timestamped and saved in ~/Pictures/
and is then uploaded anonmously to Imgur.com through their API. The link that
is return is then sent to the system clipboard.

# Plans
All of the checks for valid installations and the screenshots are done through
the command-line (via the subprocess module), so this may or may not have
issues associated with it. I am looking to move away from requiring the user to
navigate to the installation directory via command-line and start with "Python3
pysee.py," along with implementation of a GUI and hotkeys for ease of use.

Additionally, there will also (eventually) be an option to allow for the user
to choose which image host is used for uploading and which screenshot manager
they would like to use (recognize valid installations and allow for
selections).

# Installation
Download the code as a zip file, extract to a directory, and run the PySee.py script from the terminal with Python3.

# Uninstallation
Remove the main PySee/ directory and the hidden .pysee/ directory in your home (~/) directory. There are no other extraneous files.
