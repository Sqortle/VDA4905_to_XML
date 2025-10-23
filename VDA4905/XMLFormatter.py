# XMLFormatter.py
class XMLFormatter:
    def __init__(self):
        pass
        
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
