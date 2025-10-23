import xml.etree.ElementTree as ET
from datetime import datetime

from VDADataParser import VDADataParser 
from XMLFormatter import XMLFormatter
from FileHandler import FileHandler
from ConversionContext import ConversionContext 
from SegmentProcessors import PROCESSORS

VDA_INPUT_FILENAME = "/Users/mirza/Documents/vda_input.txt"
VDA_4905_message = ""

class VDA4905Converter:
    def __init__(self, VDA_4905_message):
        self.VDA_4905_message = VDA_4905_message
        
        self.parser = VDADataParser()
        self.formatter = XMLFormatter() 
        self.file_handler = FileHandler()

    def convert_and_write_multiple_files(self, VDA_4905_message, base_path): 
        segments = [line.strip() for line in VDA_4905_message.split("\n") if line.strip()]
        
        header_511, ean_loc, grouped_schedules = self.parser.group_segments(segments)

        if not header_511:
            print("Error: 511 header segment is missing or null. Cannot proceed with conversion.")
            return []

        output_files = []
        schedule_no = 0

        for schedule_group in grouped_schedules:
            schedule_no += 1
            schedule_no_str = str(schedule_no)
            
            root = ET.Element("SCHEDULES")
            schedules_el = ET.SubElement(root, "SCHEDULES")
            schedule = ET.SubElement(schedules_el, "SCHEDULE")
            
            ET.SubElement(schedule, "SUPP_SCHED_TYPE").text = "PLAN"

            context = ConversionContext(
                schedule_no_str, None, ean_loc, 
                schedule, None, None # Artık Optional[ET.Element] olarak kabul edilecek
            )

            PROCESSORS["511"].process(header_511, context)
            context.valid_from_date = schedule.find("VALID_FROM").text 

            article_lines_el = ET.SubElement(schedule, "ARTICLE_LINES")
            demand_lines_el = ET.SubElement(schedule, "DEMAND_LINES")

            context.article_lines_el = article_lines_el
            context.demand_lines_el = demand_lines_el

            for segment in schedule_group:
                tag = segment[0:3]
                
                if tag in PROCESSORS:
                    processor = PROCESSORS[tag]

                    processor.process(segment, context)

            last_delivery_date = context.last_delivery_date
            
            if last_delivery_date:
                insert_index = -1
                for i, child in enumerate(schedule):
                    if child.tag == "VALID_FROM":
                        insert_index = i + 1
                        break
                
                if insert_index != -1:
                    new_element = ET.Element("VALID_UNTIL")
                    new_element.text = last_delivery_date
                    schedule.insert(insert_index, new_element)

            self.formatter.indent(root) 
            tree = ET.ElementTree(root)
            
            result = self.file_handler.write_file(
                tree, schedule_no_str, ean_loc, context.dock_code, base_path
            )
            if result:
                output_files.append(result)
                
        return output_files


try:
    with open(VDA_INPUT_FILENAME, 'r') as f:
        VDA_4905_message = f.read()

except FileNotFoundError:
    VDA_4905_message = ""
    print(f"Error: Input file ('{VDA_INPUT_FILENAME}') was not found. Please ensure the file exists.")
except Exception as e:
    VDA_4905_message = ""
    print(f"An unexpected error occurred while reading the file: {e}")


def main():
    global VDA_4905_message 

    if not VDA_4905_message:
        return

    try:
        converter = VDA4905Converter(VDA_4905_message)
        created_files = converter.convert_and_write_multiple_files(VDA_4905_message, base_path="/Users/mirza/PycharmProjects/VDA4905/VDA4905_XML")
        
        if created_files:
            print("\nXML conversion successful.")
            print("Generated files:")
            for f in created_files:
                print(f"- {f}")
        else:
            print("\nNo valid schedules were processed, or 511 header is missing.")

    except Exception as e:
        print(f"\nAn unhandled error occurred during processing: {e}")

if __name__ == "__main__":
    main()
