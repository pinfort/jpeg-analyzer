from segments.segmentsCommon import SegmentsCommon
from markers import Markers

class DQT(SegmentsCommon):
    def __init__(self):
        super(DQT, self).__init__()

    def analyze(self, marker, body):
        if marker != Markers.DQT:
            raise ValueError("invailed marker. class DQT excepting marker is " + Markers.DQT.to_bytes(1, 'big') + ". but " + marker.to_bytes(1, 'big') + " found.")
        analyzed = {}
        analyzed["length"] = len(body) + 2
        analyzed["segmentName"] = "DQT"
        analyzed["tables"] = []
        dqt = self.__analyzeDqtTable(body)
        analyzed["tables"].append(dqt[0])
        while len(dqt[1]) > 0:
            dqt = self.__analyzeDqtTable(body)
            analyzed["tables"].append(dqt[0])
        return analyzed

    def __analyzeDqtTable(self, body):
        tableDict = {}
        qn = body[0]
        tableDict["pqn"] = (qn & 0b11110000) >> 4
        tableDict["tqn"] = qn & 0b00001111
        tableBody = []
        if tableDict["pqn"] == 0:
            for i in range(1, 65):
                tableBody.append(body[i])
            body = body[65:]
        elif tableDict["pqn"] == 1:
            for i in range(1, 129, 2):
                tableBody.append(body[i] + body[i + 1])
            body = body[129:]
        else:
            raise Exception("unsupported pqn")
        tableDict["body"] = tableBody
        return [tableDict, body]
