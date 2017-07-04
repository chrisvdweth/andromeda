


class Constants:

    def __init__(self):
        pass


    ##########################################################################################
    ##########################################################################################
    ##
    ## TOKENIZER (andromenda.core.preprocessing.text.tokenizer)
    ##
    ##########################################################################################
    ##########################################################################################
    TOKENIZER__PUNCTUATION_MARKS__TERMINAL_POINTS = '.!?'
    TOKENIZER__PUNCTUATION_MARKS__PAUSING_POINTS = ',:;'
    TOKENIZER__EMOTICONS_FIXED_PATTERNS = '^^ <3 </3'.split()
    TOKENIZER__EMOTICONS_GENERIC_PATTERN_TOP = '[]}{()<>'
    TOKENIZER__EMOTICONS_GENERIC_PATTERN_EYES = '.:;8BX='
    TOKENIZER__EMOTICONS_GENERIC_PATTERN_NOSES = '-=~\'^o'
    TOKENIZER__EMOTICONS_GENERIC_PATTERN_MOUTHS = ')(/\|DPp[]{}<>oO*'
    TOKENIZER__EMOTEXTS_CORE_PATTERNS_LIST = ['ha', 'ah', 'he', 'eh', 'hi', 'ih', 'ho', 'hu', 'hue']
    TOKENIZER__TOKEN_CLASS__UNKNOWN = 0
    TOKENIZER__TOKEN_CLASS__WHITESPACE = 1
    TOKENIZER__TOKEN_CLASS__CHARACTER_SUBSTRING = 2
    TOKENIZER__TOKEN_CLASS__ALPHANUM = 10
    TOKENIZER__TOKEN_CLASS__ALPHANUM_NEGATION_ABBREVIATION = 11
    TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS = 20
    TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED = 21
    TOKENIZER__TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS = 30
    TOKENIZER__TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS_REPEATED = 31
    TOKENIZER__TOKEN_CLASS__URL = 60
    TOKENIZER__TOKEN_CLASS__EMAIL = 65
    TOKENIZER__TOKEN_CLASS__SPECIAL_TERM_USER = 70
    TOKENIZER__TOKEN_CLASS__SPECIAL_TERM_TOPIC = 71
    TOKENIZER__TOKEN_CLASS__NUMBER = 80
    TOKENIZER__TOKEN_CLASS__TIME_FORMAT = 85
    TOKENIZER__TOKEN_CLASS__EMOTICON = 90
    TOKENIZER__TOKEN_CLASS__HTML_ENTITY = 150
    TOKENIZER__TOKEN_CLASS__UNICODE = 160
    TOKENIZER__TOKEN_CLASS__NON_ASCII = 200
    TOKENIZER__TOKEN_CLASS__QUOTE_OPEN = 301
    TOKENIZER__TOKEN_CLASS__QUOTE_CLOSE = 302
    TOKENIZER__TOKEN_CLASS__BRACKET_OPEN = 311
    TOKENIZER__TOKEN_CLASS__BRACKET_CLOSE = 312
    TOKENIZER__TOKEN_FEATURE__BASE = 'core'
    TOKENIZER__TOKEN_FEATURE__TOKEN = 'token'
    TOKENIZER__TOKEN_FEATURE__CLASS = 'class'
    TOKENIZER__TOKEN_FEATURE__FIRST_CHARACTER_INDEX = 'char_idx'
    TOKENIZER__TOKEN_FEATURE__CHARACTER_COUNT = 'char_count'


    ##########################################################################################
    ##########################################################################################
    ##
    ## POSTAGGER (andromenda.core.preprocessing.text.postagger)
    ##
    ##########################################################################################
    ##########################################################################################
    POSTAGGER__POS_TAG__COMMON_NOUN = "N"
    POSTAGGER__POS_TAG__PRONOUN = "O"
    POSTAGGER__POS_TAG__NOMINAL_POSSESSIVE = "S"
    POSTAGGER__POS_TAG__PROPER_NOUN = "^"
    POSTAGGER__POS_TAG__PROPER_NOUN_WITH_POSSESSIVE = "Z"
    POSTAGGER__POS_TAG__NOMINAL_WITH_VERBAL = "L"
    POSTAGGER__POS_TAG__PROPER_NOUN_WITH_VERBAL = "M"
    POSTAGGER__POS_TAG__VERB_INCL_COPULA_AUX = "V"
    POSTAGGER__POS_TAG__ADJECTIVE = "A"
    POSTAGGER__POS_TAG__ADVERB = "R"
    POSTAGGER__POS_TAG__INTERJECTION = "!"
    POSTAGGER__POS_TAG__DETERMINER = "D"
    POSTAGGER__POS_TAG__PRE_POST_POSITION = "P"
    POSTAGGER__POS_TAG__COORDINATING_CONJUNCTION = "&"
    POSTAGGER__POS_TAG__VERB_PARTICLE = "T"
    POSTAGGER__POS_TAG__EXISTENTIAL = "X"
    POSTAGGER__POS_TAG__EXISTENTIAL_WITH_VERBAL = "Y"
    POSTAGGER__POS_TAG__HASHTAG = "#"
    POSTAGGER__POS_TAG__AT_MENTION = "@"
    POSTAGGER__POS_TAG__DISCOURSE_MARKER = "~"
    POSTAGGER__POS_TAG__URL_OR_EMAIL = "U"
    POSTAGGER__POS_TAG__EMOTICON = "E"
    POSTAGGER__POS_TAG__NUMERAL = "$"
    POSTAGGER__POS_TAG__PUNCTUATION_PAUSING = ","
    POSTAGGER__POS_TAG__PUNCTUATION_TERMINAL = "."
    POSTAGGER__POS_TAG__OTHER_ABBREVIATIONS = "G"
    POSTAGGER__POS_TAG__UNKNOWN = "?"
    POSTAGGER__POS_TAG__WILDCARD = "W"
    POSTAGGER__TOKEN_FEATURE__BASE = 'core'
    POSTAGGER__TOKEN_FEATURE__POS_TAG = 'pos_tag'


    ##########################################################################################
    ##########################################################################################
    ##
    ## SEGMENTER (andromenda.core.preprocessing.text.segmenter)
    ##
    ##########################################################################################
    ##########################################################################################
    SEGMENTER__TOKEN_FEATURE_CLASSES__SEGMENTATION_SEPARATORS = [TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS,
                                                                 TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED,
                                                                 TOKENIZER__TOKEN_CLASS__NON_ASCII,
                                                                 TOKENIZER__TOKEN_CLASS__EMOTICON,
                                                                 TOKENIZER__TOKEN_CLASS__CHARACTER_SUBSTRING,
                                                                 TOKENIZER__TOKEN_CLASS__EMAIL,
                                                                 TOKENIZER__TOKEN_CLASS__URL,
                                                                 TOKENIZER__TOKEN_CLASS__HTML_ENTITY,
                                                                 TOKENIZER__TOKEN_CLASS__UNICODE,
                                                                 TOKENIZER__TOKEN_CLASS__UNKNOWN]
    SEGMENTER__TOKEN_FEATURE_CLASSES__INDIVIDUAL_SEGMENTS = [TOKENIZER__TOKEN_CLASS__NON_ASCII,
                                                             TOKENIZER__TOKEN_CLASS__EMOTICON,
                                                             TOKENIZER__TOKEN_CLASS__CHARACTER_SUBSTRING,
                                                             TOKENIZER__TOKEN_CLASS__EMAIL,
                                                             TOKENIZER__TOKEN_CLASS__URL,
                                                             TOKENIZER__TOKEN_CLASS__HTML_ENTITY,
                                                             TOKENIZER__TOKEN_CLASS__UNICODE,
                                                             TOKENIZER__TOKEN_CLASS__UNKNOWN]
    SEGMENTER__TOKEN_FEATURE__BASE = 'core'
    SEGMENTER__TOKEN_FEATURE__SEGMENT_NUMBER = 'segment_nr'


    ##########################################################################################
    ##########################################################################################
    ##
    ## POSTAGGER (andromenda.core.preprocessing.text.normalizer)
    ##
    ##########################################################################################
    ##########################################################################################
    NORMALIZER__MIN_LEVENSHTEIN_RATIO = 0.7
    NORMALIZER__TOKEN_CLASS_LIST__ALPHANUM = [TOKENIZER__TOKEN_CLASS__ALPHANUM,
                                              TOKENIZER__TOKEN_CLASS__ALPHANUM_NEGATION_ABBREVIATION]
    NORMALIZER__TOKEN_FEATURE__BASE = 'core'
    NORMALIZER__TOKEN_FEATURE__NORMALIZED = 'normalized'
    NORMALIZER__TOKEN_FEATURE__DESLANGED = 'deslanged'
    NORMALIZER__TOKEN_FEATURE__STANDARDIZED = 'standardized'
    NORMALIZER__TOKEN_FEATURE__SEGMENTED = 'segmented'

    ##
    ## EmoticonNormalizer
    ##
    EMOTICON_NORMALIZER__SENTIMENT_UNKNOWN = 10
    EMOTICON_NORMALIZER__SENTIMENT_NEUTRAL = 11
    EMOTICON_NORMALIZER__SENTIMENT_POSITIVE = 12
    EMOTICON_NORMALIZER__SENTIMENT_NEGATIVE = 13
    EMOTICON_NORMALIZER__EMOTICONS_GENERIC_PATTERN_TOP = '[]}{()<>'
    EMOTICON_NORMALIZER__EMOTICONS_GENERIC_PATTERN_EYES = '.:;8BX='
    EMOTICON_NORMALIZER__EMOTICONS_GENERIC_PATTERN_NOSES = '-=~\'^o'
    EMOTICON_NORMALIZER__EMOTICONS_GENERIC_PATTERN_MOUTHS = ')(/\|DPp[]{}<>oO*'
    EMOTICON_NORMALIZER__EMOTICONS_PATTERNS_ENM_MOUTH_POSITIVE = ')]}DPp>*'
    EMOTICON_NORMALIZER__EMOTICONS_PATTERNS_ENM_MOUTH_NEGATIVE = '([{\/<|'
    EMOTICON_NORMALIZER__EMOTICONS_PATTERNS_MNE_MOUTH_POSITIVE = '([{<'
    EMOTICON_NORMALIZER__EMOTICONS_PATTERNS_MNE_MOUTH_NEGATIVE = ')]}\/>|'
    EMOTICON_NORMALIZER__ORIENTATION_UNKNOWN = 100
    EMOTICON_NORMALIZER__ORIENTATION_EYES_NOSE_MOUTH = 101
    EMOTICON_NORMALIZER__ORIENTATION_MOUTH_NOSE_EYES = 102
    EMOTICON_NORMALIZER__SENTIMENT_POSITIVE_STRING = "__EMOTICON+__"
    EMOTICON_NORMALIZER__SENTIMENT_NEUTRAL_STRING = "__EMOTICON0__"
    EMOTICON_NORMALIZER__SENTIMENT_NEGATIVE_STRING = "__EMOTICON-__"
    EMOTICON_NORMALIZER__EMOTICON_MAPPING = { EMOTICON_NORMALIZER__SENTIMENT_POSITIVE : EMOTICON_NORMALIZER__SENTIMENT_POSITIVE_STRING,
                                              EMOTICON_NORMALIZER__SENTIMENT_NEUTRAL : EMOTICON_NORMALIZER__SENTIMENT_NEUTRAL_STRING,
                                              EMOTICON_NORMALIZER__SENTIMENT_NEGATIVE : EMOTICON_NORMALIZER__SENTIMENT_NEGATIVE_STRING }

    EMOTEXT_NORMALIZER__SENTIMENT_UNKNOWN = 10
    EMOTEXT_NORMALIZER__SENTIMENT_NEUTRAL = 11
    EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE = 12
    EMOTEXT_NORMALIZER__SENTIMENT_NEGATIVE = 13
    EMOTEXT_NORMALIZER__MINIMUM_PATTERN_REPETITION = 2
    EMOTEXT_NORMALIZER__PATTERN_MAPPING = { 'haha' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'ahah' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'hehe' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'eheh' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'hihi' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'ihih' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'huehue' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'hurrhurr' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'xixi' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'wkwk' : EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE,
                                            'nono' : EMOTEXT_NORMALIZER__SENTIMENT_NEGATIVE }
    EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE_STRING = "__EMOTEXT+__"
    EMOTEXT_NORMALIZER__SENTIMENT_NEUTRAL_STRING = "__EMOTEXT0__"
    EMOTEXT_NORMALIZER__SENTIMENT_NEGATIVE_STRING = "__EMOTEXT-__"
    EMOTEXT_NORMALIZER__EMOTEXT_MAPPING = { EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE : "__EMOTEXT+__",
                                            EMOTEXT_NORMALIZER__SENTIMENT_NEUTRAL : "__EMOTEXT0__",
                                            EMOTEXT_NORMALIZER__SENTIMENT_NEGATIVE : "__EMOTEXT-__" }


    UNICODE_NORMALIZER__SENTIMENT_POSITIVE_STRING = "__EMOJI+__"
    UNICODE_NORMALIZER__SENTIMENT_NEUTRAL_STRING = "__EMOJI0__"
    UNICODE_NORMALIZER__SENTIMENT_NEGATIVE_STRING = "__EMOJI-__"

    ##########################################################################################
    ##########################################################################################
    ##
    ##
    ##
    ##########################################################################################
    ##########################################################################################
    LIFE__TOKEN_FEATURE__BASE = 'life'

    LIFE__ANP = 'anp'
    LIFE__ALL_CAPS = 'allcaps'
    LIFE__QUOTED = 'quoted'
    LIFE__NEGATION = 'negated'
    LIFE__TAG = 'tag'

    LIFE__NEGATED_WORD_TOKEN_CLASSES = [TOKENIZER__TOKEN_CLASS__ALPHANUM]

    LIFE__NEGATION_BOUNDARY_POS_TAGS = [POSTAGGER__POS_TAG__INTERJECTION,
                                        POSTAGGER__POS_TAG__URL_OR_EMAIL]

    LIFE__NEGATION_MAX_SCOPE_SIZE = 3

    LIFE__NEGATION_BOUNDARY_TOKEN_CLASSES = [TOKENIZER__TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS,
                                       TOKENIZER__TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS_REPEATED,
                                       TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS,
                                       TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED,
                                       TOKENIZER__TOKEN_CLASS__EMAIL,
                                       TOKENIZER__TOKEN_CLASS__EMOTICON,
                                       TOKENIZER__TOKEN_CLASS__UNICODE,
                                       TOKENIZER__TOKEN_CLASS__URL,
                                       TOKENIZER__TOKEN_CLASS__HTML_ENTITY,
                                       TOKENIZER__TOKEN_CLASS__NON_ASCII,
                                       TOKENIZER__TOKEN_CLASS__NUMBER,
                                       TOKENIZER__TOKEN_CLASS__SPECIAL_TERM_TOPIC,
                                       TOKENIZER__TOKEN_CLASS__SPECIAL_TERM_USER,
                                       TOKENIZER__TOKEN_CLASS__TIME_FORMAT,
                                       TOKENIZER__TOKEN_CLASS__UNKNOWN]
    LIFE__NEGATION_BOUNDARY_TOKEN_EXCEPTION_CLASSES = [TOKENIZER__TOKEN_CLASS__QUOTE_CLOSE,
                                                 TOKENIZER__TOKEN_CLASS__QUOTE_OPEN]
    #LIFE__NEGATION_BOUNDARY_TOKENS = ['but', 'unless']
    LIFE__NEGATION_RULE__NEGATION_WORD_TOKEN_CLASSES = ['neg']
    LIFE__ALL_CAPS_RULE__VALID_TOKEN_CLASSES = [TOKENIZER__TOKEN_CLASS__ALPHANUM,
                                                TOKENIZER__TOKEN_CLASS__ALPHANUM_NEGATION_ABBREVIATION]
    LIFE__ANP_RULE__POS_WILDCARD_TOKEN_CLASSES = [TOKENIZER__TOKEN_CLASS__QUOTE_OPEN,
                                                  TOKENIZER__TOKEN_CLASS__QUOTE_CLOSE],
    LIFE__ANP_RULE__POS_UNKNOWN_TOKEN_CLASSES = [TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS,
                                                 TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED]
    LIFE__WORD_TYPE__ADJECTIVE__NORMAL = 1
    LIFE__WORD_TYPE__ADJECTIVE__COMPARATIVE = 2
    LIFE__WORD_TYPE__ADJECTIVE__SUPERLATIVE = 3
    LIFE__WORD_TYPE__ADJECTIVE__RELEVANCE = 5
    LIFE__QUOTATION__QUOTED_WORD = 1
    LIFE__QUOTATION__QUOTED_PHRASE = 2



    SENTIGRADE__TOKEN_FEATURE__BASE = 'sentigrade'
    SENTIGRADE__TOKEN_SENTIMENT_SCORE = 'score'

