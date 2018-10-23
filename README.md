# PySee

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


Future Functionality of PySee
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Capturing Screenshots:
~~~~~~~~~~~~~~~~~~~~~~
* Fullscreen
* Active window
* Active monitor
* Window menu
* Monitor menu
* Region (possibly with added annotation, possibly text annotiation or picture?)
* Polygon (custom shape for the screenshot as opposed to rectangular)
* Freehand (draw a shape for the screenshot with the cursor, then use that)
* Last region (take a screenshot of the region that was last captured, same shape)
* Custom region (allowing for separated regions to be all captured in one file)
* Screen recording (either saved as a .mp4 or .gif/.webm)
* Automatic/timed capture


After Capture Tasks:
~~~~~~~~~~~~~~~~~~~~
* Add image effects or watermarks
* Open in image editor
* Copy image to clipboard
* Print image
* Save image to file /as/ (allow for custom file naming)
* Copy file or file path to clipboard
* Upload to image host
* Delete file locally


After Upload Tasks:
~~~~~~~~~~~~~~~~~~~
* Upload file or directory
* Upload from clipboard
* Upload from url (given a url of a picture, upload that to specified host)
* Watch directory for new files added, upload to host when found


Supporting Image Hosts:
~~~~~~~~~~~~~~~~~~~~~~~
* Imgur
* ImageShack
* TinyPic
* Flickr
* Photobucket
* Google Photos (Picasa)
* Twitter
* vgy.me
* someimage.com
* imgland.net


URL Shorteners:
~~~~~~~~~~~~~~~
* bit.ly
* goo.gl
* is.gd
* v.gd
* tinyurl.com
* adf.ly
* turl.ca
* coinurl.com
* qr.net
* vurl.com
* 2.gp


Tools:
~~~~~~
* Color picker
* Screen color picker
* Image editor
* Image effects
* Hash check
* DNS changer
* QR code generator
* Ruler
* FTP client
* Tweet message
* Monitor test


