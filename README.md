# PySee - A Lightweight Screenshot Tool
---
## Synopsis
A `lightweight screenshot tool` for `Linux`* and `Mac OS X`*, built in `Python 3`, with automatic `image host uploading` and `system clipboard copying`.

![PySee Tool Picture](https://i.imgur.com/cgwS67K.png)

#### Requires
* datetime
* imgurpython
* pyperclip
* requests

## Usage
```bash
    $ pysee
```

After opening the graphical user interface, select your image host (default is to locally save screenshots), edit the configuration file (optional, auto-generated version will suffice for uploading to [imgur.com](https://imgur.com/)), and take a screenshot! If the screenshot is uploaded to a image host, the URL to the image will be copied to the system clipboard (unless disabled).

## Code Example
```python
    >>> from pysee import take_screenshot
    >>> take_screenshot(image_host="Imgur", clipboard=True, output=True)
    Uploading screenshot...                                # screenshot name format: 
    Successful upload of 2016-04-03-21-33-45.png!          # year, month, day, hour, minute seconds
    You can find it here: http://i.imgur.com/RIntAoK.png   # direct URL to hosted image
                                                           # output shown determined by "output" arg
    It has also been copied to your system clipboard.      # copying determined by "clipboard" arg
    True                                                   # returns True on successful upload
```

## Motivation
I have found no suitable screenshot tools for GNU/Linux or OSX that are simple (yet customizable), lightweight, and perform similarly across platforms. I hope to develop a tool that satisfies all three desires: **PySee**

## Planned Updates
1. Choice of image hosting
   * Allow for user-selection of hosting including by not limited to:
      * [x] [Imgur](https://imgur.com/)
      * [x] [Minus](http://uploads.im/)
      * [ ] Possibly my own?
2. Wider selection of supported screenshot tools
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

## Installation
```bash
    $ pip install pysee
    ✨🍰✨
```
**NOTE:** The package is currently hidden while the graphical user interface is being updated.

Per [`pyperclip`](https://github.com/asweigart/pyperclip) module documentation:
> On Linux, this module makes use of the `xclip` or `xsel` commands, which should come with the os. Otherwise run "`sudo apt-get install xclip`" or "`sudo apt-get install xsel`" (Note: `xsel` does not always seem to work.)

## Uninstallation
```bash
    $ pip uninstall pysee
```

and remove the hidden `~/.pysee/` directory in your home (~/) directory. There are no other extraneous files.

## Contributors
[![Sean Pianka](https://avatars2.githubusercontent.com/u/15352684?v=3&s=460)](http://twitter.com/seanpianka) |
---|
[Sean Pianka](http://seanpianka.com/)

## License

Currently, I have chosen to have **no license**, meaning no modifications or distributions of copies of this software are allowed without express consent from the developers. In addition, this module is currently only available for personal, non-commercial use.
