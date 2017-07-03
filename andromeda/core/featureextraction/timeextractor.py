import re
import os
import json
import falcon

#from natty import DateParser
from andromeda.config import ConfigReader

class TimeExtractor:

    KEYWORDS_SET__NOW = {'live', 'now', 'right now', 'just now', 'current', 'currently',
                         'at the moment', 'at this moment', 'at this moment', 'at that moment',
                         'at present', 'for the time being',
                         'still'}

    KEYWORDS_SET__LATEST = {'latest', 'recent', 'most recent', 'newest', 'most novel'}

    KEYWORDS_SET__VAGUE = {'morning', 'afternoon', 'evening', 'night',
                           'early morning', 'early afternoon', 'early evening', 'early night',
                           'late morning', 'late afternoon', 'late evening', 'late night',
                           'weekend'}

    KEYWORDS_SET__WEEKDAYS = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    KEYWORDS_SET__WEEKDAYS_SHORT = {'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'}

    KEYWORDS_SET = KEYWORDS_SET__NOW.union(KEYWORDS_SET__LATEST).union(KEYWORDS_SET__VAGUE).union(KEYWORDS_SET__WEEKDAYS)


    def __init__(self):
        self.config = ConfigReader(os.path.join(ConfigReader.CONFIG_DIR, 'timeextractor.yaml')).data
        self.time_references_mapping_dict = {}
        self._time_reference_mappings(self.config['time-references-mapping-files'])

        self.pattern = re.compile(r'\b(%s)\b' % ('|'.join(list(TimeExtractor.KEYWORDS_SET))), re.IGNORECASE)




    def _time_reference_mappings(self, mapping_file_names_list):
        self.time_references_mapping_dict = {}
        for mapping_file_name in mapping_file_names_list:
            with open(os.path.expanduser(mapping_file_name), 'r') as f:
                for line in f:
                    # Remove all leading a trailing whitespaces
                    line = line.strip()
                    # Ignore commented and empty lines
                    if line.startswith('#') or line == '':
                        continue

                    source, target = line.split('\t')
                    self.time_references_mapping_dict[source] = target



    def process(self, s, time_format_str=None):
        s = self._preprocess_string(s)

        s = self._handle_day(s)

        # Preprocess string by replacing some "non-standard" words and phrases into "standard" ones
        # (i.e., words or phrases that Natty handles out of the box)
        s_normalized = self._multiple_replace(self.time_references_mapping_dict, s)

        # Evaluate Natty over string
        time_struct_list = self._process_natty(s_normalized)

        if time_struct_list is None:
            time_struct_list = []

        # Convert datetime object ot human-readable string if specified
        if time_format_str is not None:
            time_struct_list = [ time_struct.strftime(time_format_str) for time_struct in time_struct_list]

        # Match all predefined keywords
        matched_keywords_list = list(self._process_own(s))

        # Return pair of time_structs and matched keywords
        return time_struct_list, matched_keywords_list


    def _preprocess_string(self, s):
        s = re.sub(r"(\b[0-9]*1)(st\b)", r"\1", s)
        s = re.sub(r"(\b[0-9]*2)(nd\b)", r"\1", s)
        s = re.sub(r"(\b[0-9]*3)(rd\b)", r"\1", s)
        s = re.sub(r"(\b[0-9]*[0-9])(th\b)", r"\1", s)
        s = re.sub(r"(\b[0-9]+)(d\b)", r"\1 days", s)           # "12d" => "12 days"
        s = re.sub(r"(\b[0-9]+)(h\b)", r"\1 hours", s)          # "12h" => "12 hours"
        s = re.sub(r"(\b[0-9]+)(m\b)", r"\1 minutes", s)        # "12m" => "12 minutes"
        s = re.sub(r"(\b[0-9]+)(s\b)", r"\1 seconds", s)        # "12s" => "12 seconds"
        s = re.sub(r"(\b[0-9]+)([a-zA-Z]+\b)", r"\1 \2", s)     # "12xxx" => "12 xxx"
        return s


    def _handle_day(self, s):
        weekdays_str = '|'.join(TimeExtractor.KEYWORDS_SET__WEEKDAYS.union(TimeExtractor.KEYWORDS_SET__WEEKDAYS_SHORT))

        p = re.compile(r"(^|\b[a-zA-Z]+\b )\b(%s)\b" %weekdays_str)
        offset = 0
        for m in p.finditer(s):
            prec_word = s[m.start(1)+offset : m.end(1)+offset].strip()
            if prec_word not in {'last', 'past', 'coming', 'next'}:
                s = ' '.join(s[:m.end(1)+offset].split() + ['past'] + s[m.start(2)+offset:m.end(2)+offset].split() + s[m.end(2)+offset:].split())

                offset += len('past')+1 # +1 because of additional whitespace

        return s


    def _process_natty(self, s):
        #dp = DateParser(s)
        #return dp.result()
        return ""


    def _process_own(self, s):
        matched_keywords_list = []
        print s
        for m in self.pattern.finditer(s):
            matched_word = s[ m.span()[0] : m.span()[1] ]
            matched_keywords_list.append(matched_word)
        return set(matched_keywords_list)


    def _multiple_replace(self, dictionary, text):
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(\b%s\b)" % "|".join(map(re.escape, dictionary.keys())), re.IGNORECASE)

        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: dictionary[mo.string[mo.start():mo.end()].lower()], text)


class TimeExtractorApiResource(object):

    def __init__(self):
        self.time_extractor = TimeExtractor()


    def on_get(self, req, resp):
        query = req.get_param('query') or ''
        time_format_str = req.get_param('format') or None

        try:
            query = query.decode('unicode-escape')
        except Exception, e:
            pass # Do nothing in case the string is already in unicode

        try:
            time_format_str = time_format_str.decode('unicode-escape')
        except Exception, e:
            time_format_str = None

        time_struct_list, matched_keywords_list = self.time_extractor.process(query, time_format_str=time_format_str)

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps( { "structs" : time_struct_list, "keywords" : matched_keywords_list } )








if __name__ == '__main__':

    te = TimeExtractor()


    examples_list = ['brotzeit vivocity 11th 100th 1st 13th 3rd']

    for s in examples_list:
        print te.process(s, time_format_str='%A, %B %d, %Y - %H:%M:%S')
        #print te.process(s)
