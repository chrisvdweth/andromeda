from andromeda.core.preprocessing.text.tokenizer import Tokenizer
from andromeda.core.preprocessing.text.normalizer import Normalizer
from andromeda.core.preprocessing.text.postagger import POSTagger



class LifeConstants:

    TOKEN_FEATURE__BASE = 'life'

    LIFE__ANP = 'anp'
    LIFE__ALL_CAPS = 'allcaps'
    LIFE__QUOTED = 'quoted'
    LIFE__NEGATION = 'negated'
    LIFE__TAG = 'tag'



    NEGATED_WORD_TOKEN_CLASSES = [Tokenizer.TOKEN_CLASS__ALPHANUM]

    NEGATION_BOUNDARY_POS_TAGS = [POSTagger.POS_TAG__INTERJECTION,
                                  POSTagger.POS_TAG__URL_OR_EMAIL]

    NEGATION_MAX_SCOPE_SIZE = 3

    NEGATION_BOUNDARY_TOKEN_CLASSES = [Tokenizer.TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS,
                                       Tokenizer.TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS_REPEATED,
                                       Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS,
                                       Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED,
                                       Tokenizer.TOKEN_CLASS__EMAIL,
                                       Tokenizer.TOKEN_CLASS__EMOTICON,
                                       Tokenizer.TOKEN_CLASS__UNICODE,
                                       Tokenizer.TOKEN_CLASS__URL,
                                       Tokenizer.TOKEN_CLASS__HTML_ENTITY,
                                       Tokenizer.TOKEN_CLASS__NON_ASCII,
                                       Tokenizer.TOKEN_CLASS__NUMBER,
                                       Tokenizer.TOKEN_CLASS__SPECIAL_TERM_TOPIC,
                                       Tokenizer.TOKEN_CLASS__SPECIAL_TERM_USER,
                                       Tokenizer.TOKEN_CLASS__TIME_FORMAT,
                                       Tokenizer.TOKEN_CLASS__UNKNOWN]

    NEGATION_BOUNDARY_TOKEN_EXCEPTION_CLASSES = [Tokenizer.TOKEN_CLASS__QUOTE_CLOSE,
                                                 Tokenizer.TOKEN_CLASS__QUOTE_OPEN]

    #NEGATION_BOUNDARY_TOKENS = ['but', 'unless']

    NEGATION_RULE__NEGATION_WORD_TOKEN_CLASSES = ['neg']


    ALL_CAPS_RULE__VALID_TOKEN_CLASSES = [Tokenizer.TOKEN_CLASS__ALPHANUM,
                                          Tokenizer.TOKEN_CLASS__ALPHANUM_NEGATION_ABBREVIATION]


    ANP_RULE__POS_WILDCARD_TOKEN_CLASSES = [Tokenizer.TOKEN_CLASS__QUOTE_OPEN,
                                            Tokenizer.TOKEN_CLASS__QUOTE_CLOSE],
    ANP_RULE__POS_UNKNOWN_TOKEN_CLASSES = [Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS,
                                           Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED]

    WORD_TYPE__ADJECTIVE__NORMAL = 1
    WORD_TYPE__ADJECTIVE__COMPARATIVE = 2
    WORD_TYPE__ADJECTIVE__SUPERLATIVE = 3
    WORD_TYPE__ADJECTIVE__RELEVANCE = 5


    QUOTATION__QUOTED_WORD = 1
    QUOTATION__QUOTED_PHRASE = 2
