"""
Project: PKN Lighted dance floor / LED Art 

"""

# Fadecandy stuff
# import opc

# Artnet stuff
from twisted.internet import protocol, endpoints
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import time

leds_per_universe = 128
numLEDs = 2048
dry_run_client = True

if dry_run_client:
    print "initialize OPC socket..."
else:
    client = opc.Client('localhost:7890')
black = (0, 0, 0)

## Calculate some derived parameters:
# Assumes no remainder:
num_universes = numLEDs / leds_per_universe
if numLEDs % leds_per_universe != 0:
    raise Exception('non-integer number of universes')

class ArtNet(DatagramProtocol):
    def __init__(self):
        self.pixels = [black] * numLEDs
        self.universe_received = [False] * num_universes
        self.opc_write_count = 0
        self.time_of_first_flush = None

    def write_universe(self, universe_id, universe_pixels):
        global_offset = leds_per_universe*universe_id
        self.pixels[global_offset:global_offset+leds_per_universe] = universe_pixels
        self.universe_received[universe_id] = True
        if all(self.universe_received):
            if dry_run_client:
                # print "putting pixels in OPC client ..."
                foo = 1
            else:
                client.put_pixels(self.pixels)
            if self.opc_write_count == 0:
                self.time_of_first_flush = time.time()
            elif self.opc_write_count % 200 == 0:
                rate = self.opc_write_count / (time.time()-self.time_of_first_flush)
                print "Average number of OPC writes per second: %f" % rate
            self.opc_write_count += 1
            self.universe_received = [False] * num_universes

    def datagramReceived(self, data, (host, port)):
        if ((len(data) > 18) and (data[0:8] == "Art-Net\x00")):
            #print "detected artnet datagram..."
            rawbytes = map(ord, data)
            opcode = rawbytes[8] + (rawbytes[9] << 8)
            protocolVersion = (rawbytes[10] << 8) + rawbytes[11]
            if ((opcode == 0x5000) and (protocolVersion >= 14)):
                sequence = rawbytes[12]
                physical = rawbytes[13]
                sub_net = (rawbytes[14] & 0xF0) >> 4
                universe = rawbytes[14] & 0x0F
                net = rawbytes[15]
                rgb_length = (rawbytes[16] << 8) + rawbytes[17]
                # print "seq %d phy %d sub_net %d uni %d net %d len %d" % \
                #    (sequence, physical, sub_net, universe, net, rgb_length)
                idx = 18
                universe_pixels = [black] * leds_per_universe
                universe_offset = 0
                while (idx < (rgb_length + 18)):
                    # print(rawbytes[idx])
                    r = rawbytes[idx]
                    idx += 1
                    g = rawbytes[idx]
                    idx += 1
                    b = rawbytes[idx]
                    idx += 1
                    # print("x= " + str(x) + ", y=" + str(y) + " r=" + str(r) + ", g=" + str(g) + "b= " +str(b))
                    universe_pixels[universe_offset] = (r, g, b)
                    universe_offset += 1
                self.write_universe(universe, universe_pixels)


reactor.listenUDP(6454, ArtNet())
reactor.run()
