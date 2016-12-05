import re

from andromeda.utils import NlpUtils


class EmotextNormalizer:

    SENTIMENT_UNKNOWN = 10
    SENTIMENT_NEUTRAL = 11
    SENTIMENT_POSITIVE = 12
    SENTIMENT_NEGATIVE = 13

    MINIMUM_PATTERN_REPETITION = 2

    PATTERN_MAPPING = { 'haha' : SENTIMENT_POSITIVE,
                        'ahah' : SENTIMENT_POSITIVE,
                        'hehe' : SENTIMENT_POSITIVE,
                        'eheh' : SENTIMENT_POSITIVE,
                        'hihi' : SENTIMENT_POSITIVE,
                        'ihih' : SENTIMENT_POSITIVE,
                        'huehue' : SENTIMENT_POSITIVE,
                        'hurrhurr' : SENTIMENT_POSITIVE,
                        'xixi' : SENTIMENT_POSITIVE,
                        'wkwk' : SENTIMENT_POSITIVE,
                        'nono' : SENTIMENT_NEGATIVE }

    EMOTEXT_MAPPING = { SENTIMENT_POSITIVE : "__EMOTEXT+__",  SENTIMENT_NEUTRAL : "__EMOTEXT0__", SENTIMENT_NEGATIVE : "__EMOTEXT-__" }


    def __init__(self, input_file_names_list):
        self.regex_pattern = re.compile(r'\b([a-z]{2,})\1{1,}[a-z]*\b', re.IGNORECASE)
        self.ignore_word_set = set()

        for input_file_name in input_file_names_list:
            self._add_words_to_dictionary(input_file_name)



    def _add_words_to_dictionary(self, input_file_name):
        with open(input_file_name, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                self.ignore_word_set.add(line)


    def normalize(self, token, emoji_mapping=EMOTEXT_MAPPING):
        token_normalized = self._normalize(token)

        if token_normalized in EmotextNormalizer.PATTERN_MAPPING:
            sentiment = EmotextNormalizer.PATTERN_MAPPING[token_normalized]
        else:
            sentiment = EmotextNormalizer.SENTIMENT_UNKNOWN

        token_normalized = NlpUtils.match_word_capitalization(token, token_normalized)

        if sentiment in [EmotextNormalizer.SENTIMENT_POSITIVE, EmotextNormalizer.SENTIMENT_NEUTRAL, EmotextNormalizer.SENTIMENT_NEGATIVE]:
            return True, token_normalized, emoji_mapping[sentiment]
        else:
            return False, token_normalized, token



    def _normalize(self, token):
        if token.lower() in self.ignore_word_set:
            return token

        token_minimized = NlpUtils.replace_repeated_letters(token, 2, 1)

        results = re.findall(self.regex_pattern, token_minimized)

        if len(results) == 0:
            return token

        return self._normalize_full(results[0], token)


    def _normalize_full(self, token, original_token):
        results = re.findall(self.regex_pattern, token)

        if len(results) == 0:
            return EmotextNormalizer.MINIMUM_PATTERN_REPETITION*token.lower()

        return self._normalize_full(results[0], original_token)









if __name__ == "__main__":

    et = EmotextNormalizer(['/home/christian/data/datasets/english-words/english-lowercase.text'])

    my_mapping = { EmotextNormalizer.SENTIMENT_POSITIVE : "EMOPOS",  EmotextNormalizer.SENTIMENT_NEUTRAL : "EMONEU", EmotextNormalizer.SENTIMENT_NEGATIVE : "EMONEG" }



    print
    print 'Hahaha', '=>', et.normalize('Hahaha')
    print 'heeeeheeee', '=>', et.normalize('heeeeeheeeeeee')
    print 'hihi', '=>', et.normalize('hihi')
    print 'xixixixi', '=>', et.normalize('xixixixi')
    print 'huehue', '=>', et.normalize('huehue')
    print 'hurrhurr', '=>', et.normalize('hurrhurr')
    print 'dummy', '=>', et.normalize('dummy')
    print 'banana', '=>', et.normalize('banana')
