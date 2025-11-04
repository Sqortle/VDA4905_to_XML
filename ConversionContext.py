# ConversionContext.py
import xml.etree.ElementTree as ET
from typing import Optional

#Data Transfer Object class
class ConversionContext:

    def __init__(self, schedule_no_str, valid_from_date, ean_loc, 
                 schedule_el: ET.Element, 
                 article_lines_el: Optional[ET.Element],
                 demand_lines_el: Optional[ET.Element]):
        
        self.schedule_no_str = schedule_no_str
        self.valid_from_date = valid_from_date
        self.ean_loc = ean_loc

        self.schedule_el = schedule_el
        self.article_lines_el = article_lines_el
        self.demand_lines_el = demand_lines_el

        self.current_article_line = None
        self.customer_po_no = None
        self.dock_code = None
        self.last_delivery_date = None
