![Inky pHAT](inky-phat-logo.png)
http://shop.pimoroni.com/products/inky-phat

**Note** that Inky pHAT uses a new display now (as of early December 2017), and **requires an updated library**. This new library automagically detects the display version, so should work interchangeably with the old and new displays.

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
sudo apt-get install python3-pip python3-dev
sudo pip3 install inkyphat
```

#### Library install for Python 2:

```bash
sudo apt-get install python-pip python-dev
sudo pip install inkyphat
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
