# XMLFormatter.py
class XMLFormatter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(XMLFormatter, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    #Singleton kontorlü
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        pass

    # indent metodu aynı kalıyor
    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "

            for idx, e in enumerate(elem):
                self.indent(e, level + 1)

                if not e.tail or not e.tail.strip():
                    if idx < len(elem) - 1:
                        e.tail = i + "  "
                    else:
                        e.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i