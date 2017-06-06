# Communication-examples
Simple bluetooth and wormhole python implementation

## Bluetooth with GUI
Requires Python 3, and with minor fixes will also works with Python 2
This program uses the library `pybluez`.

This is an example of sending a message

![Sending](https://i.imgur.com/NMEd5z1.gif)

And this is an example of the receive

![Receiving](http://imgur.com/GGrxzOM.gif)

## Bluetooth
Requires Python 3.3+

Execute `bluetooth_server.py` in one device and then `bluetooth_client.py` in another device.


## Magic Wormhole GUI
Requires Python 3, and with minor fixes will also works with Python 2.
Requires the latest git version of Magic Wormhole.

In Arch Linux it can be installed with the AUR package `magic-wormhole-git`.

If you want to use the latests stable version of Magic Wormhole, switch to the branch `0.9.2`.

To start utilize it simply execute `$ python3 worm_messages.py`

This is an example of usage

![wormhole utilization](https://i.imgur.com/WqZ2aOz.gif)

This program is interoperable with the cli official version of Magic Wormhole.

![wormhole interoperability](https://i.imgur.com/xAGoRMC.gif)

## Magic Wormhole
Can be used either with Python 2 or 3

Requires wormhole `$ pip install magic-wormhole`
