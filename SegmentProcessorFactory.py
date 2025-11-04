# SegmentProcessorFactory.py
from SegmentProcessors import Segment511Processor, Segment512Processor, Segment513Processor, Segment514Processor

#Factorynin kyllanması gerekne sınıfları mapledik
PROCESSOR_CLASSES = {
    "511": Segment511Processor,
    "512": Segment512Processor,
    "513": Segment513Processor,
    "514": Segment514Processor,
}


class SegmentProcessorFactory:

    def __init__(self):
        pass

    def get_processor(self, tag):
        #tag ile eşleşen sınıfı alıyoruz
        processor_class = PROCESSOR_CLASSES.get(tag)

        if processor_class:
            # tage göre sınıf bulup döndürme
            return processor_class()

            #Tag ile uyuşan sınıf yok ise None döndürür
        return None