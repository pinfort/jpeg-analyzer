from abc import ABCMeta, abstractmethod

class SegmentsCommon(metaclass=ABCMeta):
    @abstractmethod
    def analyze(self, marker, body):
        pass
