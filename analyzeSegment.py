from markers import Markers
from segments.SOI import SOI
from segments.EOI import EOI
from segments.SOF import SOF
from segments.DQT import DQT
from segments.DHT import DHT
from segments.COM import COM
from segments.APP import APP
from segments.SOS import SOS

class analyzeSegment(object):
    def __init__(self):
        super(analyzeSegment, self).__init__()

    def analyze(self, marker, body):
        if marker == Markers.JUST_FF:
            return None
        if marker == Markers.SOI:
            # SOI (FFD8) has no body
            return SOI().analyze(marker, body)
        elif marker == Markers.EOI:
            # EOI (FFD9) has no body
            return EOI().analyze(marker, body)
        if marker in Markers.SOF:
            # do sof
            return SOF().analyze(marker, body)
        elif marker == Markers.DQT:
            # do dqt
            return DQT().analyze(marker, body)
        elif marker == Markers.DHT:
            # do dht
            return DHT().analyze(marker, body)
        elif marker == Markers.DRI:
            # do dri
            pass
        elif marker == Markers.COM:
            # do com
            return COM().analyze(marker, body)
        elif marker in Markers.APP:
            # do app
            return APP().analyze(marker, body)
        elif marker == Markers.SOS:
            # do sos
            return SOS().analyze(marker, body)
        elif marker in Markers.RST:
            # do rst
            pass
        else:
            raise ValueError(str(b'\xFF') + str(marker.to_bytes(1, 'big')) + " is not supported marker")
        return {
            "segmentName": "Not Implemented",
            "length": 0,
        }
