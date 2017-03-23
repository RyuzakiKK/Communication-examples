from twisted.internet import reactor
from wormhole.cli.public_relay import RENDEZVOUS_RELAY
from wormhole.wormhole import wormhole
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--code", type=str, help="PAKE code")
parser.add_argument("-m", "--message", type=str, help="message to send")
args = parser.parse_args()


def _got(inbound_message):
    print("Inbound message:", inbound_message)

w2 = wormhole(u"ryuzaki", RENDEZVOUS_RELAY, reactor)

if args.code:
    w2.set_code(unicode(args.code, 'utf-8'))
else:
    w2.set_code(u'4-cannonball-tux')

if args.message:
    w2.send(str.encode(args.message))
else:
    w2.send(b"hello")

d = w2.get()
d.addCallback(_got)
d.addCallback(w2.close)
d.addBoth(lambda _: reactor.stop())
reactor.run()
