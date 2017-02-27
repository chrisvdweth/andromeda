import os
import re
from andromeda.config import Constants
from andromeda.util import NlpUtil


class EmotextNormalizer:

    def __init__(self, input_file_names_list):
        self.regex_pattern = re.compile(r'\b([a-z]{2,})\1{1,}[a-z]*\b', re.IGNORECASE)
        self.ignore_word_set = set()

        for input_file_name in input_file_names_list:
            self._add_words_to_dictionary(input_file_name)



    def _add_words_to_dictionary(self, input_file_name):
        with open(os.path.expanduser(input_file_name), 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                self.ignore_word_set.add(line)


    def normalize(self, token, emoji_mapping=Constants.EMOTEXT_NORMALIZER__EMOTEXT_MAPPING):
        token_normalized = self._normalize(token)

        if token_normalized in Constants.EMOTEXT_NORMALIZER__PATTERN_MAPPING:
            sentiment = Constants.EMOTEXT_NORMALIZER__PATTERN_MAPPING[token_normalized]
        else:
            sentiment = Constants.EMOTEXT_NORMALIZER__SENTIMENT_UNKNOWN

        token_normalized = NlpUtil.match_word_capitalization(token, token_normalized)

        if sentiment in [Constants.EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE, Constants.EMOTEXT_NORMALIZER__SENTIMENT_NEUTRAL, Constants.EMOTEXT_NORMALIZER__SENTIMENT_NEGATIVE]:
            return True, token_normalized, emoji_mapping[sentiment]
        else:
            return False, token_normalized, token



    def _normalize(self, token):
        if token.lower() in self.ignore_word_set:
            return token

        token_minimized = NlpUtil.replace_repeated_letters(token, 2, 1)

        results = re.findall(self.regex_pattern, token_minimized)

        if len(results) == 0:
            return token

        return self._normalize_full(results[0], token)


    def _normalize_full(self, token, original_token):
        results = re.findall(self.regex_pattern, token)

        if len(results) == 0:
            return Constants.EMOTEXT_NORMALIZER__MINIMUM_PATTERN_REPETITION*token.lower()

        return self._normalize_full(results[0], original_token)









if __name__ == "__main__":

    et = EmotextNormalizer(['/home/christian/work/development/git/sesame-social/somesing/data/vocabulary-files/english-lowercase.txt'])

    my_mapping = { Constants.EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE : "EMOPOS",  Constants.EMOTEXT_NORMALIZER__SENTIMENT_NEUTRAL : "EMONEU", Constants.EMOTEXT_NORMALIZER__SENTIMENT_NEGATIVE : "EMONEG" }



    #print
    #print 'Hahaha', '=>', et.normalize('Hahaha')
    #print 'heeeeheeee', '=>', et.normalize('heeeeeheeeeeee')
    #print 'hihi', '=>', et.normalize('hihi')
    #print 'xixixixi', '=>', et.normalize('xixixixi')
    #print 'huehue', '=>', et.normalize('huehue')
    #print 'hurrhurr', '=>', et.normalize('hurrhurr')
    #print 'dummy', '=>', et.normalize('dummy')
    #print 'banana', '=>', et.normalize('banana')
