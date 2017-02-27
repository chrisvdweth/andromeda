from andromeda.core.featureextraction import TimeExtractor

class TimeExtractionHandler:

    def __init__(self):
        self.time_extractor = TimeExtractor()


    def process(self, query_str, time_format_str):
        time_struct_list, matched_keywords_list = self.time_extractor.process(query_str, time_format_str)
        return { 'structs' : time_struct_list, 'keywords' : matched_keywords_list }


