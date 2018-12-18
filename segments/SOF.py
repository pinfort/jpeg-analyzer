import sys
import os
sys.path.append(os.pardir)

from segmentsCommon import SegmentsCommon
from markers import Markers

from SOFs.SOF2 import SOF2

class SOF(SegmentsCommon):
    def __init__(self):
        super(SOF, self).__init__()

    def analyze(self, marker, body):
        if marker not in Markers.SOF:
            raise ValueError("invailed marker. marker " + marker.to_bytes(1, 'big') + " found. class SOF is not excepting it.")
        if marker == Markers.SOF[0]:
            # 0xC0, # ハフマン / ベースライン / 非差分
            pass
        elif marker == Markers.SOF[1]:
            # 0xC1, # ハフマン / シーケンシャル / 非差分
            pass
        elif marker == Markers.SOF[2]:
            # 0xC2, # ハフマン / プログレッシブ / 非差分
            return SOF2().analyze(marker, body)
        elif marker == Markers.SOF[3]:
            # 0xC3, # ハフマン / ロスレス / 非差分
            pass
        elif marker == Markers.SOF[4]:
            # 0xC5, # ハフマン / シーケンシャル / 差分
            pass
        elif marker == Markers.SOF[5]:
            # 0xC6, # ハフマン / プログレッシブ / 差分
            pass
        elif marker == Markers.SOF[6]:
            # 0xC7, # ハフマン / ロスレス / 差分
            pass
        elif marker == Markers.SOF[7]:
            # 0xC9, # 算術 / シーケンシャル / 非差分
            pass
        elif marker == Markers.SOF[8]:
            # 0xCA, # 算術 / プログレッシブ / 非差分
            pass
        elif marker == Markers.SOF[9]:
            # 0xCB, # 算術 / ロスレス / 非差分
            pass
        elif marker == Markers.SOF[10]:
            # 0xCD, # 算術 / シーケンシャル / 差分
            pass
        elif marker == Markers.SOF[11]:
            # 0xCE, # 算術 / プログレッシブ / 差分
            pass
        elif marker == Markers.SOF[12]:
            # 0xCF, # 算術 / ロスレス / 差分
            pass
        else:
            raise ValueError("invailed marker. marker " + marker.to_bytes(1, 'big') + " found. class SOF is not excepting it.\nSOF expecting marker is below.\n" + str([m.to_bytes(1, 'big') for m in Markers.SOF]))
        raise NotImplementedError("this type JPEG file should be going to support but not yet.")
