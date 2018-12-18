from segments.segmentsCommon import SegmentsCommon
from markers import Markers

class SOI(SegmentsCommon):
    def __init__(self):
        super(SOI, self).__init__()

    def analyze(self, marker, body):
        if marker != Markers.SOI:
            raise ValueError("invailed marker. class SOI excepting marker is " + Markers.SOI.to_bytes(1, 'big') + ". but " + marker.to_bytes(1, 'big') + " found.")
        return {
            "segmentName": "SOI",
            "length": 0,
        }
