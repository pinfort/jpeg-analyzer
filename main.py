from segmentsFromFile import SegmentFromFile
from analyzeSegment import analyzeSegment

def main(path):
    analyzer = analyzeSegment()
    segs = SegmentFromFile(path)
    for seg in segs.tokenizeLoop():
        analyzed = analyzer.analyze(seg["marker"], seg["body"])
        print(analyzed) if analyzed is not None else ""

if __name__ == '__main__':
    path = "C:\\Users\\pinfo\\Downloads\\DsmAkbxVYAEKktJ_orig.jpg"
    main(path)
