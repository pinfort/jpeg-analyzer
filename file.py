from markers import Markers

class File(object):
    IS_SCANNING = False
    IMAGES = []
    IMG_DATA = []

    def __init__(self, path):
        super(File, self).__init__()
        self.f = open(path, 'rb')

    def __del__(self):
        self.f.close()

    def getData(self, count):
        bt = list(self.f.read(count))
        if self.IS_SCANNING:
            self.IMG_DATA.extend(bt)
        return bt

    def __getSegmentBodyLength(self, length_for_length_data):
        length = 0
        for i in range(length_for_length_data):
            length = length + (self.getData(1)[0] * (0x100 ** (length_for_length_data - i - 1)))
        return length - length_for_length_data
    
    def __getSegmentBody(self, length_for_length_data = 2):
        body_length = self.__getSegmentBodyLength(length_for_length_data)
        return self.getData(body_length)

    # return dict
    def getSegment(self, marker):
        if marker not in Markers.REGISTERED_MARKERS:
            raise Exception("unexpected marker found. it's not supported.")
        if marker != Markers.JUST_FF:
            # データの最後にマーカー（2ビット）がついているので末尾2ビット削除
            self.IMG_DATA = self.IMG_DATA[0:len(self.IMG_DATA) - 2]
            self.IMAGES.append(self.IMG_DATA)
            self.IMG_DATA = []
            self.IS_SCANNING = False
        if marker in [Markers.JUST_FF, Markers.SOI, Markers.EOI]:
            return {
                "marker": marker,
                "body": None,
            }
        body = self.__getSegmentBody()
        if marker == Markers.SOS:
            self.IS_SCANNING = True
        return {
                "marker": marker,
                "body": body,
            }
