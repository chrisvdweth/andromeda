'''
Created on Oct 20, 2016

@author: christian
'''
import regex as re
import string


class Tokenizer:

    PUNCTUATION_MARKS__TERMINAL_POINTS = '.!?'
    PUNCTUATION_MARKS__PAUSING_POINTS = ',:;'

    EMOTICONS_FIXED_PATTERNS = '^^ <3 </3'.split()

    EMOTICONS_GENERIC_PATTERN_TOP = '[]}{()<>'
    EMOTICONS_GENERIC_PATTERN_EYES = '.:;8BX='
    EMOTICONS_GENERIC_PATTERN_NOSES = '-=~\'^o'
    EMOTICONS_GENERIC_PATTERN_MOUTHS = ')(/\|DPp[]{}<>oO*'

    EMOTEXTS_CORE_PATTERNS_LIST = ['ha', 'ah', 'he', 'eh', 'hi', 'ih', 'ho', 'hu', 'hue']

    TOKEN_CLASS__UNKNOWN = 0
    TOKEN_CLASS__WHITESPACE = 1
    TOKEN_CLASS__CHARACTER_SUBSTRING = 2
    TOKEN_CLASS__ALPHANUM = 10
    TOKEN_CLASS__ALPHANUM_NEGATION_ABBREVIATION = 11
    TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS = 20
    TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED = 21
    TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS = 30
    TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS_REPEATED = 31
    TOKEN_CLASS__URL = 60
    TOKEN_CLASS__EMAIL = 65
    TOKEN_CLASS__SPECIAL_TERM_USER = 70
    TOKEN_CLASS__SPECIAL_TERM_TOPIC = 71
    TOKEN_CLASS__NUMBER = 80
    TOKEN_CLASS__TIME_FORMAT = 85
    TOKEN_CLASS__EMOTICON = 90
    #TOKEN_CLASS__LAUGHTER = 91

    TOKEN_CLASS__HTML_ENTITY = 150
    TOKEN_CLASS__UNICODE = 160

    TOKEN_CLASS__NON_ASCII = 200

    TOKEN_CLASS__QUOTE_OPEN = 301
    TOKEN_CLASS__QUOTE_CLOSE = 302
    TOKEN_CLASS__BRACKET_OPEN = 311
    TOKEN_CLASS__BRACKET_CLOSE = 312

    TOKEN_FEATURE__BASE = 'core'
    TOKEN_FEATURE__TOKEN = 'token'
    TOKEN_FEATURE__CLASS = 'class'
    TOKEN_FEATURE__FIRST_CHARACTER_INDEX = 'char_idx'
    TOKEN_FEATURE__CHARACTER_COUNT = 'char_count'


    def __init__(self):
        self._raw_string = ''
        self._char_map = []
        self._init_char_map()


    def _init_char_map(self):
        self._char_map = []
        for c in self._raw_string:
            self._char_map.append((Tokenizer.TOKEN_CLASS__UNKNOWN, 0))


    def _set_token_class(self, start_pos, end_pos, token_class, token_class_nr=0, overwrite=False):
        for pos in range(start_pos, end_pos):
            if self._char_map[pos][0] == Tokenizer.TOKEN_CLASS__UNKNOWN or overwrite == True:
                self._char_map[pos] = (token_class, token_class_nr)


    def tokenize(self, s):
        self._raw_string = s.strip()
        self._init_char_map()


        self._match_whitespaces(Tokenizer.TOKEN_CLASS__WHITESPACE)
        #self._match_unicode_strings(Tokenizer.TOKEN_CLASS__UNICODE)
        self._match_urls(Tokenizer.TOKEN_CLASS__URL)
        self._match_emails(Tokenizer.TOKEN_CLASS__EMAIL)
        self._match_special_twitter_concepts('@', Tokenizer.TOKEN_CLASS__SPECIAL_TERM_USER)
        self._match_special_twitter_concepts('#', Tokenizer.TOKEN_CLASS__SPECIAL_TERM_TOPIC)
        self._match_html_entities(Tokenizer.TOKEN_CLASS__HTML_ENTITY)
        #self._match_time_formats(Tokenizer.TOKEN_CLASS__TIME_FORMAT)
        self._match_numbers(Tokenizer.TOKEN_CLASS__NUMBER)
        self._match_brackets()
        self._match_quotes()
        self._match_emoticons(Tokenizer.TOKEN_CLASS__EMOTICON)
        #self._match_laughter(Tokenizer.TOKEN_CLASS__LAUGHTER)
        self._match_character_substrings('-=\+<>', 2, Tokenizer.TOKEN_CLASS__CHARACTER_SUBSTRING)
        self._match_repeated_chars(Tokenizer.PUNCTUATION_MARKS__TERMINAL_POINTS, Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED)
        self._match_repeated_chars(Tokenizer.PUNCTUATION_MARKS__PAUSING_POINTS, Tokenizer.TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS_REPEATED)
        self._match_punctuation_marks(Tokenizer.PUNCTUATION_MARKS__TERMINAL_POINTS, Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS)
        self._match_punctuation_marks(Tokenizer.PUNCTUATION_MARKS__PAUSING_POINTS, Tokenizer.TOKEN_CLASS__PUNCTUATION_PAUSING_POINTS)
        self._match_alphanumeric_words(Tokenizer.TOKEN_CLASS__ALPHANUM)
        #self._match_negation_abbreviation(Tokenizer.TOKEN_CLASS__ALPHANUM_NEGATION_ABBREVIATION)
        self._match_selected_characters('\'&@*+', Tokenizer.TOKEN_CLASS__ALPHANUM)
        self._match_unicode_characters(Tokenizer.TOKEN_CLASS__UNICODE)
        return self._generate_token_list()


    def _match_html_entities(self, token_class):
        p = re.compile('&[^\s]*;')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_unicode_strings(self, token_class):
        token_class_nr = 0
        for size in [8,4]:
            p = re.compile(r'(\\[U])(\w{%s})' % size, re.IGNORECASE)
            for m in p.finditer(self._raw_string):
                token_class_nr += 1
                self._set_token_class(m.start(1), m.end(2), token_class, token_class_nr)


    def _match_urls(self, token_class):
        p = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[^ \<\.;:"\'\)\]\}]')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_emails(self, token_class):
        p = re.compile('([a-z0-9!#$%&\'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)')
        for m in p.finditer(self._raw_string, re.UNICODE):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_whitespaces(self, token_class):
        p = re.compile(' ')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_repeated_chars(self, character_list, token_class):
        pattern_core = '|'.join(character_list)
        p = re.compile('['+pattern_core+']{2,}')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_character_substrings(self, character_list, min_length, token_class):
        core_pattern = ''.join(character_list)
        p = re.compile('['+core_pattern+']{2,}')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_quotes(self):
        p = re.compile('(?<=\W)"([^"'+Tokenizer.PUNCTUATION_MARKS__PAUSING_POINTS+Tokenizer.PUNCTUATION_MARKS__TERMINAL_POINTS+']*)"(?=\W)')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[0] + 1, Tokenizer.TOKEN_CLASS__QUOTE_OPEN)
            self._set_token_class(m.span()[1] - 1, m.span()[1], Tokenizer.TOKEN_CLASS__QUOTE_CLOSE)
        p = re.compile('(?<=\W)\'([^\':;\.,]*)\'(?=\W)')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[0] + 1, Tokenizer.TOKEN_CLASS__QUOTE_OPEN)
            self._set_token_class(m.span()[1] - 1, m.span()[1], Tokenizer.TOKEN_CLASS__QUOTE_CLOSE)


    def _match_brackets(self):
        bracket_pairs = [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]
        for bracket_pair in bracket_pairs:
            p = re.compile('\\'+bracket_pair[0]+'([^\\'+bracket_pair[0]+'\\'+bracket_pair[1]+']*)\\'+bracket_pair[1])
            for m in p.finditer(self._raw_string):
                self._set_token_class(m.span()[0], m.span()[0] + 1, Tokenizer.TOKEN_CLASS__BRACKET_OPEN)
                self._set_token_class(m.span()[1] - 1, m.span()[1], Tokenizer.TOKEN_CLASS__BRACKET_CLOSE)


    def _match_punctuation_marks(self, character_list, token_class):
        pattern_core = '|'.join(character_list)
        p = re.compile(r'(['+pattern_core+'])')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.start(1), m.end(1), token_class)


    def _match_alphanumeric_words(self, token_class):
        p = re.compile('([a-zA-Z0-9]+)(?:[-[a-zA-Z0-9]|\']*([a-zA-Z0-9])?)?')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_special_twitter_concepts(self, start_char, token_class):
        p = re.compile(start_char+'([A-Za-z_]+[A-Za-z0-9_]+)')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_numbers(self, token_class):
        p = re.compile('(?<=\s)([+-]?\d+(?:.\d)?\d*)(?=\W)')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_time_formats(self, token_class):
        p = re.compile(r'(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)\s?(am|pm|a\.m\.|p\.m\.)?')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)

    def _match_laughter(self, token_class):
        pattern_core = '|'.join(Tokenizer.EMOTEXTS_CORE_PATTERNS_LIST)
        p = re.compile(r'\b[a-z]*(' + pattern_core + r'){2,}[a-z]*\b', re.IGNORECASE)
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_emoticons(self, token_class):
        # Generic patterns
        p = re.compile("(^|\s+)([%s]?)([%s])([%s]?)([%s]+)([,\.]|$|\s+)" % tuple(map(re.escape, [Tokenizer.EMOTICONS_GENERIC_PATTERN_TOP, Tokenizer.EMOTICONS_GENERIC_PATTERN_EYES, Tokenizer.EMOTICONS_GENERIC_PATTERN_NOSES, Tokenizer.EMOTICONS_GENERIC_PATTERN_MOUTHS])))
        for m in p.finditer(self._raw_string, overlapped=True):
            self._set_token_class(m.start(2), m.end(5), token_class)
        # Generic patterns (mirrored orientation)
        p = re.compile("(^|\s+)([%s]+)([%s]?)([%s])([%s]?)([,\.]|$|\s+)" % tuple(map(re.escape, [Tokenizer.EMOTICONS_GENERIC_PATTERN_MOUTHS, Tokenizer.EMOTICONS_GENERIC_PATTERN_NOSES, Tokenizer.EMOTICONS_GENERIC_PATTERN_EYES, Tokenizer.EMOTICONS_GENERIC_PATTERN_TOP])))
        for m in p.finditer(self._raw_string, overlapped=True):
            self._set_token_class(m.start(2), m.end(5), token_class)
        # Fixed patterns
        p = re.compile('|'.join(map(re.escape, Tokenizer.EMOTICONS_FIXED_PATTERNS)))
        for m in p.finditer(self._raw_string, overlapped=True):
            self._set_token_class(m.span()[0], m.span()[1], token_class, overwrite=True)


    def _match_unicode_characters(self, token_class):
        token_class_nr = 0
        p = re.compile("\W", re.UNICODE)
        for m in p.finditer(self._raw_string):
            c = self._raw_string[m.span()[0]:m.span()[1]]
            if c not in string.printable:
                token_class_nr += 1
                self._set_token_class(m.span()[0], m.span()[1], token_class, token_class_nr)


    def _match_selected_characters(self, character_list, token_class):
        pattern_core = '|'.join(character_list)
        p = re.compile('['+pattern_core+']{1}')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _match_negation_abbreviation(self, token_class):
        p = re.compile('([A-Za-z0-9_]+)([^n])([n]+\'[t]+)' , re.IGNORECASE)
        for m in p.finditer(self._raw_string):
            #print m.start(2), m.end(2)
            self._set_token_class(m.start(3), m.end(3), token_class, overwrite=True)


    def __match_time_formats(self, token_class):
        p = re.compile(r'(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)\s?(am|pm|a\.m\.|p\.m\.)?')
        for m in p.finditer(self._raw_string):
            self._set_token_class(m.span()[0], m.span()[1], token_class)


    def _generate_token_list(self):
        token_list = []
        token = ''
        current_token_class = -1
        current_token_class_nr = -1
        for pos, val in enumerate(self._char_map):
            token_class = val[0]
            token_class_nr = val[1]

            if token_class != current_token_class or token_class_nr != current_token_class_nr or token_class == Tokenizer.TOKEN_CLASS__NON_ASCII:
                if not token.isspace() and current_token_class >= 0:
                    token_list.append({ Tokenizer.TOKEN_FEATURE__BASE :
                                            { Tokenizer.TOKEN_FEATURE__TOKEN: token,
                                              Tokenizer.TOKEN_FEATURE__CLASS: current_token_class,
                                              Tokenizer.TOKEN_FEATURE__FIRST_CHARACTER_INDEX: (pos - len(token)),
                                              Tokenizer.TOKEN_FEATURE__CHARACTER_COUNT: len(token)
                                            }
                                      })
                token = ''
                current_token_class = token_class
                current_token_class_nr = token_class_nr
            token += self._raw_string[pos]

        if token != '':
            token_list.append({ Tokenizer.TOKEN_FEATURE__BASE :
                                    { Tokenizer.TOKEN_FEATURE__TOKEN: token,
                                      Tokenizer.TOKEN_FEATURE__CLASS: current_token_class,
                                      Tokenizer.TOKEN_FEATURE__FIRST_CHARACTER_INDEX: (pos+1 - len(token)),
                                      Tokenizer.TOKEN_FEATURE__CHARACTER_COUNT: len(token)
                                    }
                              })
        return token_list









