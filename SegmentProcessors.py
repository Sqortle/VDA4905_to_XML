import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from ISegmentProcessor import ISegmentProcessor
from ConversionContext import ConversionContext

class BaseSegmentProcessor:
    def __init__(self):
        pass
    
    def format_date(self, date_value):
        date_value = date_value.strip()
        if len(date_value) == 6:
            return f"20{date_value[:2]}-{date_value[2:4]}-{date_value[4:]}T00:00:00" 
        return ""
        
    def safe_int_to_str(self, value_string):
        stripped_value = value_string.strip()
        if not stripped_value:
            return "0"
        
        try:
            return str(int(stripped_value))
        except ValueError:
            return "0"

    def _get_first_monday_of_month(self, year, month):
        try:
            dt = datetime(year, month, 1)
            day_of_week = dt.weekday()
            days_until_monday = (7 - day_of_week) % 7 
            if day_of_week == 0:
                 days_until_monday = 0 
            
            return dt + timedelta(days=days_until_monday)
        except ValueError:
            return None 
            
    def _get_monday_of_week(self, year, week_num):
        try:
            return datetime.fromisocalendar(year, week_num, 1)
        except ValueError:
            return None 

    def get_schedule_info(self, date_value):
        date_value = date_value.strip()
        
        line_type_id = "1"
        delivery_date_dt = None
        formatted_date_str = self.format_date(date_value)

        if len(date_value) != 6:
            return formatted_date_str, "1"

        try:
            year = 2000 + int(date_value[0:2])
            month = int(date_value[2:4])
            day_or_week = date_value[4:6]
            
            if day_or_week == "00" and 1 <= month <= 12:
                delivery_date_dt = self._get_first_monday_of_month(year, month)
                line_type_id = "2"
            
            elif month == 0 and 1 <= int(day_or_week) <= 53: 
                week_num = int(day_or_week)
                delivery_date_dt = self._get_monday_of_week(year, week_num)
                line_type_id = "2"
            
            if delivery_date_dt:
                formatted_date_str = delivery_date_dt.strftime("%Y-%m-%dT00:00:00")

        except Exception:
            pass
            
        return formatted_date_str, line_type_id


class Segment511Processor(BaseSegmentProcessor, ISegmentProcessor):
    def process(self, segment: str, context: ConversionContext):
        ET.SubElement(context.schedule_el, "VENDOR_NO").text = segment[14:23].strip()
        ET.SubElement(context.schedule_el, "EAN_LOCATION").text = context.ean_loc
        ET.SubElement(context.schedule_el, "MESSAGE_ID").text = segment[30:33].strip()
        ET.SubElement(context.schedule_el, "SENDER_COMMUNICATION_ID").text = segment[5:14].strip()
        ET.SubElement(context.schedule_el, "RECEIVER_COMMUNICATION_ID").text = segment[14:23].strip()
        ET.SubElement(context.schedule_el, "VALID_FROM").text = self.format_date(segment[33:39])
        ET.SubElement(context.schedule_el, "SHIP_FROM").text = segment[14:23].strip()


class Segment512Processor(BaseSegmentProcessor, ISegmentProcessor):
    def process(self, segment: str, context: ConversionContext):
        
        current_article_line = ET.SubElement(context.article_lines_el, "ARTICLE_LINE")
        ET.SubElement(current_article_line, "PART_NO").text = segment[38:60].strip()
        ET.SubElement(current_article_line, "CALL_OF_NO").text = segment[8:11].strip()
        ET.SubElement(current_article_line, "SCHEDULE_NO").text = context.schedule_no_str
        
        # Bağlamı güncelle (DTO'ya yaz)
        context.current_article_line = current_article_line
        context.customer_po_no = segment[82:93].strip()
        context.dock_code = segment[94:98].strip()


class Segment513Processor(BaseSegmentProcessor, ISegmentProcessor):
    def process(self, segment: str, context: ConversionContext):
        
        if context.current_article_line is None:
            return 

        cum_qty = self.safe_int_to_str(segment[37:47])
        last_qty = self.safe_int_to_str(segment[25:37])
        
        ET.SubElement(context.current_article_line, "LAST_RECEIPT_REFERENCE").text = segment[13:19].strip()
        ET.SubElement(context.current_article_line, "CUM_RECEIPT_QTY").text = cum_qty
        ET.SubElement(context.current_article_line, "LAST_RECEIPT_QTY").text = last_qty
        ET.SubElement(context.current_article_line, "LAST_RECEIPT_DATE").text = self.format_date(segment[5:11])
       
        self.process_demand_fields(segment, context, 47, 122)
    
    def process_demand_fields(self, segment, context, start_index, end_index):
        last_processed_date = context.last_delivery_date
        
        for i in range(start_index, min(len(segment), end_index), 15):
            date_field = segment[i:i + 6].strip()
            qty_field = self.safe_int_to_str(segment[i + 6:i + 15])

            if not date_field or date_field in ["000000", "222222", "555555"]:
                continue

            if date_field == "333333":
                delivery_date = context.valid_from_date
                line_type_id = "3"
            else:
                delivery_date, line_type_id = self.get_schedule_info(date_field)

            last_processed_date = delivery_date
            
            self.functionScheduleLineHeaders(
                context.demand_lines_el, context.current_article_line, context.schedule_no_str, 
                delivery_date, line_type_id, qty_field, context.customer_po_no, context.dock_code
            )
            
        context.last_delivery_date = last_processed_date

    def functionScheduleLineHeaders(self, demand_lines_el, current_article_line, schedule_no_str, delivery_date, line_type_id, qty_field, customer_po_no, dock_code):
        current_schedule_no = ET.SubElement(demand_lines_el, "SCHEDULE_LINE")
        ET.SubElement(current_schedule_no, "PART_NO").text = current_article_line.find("PART_NO").text
        ET.SubElement(current_schedule_no, "LINE_TYPE_ID").text = line_type_id 
        ET.SubElement(current_schedule_no, "SCHEDULE_NO").text = schedule_no_str
        ET.SubElement(current_schedule_no, "DOCK_CODE").text = dock_code
        ET.SubElement(current_schedule_no, "DELIVERY_DUE_DATE").text = delivery_date
        ET.SubElement(current_schedule_no, "TO_DATE").text = delivery_date 
        ET.SubElement(current_schedule_no, "QUANTITY_DUE").text = qty_field
        ET.SubElement(current_schedule_no, "CUSTOMER_PO_NO").text = customer_po_no


class Segment514Processor(Segment513Processor, ISegmentProcessor):
    def process(self, segment: str, context: ConversionContext):
        if context.current_article_line is None:
            return 

        self.process_demand_fields(segment, context, 5, 125)

