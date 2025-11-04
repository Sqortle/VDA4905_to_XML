# SegmentProcessorFactory.py
from SegmentProcessors import Segment511Processor, Segment512Processor, Segment513Processor, Segment514Processor

# Factory'nin kullanacağı Sınıf (Class) referansları
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
        """
        Segment etiketine göre ilgili işlemci sınıfının bir örneğini döndürür.
        """
        processor_class = PROCESSOR_CLASSES.get(tag)

        if processor_class:
            # Sınıfı bulduktan sonra, onun bir örneğini oluşturur ve döndürür (Fabrika işi)
            return processor_class()

            # Eğer geçerli bir segment etiketi değilse None döndür (veya hata fırlat)
        return None