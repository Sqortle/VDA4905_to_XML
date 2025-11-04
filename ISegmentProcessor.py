from abc import ABC, abstractmethod
from ConversionContext import ConversionContext

#Interface
class ISegmentProcessor(ABC):

    @abstractmethod
    def process(self, segment: str, context: ConversionContext):
        pass
