from segments.segmentsCommon import SegmentsCommon
from markers import Markers

# Define huffman table
class DHT(SegmentsCommon):
    def __init__(self):
        super(DHT, self).__init__()

    def analyze(self, marker, body):
        if marker != Markers.DHT:
            raise ValueError("invailed marker. class DHT excepting marker is " + Markers.DHT.to_bytes(1, 'big') + ". but " + marker.to_bytes(1, 'big') + " found.")
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
            table = self.__getAcHuffmanTable(l, v)
        else:
            raise Exception("invalied data. not supported")
        analyzed["table"] = table
        return analyzed

    def __getHuffmanTableBitList(self, l):
        # ex.
        # <<I [0, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # >>O [
        #     0b00,
        #     0b01,
        #     0b10,
        #     0b110,
        #     0b1110,
        #     0b11110,
        #     0b111110,
        #     0b1111110,
        # ]
        # <<I [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # >>O [
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
        table = {}
        for i in range(len(bitList)):
            target_bit = bitList[i]
            target_zero_runlength = v[i] >> 4
            target_data_bit_length = v[i] & 0b00001111
            if v[i] == 0:
                table[target_bit] = ["EOB"]
            elif target_data_bit_length == 0:
                table[target_bit] = []
                [table[target_bit].append(0) for i in range(target_zero_runlength)]
            else:
                for i in range(2 ** target_data_bit_length):
                    target_data_list = []
                    [target_data_list.append(0) for i in range(target_zero_runlength)]
                    val = format(i, '0' + str(target_data_bit_length) + 'b')
                    if val[0] == '0':
                        val2 = val.replace('0', '2').replace('1', '0').replace('2', '1')
                        target_data_list.append(int(val2, 2) * -1)
                        table[target_bit + val] = target_data_list
                    else:
                        target_data_list.append(i)
                        table[target_bit + val] = target_data_list
        return table

    def __getDcHuffmanTable(self, l, v):
        bitList = self.__getHuffmanTableBitList(l)
        return self.__getDcHuffmanTableDef(bitList, v)
    
    def __getAcHuffmanTable(self, l, v):
        bitList = self.__getHuffmanTableBitList(l)
        return self.__getAcHuffmanTableDef(bitList, v)
