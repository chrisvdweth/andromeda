import os

class UnicodeNormalizer:



    def __init__(self, mapping_file_names_list):
        self.mapping_dict = {}

        for mapping_file_name in mapping_file_names_list:
            self._add_to_dictionary(mapping_file_name)


    def _add_to_dictionary(self, mapping_file_name):
        with open(os.path.expanduser(mapping_file_name), 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue

                code, mapping = line.split('\t')
                self.mapping_dict[code.lower()] = mapping



    def normalize(self, unicode_token):
        token = unicode_token.encode('unicode-escape').replace('\\\\U', '\\U')
        if token.lower() in self.mapping_dict:
            return True, self.mapping_dict[token.lower()]
        else:
            return False, token



if __name__ == "__main__":

    et = UnicodeNormalizer(['/home/christian/work/development/git/sesame-social/somesing/data/vocabulary-files/unicode-to-ascii-mapping-emojis.txt',
                            '/home/christian/work/development/git/sesame-social/somesing/data/vocabulary-files/unicode-to-ascii-mapping.txt'])

    #print
    #print u'\U0001F49A', '=>', et.normalize('\U0001F49A')
    #print u'\U0001F621', '=>', et.normalize('\U0001F621')
    #print u'\U0001F609', '=>', et.normalize('\U0001F609')
    #print u'\U0001F613', '=>', et.normalize('\U0001F613')
    #print u'dummy', '=>', et.normalize('dummy')
