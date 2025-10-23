# FileHandler.py
import xml.etree.ElementTree as ET
from datetime import datetime

class FileHandler:

    def __init__(self):
        pass

    def write_file(self, tree, schedule_no_str, ean_loc, dock_code, base_path):
        
        current_date_str = datetime.now().strftime("%Y-%m-%d")

        safe_ean_loc = ean_loc if ean_loc else "UNKNOWN"
        safe_dock_code = dock_code if dock_code else "0000"

        filename = f"VDA4905_{schedule_no_str}_{safe_ean_loc}_{safe_dock_code}_{current_date_str}.xml"
        output_path = base_path.rstrip('/') + '/' + filename
        
        try:
            tree.write(output_path, encoding="ISO-8859-1", xml_declaration=True)
            return output_path
        except Exception as e:
            print(f"Error writing file {output_path}: {e}")
            return None
