from segmentsFromFile import SegmentFromFile
from analyzeSegment import analyzeSegment

def getAnalyzedSegments(path):
    analyzedSegments = []
    SOSs = []
    analyzer = analyzeSegment()
    segs = SegmentFromFile(path)
    for seg in segs.tokenizeLoop():
        analyzed = analyzer.analyze(seg["marker"], seg["body"])
        if analyzed is None:
            continue
        if analyzed["segmentName"] == "SOF":
            print("X:", analyzed["x_size"], "Y:", analyzed["y_size"])
            for nf in analyzed["nfData"]:
                print(nf["id"], nf["name"], nf["hn"], "x", nf["vn"])
        elif analyzed["segmentName"] == "SOS":
            SOSs.append(analyzed)
        analyzedSegments.append(analyzed)
    assert(len(SOSs) == len(segs.f.IMAGES))
    count = 0
    for segments in analyzedSegments:
        if segments["segmentName"] == "SOS":
            segments["image"] = segs.f.IMAGES[count]
            count = count + 1
        yield segments

def main(path):
    for segment in getAnalyzedSegments(path):
        print(segment["segmentName"])

if __name__ == '__main__':
    path = "C:\\Users\\pinfo\\Downloads\\DsmAkbxVYAEKktJ_orig.jpg"
    main(path)
