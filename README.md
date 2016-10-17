# pyStrangerBoard
Python serial interface to StrangerBoard Arduino sketch

# Setup

* Install python3 and pip3
* Copy `strangertweets.ini` to `src`, add your Twitter API key info and the path to the USB tty device associated with your Arduino
* `pip3 install -r src/requirements.txt`
* `cd src ; python3 -u strangertweets.py`

## Raspberry Pi example

Copy `strangertweets.ini` into your `src` directory.

With Arduino **unplugged**:

    ls /dev/tty*
    
Make a note of the tty devices, then plug in the Arduino to USB and:

    ls /dev/tty*

Find the new tty device, add it to `strangerhacks.ini` in the `src` directory. Add your Twitter API keys as well. It uses
app-only auth, so you don't need to complete a auth handshake with an account; just the API consumer key and secret are needed.

Then:

    sudo apt install python3 python3-pip
    cd src
    sudo pip3 install -r requirements.txt
    python3 -u strangertweets.py
