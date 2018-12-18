from segments.segmentsCommon import SegmentsCommon
from markers import Markers

# Start of scan
class SOS(SegmentsCommon):
    def __init__(self):
        super(SOS, self).__init__()

    def analyze(self, marker, body):
        if marker != Markers.SOS:
            raise ValueError("invailed marker. class SOS excepting marker is " + Markers.SOS.to_bytes(1, 'big') + ". but " + marker.to_bytes(1, 'big') + " found.")
        analyzed = {}
        analyzed["segmentName"] = "SOS"
        analyzed["ns"] = body[0]
        analyzed["cs"] = []
        offset = 1
        for i in range(analyzed["ns"]):
            cs = {}
            cs["id"] = body[offset]
            cs["td"] = body[offset + 1] >> 4
            cs["ta"] = body[offset + 1] & 0b00001111
            analyzed["cs"].append(cs)
            offset = offset + 2
        offset = 2 * analyzed["ns"] + 1
        analyzed["ss"] = body[offset]
        analyzed["se"] = body[offset + 1]
        analyzed["ah"] = body[offset + 2] >> 4
        analyzed["al"] = body[offset + 2] & 0b00001111
        return analyzed
