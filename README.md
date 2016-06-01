# PySee - A Lightweight Screenshot Tool
---
## Synopsis
A `free`, `open source,` and `lightweight` `screenshot sharing tool`, built in `Python 3`, for `GNU/Linux` and `Mac OS X`.

<p align="center">
    <img src="https://i.imgur.com/cgwS67K.png" alt="A screenshot showing PySee">
</p>

## Motivation
I have found no suitable screenshot tools for GNU/Linux or OSX that are simple (yet customizable), lightweight, and perform similarly across platforms. I hope to develop a tool that satisfies all three desires: **PySee**

#### Requires
* imgurpython
* pyperclip
* requests

## Installation
```bash
    $ pip install pysee
    ✨🍰✨
```

Per [`pyperclip`](https://github.com/asweigart/pyperclip) module documentation:
> On Linux, this module makes use of the `xclip` or `xsel` commands, which should come with the os. Otherwise run "`sudo apt-get install xclip`" or "`sudo apt-get install xsel`" (Note: `xsel` does not always seem to work.)

## Usage
```bash
    $ pysee [OPTIONS]
    or
    $ pysee-gui
```
Options:
  * -h --help
  * -w --window
  * -r --region
  * -f --full-area
  * -1 --no-upload
  * -2 --no-output
  * -3 --no-clipboard
  * ~~-4 --timed~~
  * -s --imgur
  * -s --slimg

  
After opening the graphical user interface, select your image host (default is to locally save screenshots), edit the configuration file (optional, auto-generated version will suffice for uploading to [imgur.com](https://imgur.com/)), and take a screenshot! If the screenshot is uploaded to a image host, the URL to the image will be copied to the system clipboard (unless disabled).

## Code Example
```python
    >>> from pysee import take_screenshot
    >>> # optional kwargs are: image_host="imgur", mode="r", timed=False
    >>> # no_clipboard=False, no_output=False, no_upload=False
    >>> take_screenshot(image_host="imgur", mode="r")
    Uploading screenshot...                                # will produce PySeeError exception on failure
    Successful upload of 2016-04-03-21-33-45.png!          # year, month, day, hour, minute, seconds
    You can find it here: https://i.imgur.com/cgwS67K.png  # direct URL to hosted image
                                                           # output shown determined by "no_output" arg
    It has also been copied to your system clipboard.      # copying determined by "no_clipboard" arg
    "/home/user/Pictures/2016-04-03-21-33-45.png"          # returns path to file on successful upload
```

## Uninstallation
```bash
    $ pip uninstall pysee
```

and remove the `~/.config/pysee/` directory in your home (~/) directory. There are no other extraneous files.

## Planned and Future Updates
1. Supported Image Hosts
   * [x] [Imgur](https://imgur.com/)
   * [ ] [ImageShack](https://imageshack.us)
   * [ ] [TinyPic](http://tinypic.com/)
   * [ ] [Flickr](https://www.flickr.com/)
   * [ ] [Photobucket](http://s5.photobucket.com/)
   * [ ] [Google Photos (Picasa)](https://photos.google.com/)
   * [ ] [Twitter](https://twitter.com/)
   * [ ] [vgy.me](https://vgy.me/)
   * [ ] [SomeImage.com](https://someimage.com/)
   * [ ] [imgland.net](http://imgland.net/)
2. Supported 
   * Currently supported tools:
      * Mac OS X:
         * `screencapture`
      * GNU/Linux: Ubuntu, Debian:
         * `gnome-screenshot`
         * `shutter`
   * [ ] Expand supported tools
   * [x] Basic user selection of image-host
3. Custom storage locations and names (patterns or specific names/lists prefixs)
   * [x] Allow for user-defined paths for local screenshot saving.
4. GUI implementation
   * [x] Move away from command-line startup with GUI implementation
5. System-wide hotkeys
    * [ ] Custom, cross-platform hotkeys
    * [ ] GUI or other process that listens (while minimized) for hotkey combinations system-wide
6. Timer
   * [ ] Allow for a user-set timer to automatically take a screenshot of either an open window, all screens, or region.
   * [ ] Send to image host, FTP, Dropbox/Google Drive, save to specific location, etc..
7. Dedicated website for tool
   * [x] Move it away from GitHub (beyond hosting of the source) -- [Here's a start.](http://pysee.me/)
8. Command-line Arguments
   * [ ] Add command-line arguments + associated options.

## Contributors
[![Sean Pianka](https://avatars2.githubusercontent.com/u/15352684?v=3&s=120)](http://twitter.com/seanpianka) |
---|
[Sean Pianka](http://seanpianka.com/)

## License

Currently, I have chosen to have **no license**, meaning no modifications or distributions of copies of this software are allowed without express consent from the developers. In addition, this module is currently only available for personal, non-commercial use.

