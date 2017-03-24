from twisted.internet import reactor
from wormhole.cli.public_relay import RENDEZVOUS_RELAY
from wormhole.wormhole import wormhole
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--code", type=str, help="PAKE code")
args = parser.parse_args()


def _got(inbound_message):
    print("Inbound message:", inbound_message)
    w1.send(b"ok")

w1 = wormhole(u"ryuzaki", RENDEZVOUS_RELAY, reactor)

if args.code:
    w1.set_code(args.code)
else:
    w1.set_code(u'4-cannonball-tux')

d = w1.get()
d.addCallback(_got)
d.addCallback(w1.close)
d.addBoth(lambda _: reactor.stop())
reactor.run()
