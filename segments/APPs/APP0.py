from segments.segmentsCommon import SegmentsCommon
from markers import Markers

class APP0(SegmentsCommon):
    def __init__(self):
        super(APP0, self).__init__()

    def analyze(self, marker, body):
        analyzed = {}
        analyzed["segmentName"] = "APP0"
        assert body[0:5] == [ord('J'), ord('F'), ord('I'), ord('F'), 0x00], 'for APP0, JFIF is only supported. maybe it contains JFXX segment?'
        # TODO: support JFXX segent
        analyzed["format"] = "JFIF"
        analyzed["ver"] = str(body[5]) + '.' + str(body[6])
        analyzed["units"] = body[7] # 0 = None, 1 = dpi, 2 = dpcm
        analyzed["xdensity"] = body[8] * 0x100 + body[9]
        analyzed["ydensity"] = body[10] * 0x100 + body[11]
        analyzed["xthumbnail"] = body[12]
        analyzed["ythumbnail"] = body[13]
        if analyzed["xthumbnail"] * analyzed["ythumbnail"] > 0:
            analyzed["RGB"] = body[14:14 + 3 * analyzed["xthumbnail"] * analyzed["ythumbnail"]]
        return analyzed
