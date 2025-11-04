
class VDADataParser:
    def __init__(self):
        pass

    def group_segments(self, segments):
        grouped_schedules = []
        current_schedule_group = []
        
        header_511 = None
        ean_loc = None

        for segment in segments:
            tag = segment[0:3]
            if tag == "511":
                header_511 = segment
            
            if tag == "512":
                if current_schedule_group:
                    grouped_schedules.append(current_schedule_group)
                current_schedule_group = [segment] 
                if ean_loc is None:
                    ean_loc = segment[5:8].strip()
            
            elif tag in ["513", "514", "517"] and current_schedule_group:
                current_schedule_group.append(segment)

        if current_schedule_group:
            grouped_schedules.append(current_schedule_group)
            
        return header_511, ean_loc, grouped_schedules