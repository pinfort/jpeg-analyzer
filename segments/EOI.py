from segments.segmentsCommon import SegmentsCommon
from markers import Markers

class EOI(SegmentsCommon):
    def __init__(self):
        super(EOI, self).__init__()

    def analyze(self, marker, body):
        if marker != Markers.EOI:
            raise ValueError("invailed marker. class EOI excepting marker is " + Markers.EOI.to_bytes(1, 'big') + ". but " + marker.to_bytes(1, 'big') + " found.")
        return {
            "segmentName": "EOI",
            "length": 0,
        }
