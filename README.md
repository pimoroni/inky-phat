![Inky pHAT](inky-phat-logo.png)
http://shop.pimoroni.com/products/inky-phat

**NOTE** This library has been superceded by the new [Inky Python library](https://github.com/pimoroni/inky) that supports both the Inky pHAT e-paper displays and the larger Inky wHAT e-paper displays, all in one library. The new Inky library does however drop support for the very first version of Inky pHAT, so if you have one of them then you'll need to use this older Inky pHAT library.

You have a newer Inky pHAT if:

* It's any colour other than Red (IE: Yellow and Black/White Inky pHATs were only available as V2)
* Has a square inductor on the reverse of the board (large compared to the other components, and dark grey)

## Installing

### Full install (recommended):

We've created an easy installation script that will install all pre-requisites and get your Inky pHAT
up and running with minimal efforts. To run it, fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop, as illustrated below:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the command exactly as it appears below (check for typos) and follow the on-screen instructions:

```bash
curl https://get.pimoroni.com/inkyphat | bash
```

If you choose to download examples you'll find them in `/home/pi/Pimoroni/inkyphat/`.

### Manual install:

#### Library install for Python 3:

```bash
sudo apt-get install python3-inkyphat
```

#### Library install for Python 2:

```bash
sudo apt-get install python-inkyphat
```

### Development:

If you want to contribute, or like living on the edge of your seat by having the latest code, you should clone this repository, `cd` to the library directory, and run:

```bash
sudo apt-get install python-dev python-setuptools
sudo python3 setup.py install
```
(or `sudo python setup.py install` whichever your primary Python environment may be)

In all cases you will have to enable the SPI bus.

## Documentation & Support

* Guides and tutorials - https://learn.pimoroni.com/inky-phat
* Function reference - http://docs.pimoroni.com/inkyphat/
* GPIO Pinout - http://pinout.xyz/pinout/inky_phat
* Get help - http://forums.pimoroni.com/c/support
