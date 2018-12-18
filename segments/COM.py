import sys
import os
sys.path.append(os.pardir)

from segmentsCommon import SegmentsCommon
from markers import Markers

class COM(SegmentsCommon):
    def __init__(self):
        super(COM, self).__init__()

    def analyze(self, marker, body):
        if marker != Markers.COM:
            raise ValueError("invailed marker. class COM excepting marker is " + Markers.COM.to_bytes(1, 'big') + ". but " + marker.to_bytes(1, 'big') + " found.")
        analyzed = {}
        analyzed["segmentName"] = "COM"
        analyzed["comment"] = ''.join([chr(i) for i in body])
        return analyzed
