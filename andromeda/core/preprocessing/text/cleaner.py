#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import unicodedata


class Cleaner:

    def __init__(self, config):
        self._unicode_mapping ={}

        for unicode_to_ascii_mapping_file in config['mapping-files']:
            self._add_to_unicode_mapping(unicode_to_ascii_mapping_file)


    def _add_to_unicode_mapping(self, unicode_to_ascii_mapping_file):
        with open(os.path.expanduser(unicode_to_ascii_mapping_file), 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue

                code, mapping = line.split('\t')
                code = code.decode('unicode_escape')
                self._unicode_mapping[code.lower()] = mapping


    def clean(self, s):
        # Remove duplicate whitespaces
        s = re.sub(' +',' ', s)

        # Convert to unicode; otherwise normalizing somtimes fails
        try:
            s = unicode(s)
        except:
            return s

        # Replace the unicode PUNCTUATION characters with their closest ASCII representation
        try:
            s = self._asciify_unicode_characers(s)
        except:
            return s

        # Replace the unicode LETTER characters with their closest ASCII representation
        # (this method removes, e.g., unicode apostrophes; hence, has to be called at last)
        try:
            # Ignore characters that are not assinged (e.g. "Cn" category), otherwise emojies get removed
            s = ''.join([unicodedata.normalize('NFD', c) if unicodedata.category(c) not in ['Cn'] else c for c in s ])
        except:
            return s

        return s



    def _asciify_unicode_characers(self, s):
        # use these three lines to do the replacement
        rep = dict((re.escape(k), v) for k, v in self._unicode_mapping.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        return pattern.sub(lambda m: rep[re.escape(m.group(0))], s)




