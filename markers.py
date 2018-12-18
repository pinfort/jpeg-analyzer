class Markers(object):
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
