class HeaderAnalyze(object):
    SOI = 0xd8
    EOI = 0xd9
    JUST_FF = 0x00

    # cf. https://hp.vector.co.jp/authors/VA032610/JPEGFormat/marker/SOF.htm
    SOF = [
        0xC0, # ハフマン / ベースライン / 非差分
        0xC1, # ハフマン / シーケンシャル / 非差分
        0xC2, # ハフマン / プログレッシブ / 非差分
        0xC3, # ハフマン / ロスレス / 非差分
        0xC5, # ハフマン / シーケンシャル / 差分
        0xC6, # ハフマン / プログレッシブ / 差分
        0xC7, # ハフマン / ロスレス / 差分
        0xC9, # 算術 / シーケンシャル / 非差分
        0xCA, # 算術 / プログレッシブ / 非差分
        0xCB, # 算術 / ロスレス / 非差分
        0xCD, # 算術 / シーケンシャル / 差分
        0xCE, # 算術 / プログレッシブ / 差分
        0xCF, # 算術 / ロスレス / 差分
    ]

    RST = [
        0xD0,
        0xD1,
        0xD2,
        0xD3,
        0xD4,
        0xD5,
        0xD6,
        0xD7,
    ]

    # cf. https://hp.vector.co.jp/authors/VA032610/JPEGFormat/JPEGsegment.htm
    DQT = 0xDB # 量子化テーブル定義
    DHT = 0xC4 # ハフマンテーブル定義
    DRI = 0xDD
    COM = 0xFE
    SOS = 0xDA
    APP = [
        0xE0,
        0xE1,
        0xE2,
        0xE3,
        0xE4,
        0xE5,
        0xE6,
        0xE7,
        0xE8,
        0xE9,
        0xEA,
        0xEB,
        0xEC,
        0xED,
        0xEE,
        0xEF,
    ]

    REGISTERED_MARKERS = []
    REGISTERED_MARKERS.extend(SOF)
    REGISTERED_MARKERS.extend(APP)
    REGISTERED_MARKERS.extend(RST)
    REGISTERED_MARKERS.append(SOI)
    REGISTERED_MARKERS.append(DQT)
    REGISTERED_MARKERS.append(DHT)
    REGISTERED_MARKERS.append(DRI)
    REGISTERED_MARKERS.append(COM)
    REGISTERED_MARKERS.append(SOS)
    REGISTERED_MARKERS.append(EOI)
    REGISTERED_MARKERS.append(JUST_FF)

    def __init__(self, path):
        super(HeaderAnalyze, self).__init__()
        self.f = open(path, 'rb')
    
    def __del__(self):
        self.f.close()
    
    def __getData(self, count):
        if count < 2:
            return int.from_bytes(self.f.read(count), 'big')
        return list(self.f.read(count))

    # return Dict || Bytes
    def TokenizeLoop(self):
        try:
            bt = self.__getData(1)
        except Exception as e:
            return []

        if bt == 0xFF:
            return self.__Tokenize()
        else:
            return self.TokenizeLoop()


    # return Dict
    def __Tokenize(self):
        segmentsList = []

        try:
            bt = self.__getData(1)
        except Exception as e:
            return segmentsList
        
        if bt == 0xFF:
            segmentsList.extend(self.__Tokenize())
        elif bt in self.REGISTERED_MARKERS:
            segmentsList.append(self.__AnalyzeMarkers(bt))
        segmentsList.extend(self.TokenizeLoop())
        return segmentsList

    # return Dict
    def __AnalyzeMarkers(self, bt):
        if bt == self.SOI:
            # SOI (FFD8) has no body
            return {
                "segmentName": "SOI",
                "length": 0,
            }
        elif bt == self.EOI:
            # EOI (FFD9) has no body
            return {
                "segmentName": "EOI",
                "length": 0,
            }
        elif bt == self.JUST_FF:
            return {
                "segmentName": "JUST_FF",
                "length": 0
            }

        body = self.__getSegmentBody()
        if bt in self.SOF:
            # do sof
            return self.__analyzeSof(body)
        elif bt == self.DQT:
            # do dqt
            return self.__analyzeDqt(body)
        elif bt == self.DHT:
            # do dht
            return self.__analyzeDht(body)
        elif bt == self.DRI:
            # do dri
            pass
        elif bt == self.COM:
            # do com
            pass
        elif bt in self.APP:
            # do app
            return self.__analyzeApp(bt, body)
        elif bt == self.SOS:
            # do sos
            return self.__analyzeSos(body)
        elif bt in self.RST:
            # do rst
            pass
        else:
            raise ValueError(str(b'\xFF') + str(bt.to_bytes(1, 'big')) + " is not supported marker")
        return {
            "segmentName": "Not Implemented",
            "length": 0,
        }

    def __getSegmentBodyLength(self, length_for_length_data):
        length = 0
        for i in range(length_for_length_data):
            length = length + (self.__getData(1) * (0x100 ** (length_for_length_data - i - 1)))
        return length - length_for_length_data
    
    def __getSegmentBody(self, length_for_length_data = 2):
        body_length = self.__getSegmentBodyLength(length_for_length_data)
        return self.__getData(body_length)

    def __analyzeSof(self, body):
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
    
    def __analyzeDqt(self, body):
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
    
    def __analyzeDht(self, body):
        analyzed = {}
        analyzed["length"] = len(body) + 2
        analyzed["segmentName"] = "DHT"
        tn = body[0]
        analyzed["tcn"] = (tn & 0b11110000) >> 4
        analyzed["thn"] = tn & 0b00001111
        l = [body[i] for i in range(1, 17)]
        v = [body[i] for i in range(17, len(body))]
        # lはL1 ~ L16までが入る
        
        if analyzed["tcn"] == 0:
            table = self.__getDcHuffmanTable(l, v)
        elif analyzed["tcn"] == 1:
            raise NotImplementedError("AC huffman table support not inplemented")
        else:
            raise Exception("invalied data. not supported")
        analyzed["table"] = table
        return analyzed
    
    def __getHuffmanTableBitList(self, l):
        # 例
        # [0, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # [
        #     0b00,
        #     0b01,
        #     0b10,
        #     0b110,
        #     0b1110,
        #     0b11110,
        #     0b111110,
        #     0b1111110,
        # ]
        # [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # [
        #     0b0,
        #     0b10,
        #     0b110,
        #     0b1110,
        #     0b11110,
        #     0b111110,
        # ]
        bit_length = 0
        bitList = []
        for bit_num in l:
            bit_length = bit_length + 1
            if bit_num == 0:
                continue
            if len(bitList) == 0:
                # 最初の符号
                bitList.append(format(0, '0' + str(bit_length) + 'b'))
                bit_num = bit_num - 1

            if bit_num == 0:
                continue
            
            for i in range(bit_num):
                # 二つ目以降
                before = bitList[len(bitList) - 1]
                before_len = len(before)
                before_int = int(before, 2)
                new_int = before_int + 1
                if before_len < bit_length:
                    new_str = format(new_int, '0' + str(before_len) + 'b')
                    new_str = new_str + ('0' * (bit_length - before_len))
                else:
                    new_str = format(new_int, '0' + str(bit_length) + 'b')
                bitList.append(new_str)
        return bitList
    
    def __getDcHuffmanTableDef(self, bitList, v):
        if len(bitList) != len(v):
            raise Exception("invalid data")
        table = {}
        for i in range(len(bitList)):
            target_bit = bitList[i]
            target_data_bit_length = v[i]
            # table[target_bit] = target_data_bit_length
            if target_data_bit_length == 0:
                table[target_bit] = 0
            else:
                for i in range(2 ** target_data_bit_length):
                    val = format(i, '0' + str(target_data_bit_length) + 'b')
                    if val[0] == '0':
                        val2 = val.replace('0', '2').replace('1', '0').replace('2', '1')
                        table[target_bit + val] = int(val2, 2) * -1
                    else:
                        table[target_bit + val] = i
        return table
    
    def __getAcHuffmanTableDef(self, bitList, v):
        if len(bitList) != len(v):
            raise Exception("invalid data")
        pass

    def __getDcHuffmanTable(self, l, v):
        bitList = self.__getHuffmanTableBitList(l)
        return self.__getDcHuffmanTableDef(bitList, v)
    
    def __getAcHuffmanTable(self, l, v):
        bitList = self.__getHuffmanTableBitList(l)
        return self.__getAcHuffmanTableDef(bitList, v)
    
    def __analyzeApp(self, bt, body):
        if bt == 0xE0:
            return self.__analyzeAppJfif(body)
        elif bt == 0xE2:
            return self.__analyzeAppIccprofile(body)
        else:
            return self.__analyzeAppNotImplemented(bt, body)
    
    def __analyzeAppJfif(self, body):
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
    
    def __analyzeAppIccprofile(self, body):
        analyzed = {}
        analyzed["segmentName"] = "APP2"
        analyzed["body"] = body
        return analyzed
    
    def __analyzeAppNotImplemented(self, bt, body):
        analyzed = {}
        analyzed["segmentName"] = "APP" + str(bt & 0b00001111)
        analyzed["body"] = body
        return analyzed

    def __analyzeSos(self, body):
        analyzed = {}
        analyzed["ns"] = body[0]
        analyzed["cs"] = []
        offset = 0
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
        print(analyzed)
        return analyzed


if __name__ == "__main__":
    # path = "C:\\Users\\pinfo\\Downloads\\DsmAkbxVYAEKktJ_orig.jpg"
    label = [
        "HEADER: ",
        "IMAGE",
    ]
    # C:\\Users\\pinfo\\Documents\\CIMG1106.JPG
    analyzed = HeaderAnalyze("C:\\Users\\pinfo\\Downloads\\DsmAkbxVYAEKktJ_orig.jpg").TokenizeLoop()
    # print(analyzed)
