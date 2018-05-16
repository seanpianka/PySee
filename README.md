# PySee

---

## Synopsis
A free and open source screenshot sharing tool, built in Python 3, for Linux and Mac OS X.

<p align="center">
    <img src="https://i.imgur.com/Ttocjp7.png" alt="A screenshot showing PySee">
</p>

#### Requires
* imgurpython
* pyperclip
* requests
* `xsel` or `xclip`

## Installation
```bash
    $ pip install pysee
    ✨🍰✨
```

Per [`pyperclip`](https://github.com/asweigart/pyperclip) module documentation:
> On Linux, this module makes use of the `xclip` or `xsel` commands, which should come with the os. Otherwise run "`sudo apt-get install xclip`" or "`sudo apt-get install xsel`" (Note: `xsel` does not always seem to work.)

<a href='https://ko-fi.com/A80049AF' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi4.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## Usage
```bash
usage: pysee.py [-h] [--init] [--mode mode] [--image-host host]
                [--screenshot-tool tool] [--save-directory dir] [--upload]
                [--logging] [--clipboard] [--save] [--gui]

optional arguments:
  -h, --help            show this help message and exit
  --init                Initialize PySee and its configuration file
                        information.
  --mode mode, -m mode  Set the mode to take a screenshot in. Ensure you have
                        a screenshot tool installed which supports the desired
                        mode.
  --image-host host, -i host
                        Image host name to upload the screenshot to.
  --screenshot-tool tool, -t tool
                        Name of screenshot program to use.
  --save-directory dir, -d dir
                        Where to locally save the screenshot.
  --upload, -u          Upload screenshot to an image host after capture.
  --logging, -l         Output any logged information to the terminal.
  --clipboard, -c       Copy image URL to system clipboard after capture.
  --save, -s            Save screenshot locally after capture.
  --gui                 Start PySee in GUI mode.

```
  
After opening the graphical user interface, select your image host (default is to locally save screenshots), edit the configuration file (optional, auto-generated version will suffice for uploading to [imgur.com](https://imgur.com/)), and take a screenshot! If the screenshot is uploaded to a image host, the URL to the image will be copied to the system clipboard (unless disabled).

## Code Example
```python
    >>> from pysee import PySee
    >>> pysee = PySee()
    >>> pysee.main('imgur', 'scrot', 'region')
    [+] Screenshot capture: "2018-05-16-17-36-56.png" was saved in "/home/sean/Pictures/".
    [+] Image upload: "2018-05-16-17-36-56.png" was uploaded to "imgur" at "https://i.imgur.com/GZHVJsL.png".
    [+] Clipboard copy: "https://i.imgur.com/GZHVJsL.png" has been copied to your system clipboard.
    'https://i.imgur.com/GZHVJsL.png'
```

## Uninstallation
```bash
    $ pip uninstall pysee
```

and remove the `~/.config/pysee/` directory in your home (`~`) directory.

## Support

* Capture Tools
  * Mac OS X:
     * `screencapture`
  * Linux
     * `gnome-screenshot`
     * `shutter`
     * `scrot`
     * `xfce4-screenshot`
* Image Hosts
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

