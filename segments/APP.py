import warnings

from segments.segmentsCommon import SegmentsCommon
from markers import Markers
from segments.APPs.APP0 import APP0

class APP(SegmentsCommon):
    def __init__(self):
        super(APP, self).__init__()

    def analyze(self, marker, body):
        if marker == Markers.APP[0]:
            return APP0().analyze(marker, body)
        elif marker == Markers.APP[1]:
            pass
        elif marker == Markers.APP[2]:
            pass
        elif marker == Markers.APP[3]:
            pass
        elif marker == Markers.APP[4]:
            pass
        elif marker == Markers.APP[5]:
            pass
        elif marker == Markers.APP[6]:
            pass
        elif marker == Markers.APP[7]:
            pass
        elif marker == Markers.APP[8]:
            pass
        elif marker == Markers.APP[9]:
            pass
        elif marker == Markers.APP[10]:
            pass
        elif marker == Markers.APP[11]:
            pass
        elif marker == Markers.APP[12]:
            pass
        elif marker == Markers.APP[13]:
            pass
        elif marker == Markers.APP[14]:
            pass
        elif marker == Markers.APP[15]:
            pass
        else:
            raise ValueError("invailed marker. marker " + marker.to_bytes(1, 'big') + " found. class APP is not excepting it.\nAPP expecting marker is below.\n" + str([m.to_bytes(1, 'big') for m in Markers.APP]))
        warnings.warn("this type APP segment not supported. please inform to the author.")
