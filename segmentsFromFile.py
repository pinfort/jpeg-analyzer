from file import File
from markers import Markers

class SegmentFromFile(object):
    def __init__(self, path):
        super(SegmentFromFile, self).__init__()
        self.f = File(path)

    def tokenizeLoop(self):
        btl = self.f.getData(1)
        while len(btl) != 0:
            segment = self.__tokenize(btl[0])
            if segment is not None:
                yield segment
            btl = self.f.getData(1)

    def __tokenize(self, bt):
        if bt == 0xFF:
            bt2 = self.f.getData(1)[0]
            if bt2 in Markers.REGISTERED_MARKERS:
                return self.f.getSegment(bt2)
            else:
                while bt2 != 0xFF:
                    bt2 = self.f.getData(1)[0]
                return self.__tokenize(bt2)
        else:
            while bt != 0xFF:
                bt = self.f.getData(1)[0]
            return self.__tokenize(bt)
