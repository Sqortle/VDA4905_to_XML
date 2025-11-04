# vda4905.py
import xml.etree.ElementTree as ET
import os
from VDADataParser import VDADataParser
from XMLFormatter import XMLFormatter  # Singleton
from FileHandler import FileHandler  # Singleton
from ConversionContext import ConversionContext
from SegmentProcessorFactory import SegmentProcessorFactory  # Factory

# Burası güncellenmeli
VDA_INPUT_FILENAME = "/Users/mirza/Documents/vda_input.txt"
VDA_4905_message = ""


class VDA4905Converter:
    def __init__(self, VDA_4905_message):
        self.VDA_4905_message = VDA_4905_message

        self.formatter = XMLFormatter()
        self.file_handler = FileHandler()

        self.processor_factory = SegmentProcessorFactory()

        self.parser = VDADataParser()

    def convert_and_write_multiple_files(self, VDA_4905_message, base_path):
        segments = [line.strip() for line in VDA_4905_message.split("\n") if line.strip()]

        header_511, ean_loc, grouped_schedules = self.parser.group_segments(segments)

        if not header_511:
            print("Error: 511 header segment is missing or null. Cannot proceed with conversion.")
            return []

        output_files = []
        schedule_no = 0

        # Eğer çıkış yolu yoksa oluştur
        os.makedirs(base_path, exist_ok=True)

        # ... (Kodu buradan devam ediyor)

        for schedule_group in grouped_schedules:
            try:
                schedule_no += 1
                schedule_no_str = str(schedule_no)

                # XML yapısını oluşturma
                root = ET.Element("SCHEDULES")
                schedule = ET.SubElement(root, "SCHEDULE")

                ET.SubElement(schedule, "SUPP_SCHED_TYPE").text = "PLAN"

                # ARTICLE_LINES ve DEMAND_LINES elementlerini, processor'lar kullanacağı için başta OLUŞTURUYORUZ
                article_lines_el = ET.SubElement(schedule, "ARTICLE_LINES")
                demand_lines_el = ET.SubElement(schedule, "DEMAND_LINES")

                context = ConversionContext(
                    schedule_no_str, None, ean_loc,
                    schedule, article_lines_el, demand_lines_el
                )

                # Segment 511 işleme (Header bilgileri buraya ekleniyor: VENDOR_NO, VALID_FROM, vb.)
                processor_511 = self.processor_factory.get_processor("511")
                if processor_511:
                    processor_511.process(header_511, context)

                # VALID_FROM değerini context'e ekledikten sonra alıyoruz
                context.valid_from_date = schedule.find("VALID_FROM").text

                for segment in schedule_group:
                    tag = segment[0:3]

                    # Factory ile işlemci nesnesi oluşturma
                    processor = self.processor_factory.get_processor(tag)

                    if processor:
                        processor.process(segment, context)

                # VALID_UNTIL (Son Teslimat Tarihi) Ekleme Mantığı
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

                # XML Hiyerarşisini düzgün şekilde biçimlendirme:
                # 1. Elementleri mevcut konumlarından çıkarıyoruz
                schedule.remove(article_lines_el)
                schedule.remove(demand_lines_el)

                # 2. Elementleri en sona tekrar ekliyoruz
                schedule.append(article_lines_el)
                schedule.append(demand_lines_el)
                # ------------------------------------------------

                # XML'i biçimlendir ve dosyaya yaz
                self.formatter.indent(root)
                tree = ET.ElementTree(root)

                result = self.file_handler.write_file(
                    tree, schedule_no_str, ean_loc, context.dock_code, base_path
                )
                if result:
                    output_files.append(result)

            except Exception as e:
                print(f"Critical Error processing schedule group #{schedule_no_str}: {e}. Skipping this schedule.")
                # Hata durumunda bu programı atlar ve bir sonrakine geçer.

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
        # Burası güncellenmeli
        base_output_path = "/Users/mirza/PycharmProjects/VDA4905/VDA4905_XML"

        converter = VDA4905Converter(VDA_4905_message)
        created_files = converter.convert_and_write_multiple_files(VDA_4905_message, base_path=base_output_path)

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