# PySee
A `lightweight screenshot tool` for `Linux` and `OSx`, built in `Python`, with automatic `Imgur uploading` and `system clipboard copying`.

---

# Operation
The script will check for valid installations of known screenshot tools from
popular desktop managers and use a given list of commands to perform the
screenshots. There is currently no method for changing the type of screenshot
performed (currently set to area screenshot with pointer shown), but eventually
there will be a way to switch between a variety of options.

After taking the screenshot, the file is timestamped and saved in ~/Pictures/
and is then uploaded anonymously to [Imgur.com](http://imgur.com/) through their [API](https://api.imgur.com/). The link that
is return is then sent to the system clipboard.

# Issues
1. All of the files for the tool must be manually installed.
2. Dependencies must be manually installed.
3. No method for alternate forms of screenshots besides physically hardcoding differences in the `pysee.py` file.
4. Tool must be run from the command-line for each screenshot.
5. Screenshot mechanism and valid installation checks performed on the command-line via the `subprocess` Python module.

# Plans
1. ##### Choice of image hosting
   * Allow for user-selection of hosting including by not limited to:
      * [Imgur](http://imgur.com/)
      * [Minus](http://minus.com/)
      * [Photobucket](http://s5.photobucket.com/)
      * [PostImage](http://postimage.org/)
      * Possibly my own?
2. ##### Wider selection of available screenshot tools
   * Currently, the supported tools are:
      * OSx:
         1. `screencapture`
      * Linux (Ubuntu/Debian):
         1. `gnome-screenshot`
         2. `shutter`
   * I would like to make this list more encompassing and allow for user-selection + modification (without having to hard-code changes to the `pysee.py` file.
3. ##### Custom storage locations and names (patterns or specific names/lists prefixs)
   * Allow for user-defined path and name for screenshot saving.
4. ##### GUI implementation
   * *Move away from command-line startup* and allow for easier usage through a GUI (possibly through `tkinter`?) which allows for "presence" (be a program that can stay running in the background, listening from the next item on the list...
5. ##### System-wide hotkeys
   * This is my main gripe with the current implementation... I have to start the damn thing from the terminal. If there was ever a time where I needed to quickly capture something... _it's gone!_ This will change... once I figure out how.
6. ##### Timer
   * Allow for a user-set timer to automatically take a screenshot of either an open window, all screens, or region.
   * Send to image host, FTP, Dropbox/Google Drive, save to specific location, etc..
7. ##### Dedicated website for downloading/tutorials
   * Move it away from GitHub (beyond hosting of the source)
8. ##### Installation via `pip`

# Installation
Download the code as a zip file, extract to a directory, and run the PySee.py script from the terminal with Python3.

# Uninstallation
Remove the main PySee/ directory and the hidden .pysee/ directory in your home (~/) directory. There are no other extraneous files.
