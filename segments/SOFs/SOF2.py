from segments.segmentsCommon import SegmentsCommon
from markers import Markers

class SOF2(SegmentsCommon):
    def __init__(self):
        super(SOF2, self).__init__()

    def analyze(self, marker, body):
        if marker != Markers.SOF[2]:
            raise ValueError("invailed marker. class SOF excepting marker is " + Markers.SOF[2].to_bytes(1, 'big') + ". but " + marker.to_bytes(1, 'big') + " found.")
        analyzed = {}
        analyzed["length"] = len(body) + 2
        analyzed["segmentName"] = "SOF"
        analyzed["p"] = body[0]
        analyzed["y_size"] = body[1] * 0x100 + body[2]
        analyzed["x_size"] = body[3] * 0x100 + body[4]
        analyzed["nf"] = body[5]
        analyzed["nfData"] = []
        nfHead = 6
        nfLength = 3
        for i in range(analyzed["nf"]):
            nfDict = {}
            nf = body[nfHead:nfHead + nfLength]
            nfDict["cn"] = nf[0]
            hv = nf[1]
            nfDict["hn"] = (hv & 0b11110000) >> 4
            nfDict["vn"] = hv & 0b00001111
            nfDict["tqn"] = nf[2]
            analyzed["nfData"].append(nfDict)
            nfHead = nfHead + nfLength
        return analyzed