if __name__ == "__main__":


    s = '@DemoUser Watched Spectre yesterday HAHAHAHA It was good, but not the "masterpiece" everyone had expected :('
    #s = '@DemoUser Can I do it? \U0001F61E \U0001F52B'
    #s = 'peoples\' consumers \'decide on what they really want\': SINGAPORE An elderly customer bought... http://t.co/dwSxPnUbJJ #singapore'
    #s = 'new \'Your Signature Emoji\' feature (http://bla.com)'
    s = ':\'( :\'( \'test\' yep'
    #s = ':\'( :\'( "test" yes'
    s = '\U0001F602\U0001F602Woooow\u2026Deadpool\U0001F602'.decode('unicode-escape')


    print type(s), s

    tokenizer = Tokenizer()
    token_list = tokenizer.tokenize(s)

    for feature_dict in token_list:
        print feature_dict

    #cleaned_tweet = tokenizer.generate_minimized_document(token_list=None, valid_token_list=[Tokenizer.TOKEN_CLASS_ALPHANUM, Tokenizer.TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS, Tokenizer.TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS, Tokenizer.TOKEN_CLASS_QUOTE_OPEN, Tokenizer.TOKEN_CLASS_QUOTE_CLOSE, Tokenizer.TOKEN_CLASS_BRACKET_OPEN, Tokenizer.TOKEN_CLASS_BRACKET_CLOSE, Tokenizer.TOKEN_CLASS_UNICODE, Tokenizer.TOKEN_CLASS_NUMBER])
    #print cleaned_tweet
