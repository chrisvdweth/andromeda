import re


class EmoticonNormalizer:

    SENTIMENT_UNKNOWN = 10
    SENTIMENT_NEUTRAL = 11
    SENTIMENT_POSITIVE = 12
    SENTIMENT_NEGATIVE = 13


    EMOTICONS_GENERIC_PATTERN_TOP = '[]}{()<>'
    EMOTICONS_GENERIC_PATTERN_EYES = '.:;8BX='
    EMOTICONS_GENERIC_PATTERN_NOSES = '-=~\'^o'
    EMOTICONS_GENERIC_PATTERN_MOUTHS = ')(/\|DPp[]{}<>oO*'

    EMOTICONS_PATTERNS_ENM_MOUTH_POSITIVE = ')]}DPp>*'
    EMOTICONS_PATTERNS_ENM_MOUTH_NEGATIVE = '([{\/<|'
    EMOTICONS_PATTERNS_MNE_MOUTH_POSITIVE = '([{<'
    EMOTICONS_PATTERNS_MNE_MOUTH_NEGATIVE = ')]}\/>|'

    ORIENTATION_UNKNOWN = 100
    ORIENTATION_EYES_NOSE_MOUTH = 101
    ORIENTATION_MOUTH_NOSE_EYES = 102

    SENTIMENT_POSITIVE_STRING = "__EMOTICON+__"
    SENTIMENT_NEUTRAL_STRING = "__EMOTICON0__"
    SENTIMENT_NEGATIVE_STRING = "__EMOTICON-__"

    EMOTICON_MAPPING = { SENTIMENT_POSITIVE : SENTIMENT_POSITIVE_STRING,  SENTIMENT_NEUTRAL : SENTIMENT_NEUTRAL_STRING, SENTIMENT_NEGATIVE : SENTIMENT_NEGATIVE_STRING }


    def __init__(self):
        self.regex_pattern_eyes_nose_mouth = re.compile("([%s]?)([%s])([%s]?)([%s]+)" % tuple(map(re.escape, [EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_TOP, EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_EYES, EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_NOSES, EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_MOUTHS])))
        self.regex_pattern_mouth_nose_eyes = re.compile("([%s]+)([%s]?)([%s])([%s]?)" % tuple(map(re.escape, [EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_MOUTHS, EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_NOSES, EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_EYES, EmoticonNormalizer.EMOTICONS_GENERIC_PATTERN_TOP])))



    def tag(self, emoticon):
        orientation = self._detect_orientation(emoticon)
        #print orientation
        if orientation == EmoticonNormalizer.ORIENTATION_UNKNOWN:
            return EmoticonNormalizer.SENTIMENT_UNKNOWN, emoticon

        top, eyes, nose, mouth = self._split_emoticon(emoticon, orientation)

        mouth_sentiment, normalized_mouth_size, normalized_mouth = self._analyze_mouth(mouth, orientation)

        if orientation == EmoticonNormalizer.ORIENTATION_EYES_NOSE_MOUTH:
            emoticon_normalized = top + eyes + nose + normalized_mouth
        else:
            emoticon_normalized = normalized_mouth + nose + eyes + top

        return mouth_sentiment, emoticon_normalized



    def _split_emoticon(self, emoticon, orientation):
        if orientation == EmoticonNormalizer.ORIENTATION_EYES_NOSE_MOUTH:
            regex_pattern = self.regex_pattern_eyes_nose_mouth
        elif orientation == EmoticonNormalizer.ORIENTATION_MOUTH_NOSE_EYES:
            regex_pattern = self.regex_pattern_mouth_nose_eyes
        else:
            return None, None, None, None

        regex_match = regex_pattern.match(emoticon)
        if regex_match is None:
            return None, None, None, None

        emoticon_parts = regex_match.groups()
        #print emoticon_parts
        if len(emoticon_parts) != 4:
            return None, None, None, None

        if orientation == EmoticonNormalizer.ORIENTATION_EYES_NOSE_MOUTH:
            top = emoticon_parts[0]
            eyes = emoticon_parts[1]
            nose = emoticon_parts[2]
            mouth = emoticon_parts[3]
        elif orientation == EmoticonNormalizer.ORIENTATION_MOUTH_NOSE_EYES:
            top = emoticon_parts[3]
            eyes = emoticon_parts[2]
            nose = emoticon_parts[1]
            mouth = emoticon_parts[0]
        else:
            return (None, None, None, None)

        return  top, eyes, nose, mouth



    def _detect_orientation(self, emoticon):
        # Generic patterns
        m = self.regex_pattern_eyes_nose_mouth.search(emoticon)
        if m is not None:
            return EmoticonNormalizer.ORIENTATION_EYES_NOSE_MOUTH
        # Generic patterns (mirrored orientation)
        m = self.regex_pattern_mouth_nose_eyes.search(emoticon)
        if m is not None:
            return EmoticonNormalizer.ORIENTATION_MOUTH_NOSE_EYES

        return EmoticonNormalizer.ORIENTATION_UNKNOWN



    def _analyze_mouth(self, mouth, orientation):
        if orientation == EmoticonNormalizer.ORIENTATION_EYES_NOSE_MOUTH:
            character_list_positive = EmoticonNormalizer.EMOTICONS_PATTERNS_ENM_MOUTH_POSITIVE
            character_list_negative = EmoticonNormalizer.EMOTICONS_PATTERNS_ENM_MOUTH_NEGATIVE
        elif orientation == EmoticonNormalizer.ORIENTATION_MOUTH_NOSE_EYES:
            character_list_positive = EmoticonNormalizer.EMOTICONS_PATTERNS_MNE_MOUTH_POSITIVE
            character_list_negative = EmoticonNormalizer.EMOTICONS_PATTERNS_MNE_MOUTH_NEGATIVE
        else:
            return EmoticonNormalizer.SENTIMENT_UNKNOWN

        try:
            count_positive = sum(len(c) for c in mouth if c in character_list_positive)
        except:
            count_positive = 0
        try:
            count_negative = sum(len(c) for c in mouth if c in character_list_negative)
        except:
            count_negative = 0

        normalized_mouth_size = (self._sign(count_positive) + self._sign(count_negative))

        normalized_mouth = mouth[0] * normalized_mouth_size

        if count_positive > count_negative:
            return EmoticonNormalizer.SENTIMENT_POSITIVE, normalized_mouth_size, normalized_mouth
        elif count_positive < count_negative:
            return EmoticonNormalizer.SENTIMENT_NEGATIVE, normalized_mouth_size, normalized_mouth
        else:
            return EmoticonNormalizer.SENTIMENT_UNKNOWN, normalized_mouth_size, normalized_mouth


    def normalize(self, token, emoticon_mapping=EMOTICON_MAPPING):
        sentiment, token_normalized = self.tag(token)

        is_normalized = False
        if token != token_normalized:
            is_normalized = True

        if sentiment in [EmoticonNormalizer.SENTIMENT_POSITIVE, EmoticonNormalizer.SENTIMENT_NEUTRAL, EmoticonNormalizer.SENTIMENT_NEGATIVE]:
            return True, is_normalized, token_normalized, emoticon_mapping[sentiment]
        else:
            return False, is_normalized, token_normalized, token





    def _sign(self, number):
        """Will return 1 for positive,
        -1 for negative, and 0 for 0"""
        try:
            return number/abs(number)
        except ZeroDivisionError:
            return 0



if __name__ == "__main__":

    et = EmoticonNormalizer()

    my_mapping = { EmoticonNormalizer.SENTIMENT_POSITIVE : "EMOPOS",  EmoticonNormalizer.SENTIMENT_NEUTRAL : "EMONEU", EmoticonNormalizer.SENTIMENT_NEGATIVE : "EMONEG" }

    print '<3', '=>', et.tag('<3')
    print ':|', '=>', et.tag(':||||')
    print ':o))))', '=>', et.tag(':o))))')
    print ':-(((', '=>', et.tag(':-(((')
    print '((:', '=>', et.tag('((:')
    print 'dummy', '=>', et.tag('dummy')
    print
    print ':-)]]', '=>', et.normalize(':-)]]')
    print ':o))))', '=>', et.normalize(':o))))')
    print ':-(((', '=>', et.normalize(':-(((', emoticon_mapping=my_mapping)
    print '((:', '=>', et.normalize('((:')
    print 'dummy', '=>', et.normalize('dummy')
