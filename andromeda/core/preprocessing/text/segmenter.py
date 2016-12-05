from andromeda.core.preprocessing.text.tokenizer import Tokenizer


class Segmenter:

    TOKEN_FEATURE_CLASSES__SEGMENTATION_SEPARATORS = [Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS,
                                                      Tokenizer.TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED,
                                                      Tokenizer.TOKEN_CLASS__NON_ASCII,
                                                      Tokenizer.TOKEN_CLASS__EMOTICON,
                                                      Tokenizer.TOKEN_CLASS__CHARACTER_SUBSTRING,
                                                      Tokenizer.TOKEN_CLASS__EMAIL,
                                                      Tokenizer.TOKEN_CLASS__URL,
                                                      Tokenizer.TOKEN_CLASS__HTML_ENTITY,
                                                      Tokenizer.TOKEN_CLASS__UNICODE,
                                                      Tokenizer.TOKEN_CLASS__UNKNOWN]

    TOKEN_FEATURE_CLASSES__INDIVIDUAL_SEGMENTS = [Tokenizer.TOKEN_CLASS__NON_ASCII,
                                                  Tokenizer.TOKEN_CLASS__EMOTICON,
                                                  Tokenizer.TOKEN_CLASS__CHARACTER_SUBSTRING,
                                                  Tokenizer.TOKEN_CLASS__EMAIL,
                                                  Tokenizer.TOKEN_CLASS__URL,
                                                  Tokenizer.TOKEN_CLASS__HTML_ENTITY,
                                                  Tokenizer.TOKEN_CLASS__UNICODE,
                                                  Tokenizer.TOKEN_CLASS__UNKNOWN]

    TOKEN_FEATURE__BASE = 'core'
    TOKEN_FEATURE__SEGMENT_NUMBER = 'segment_nr'


    def __init__(self):
        pass


    def segment(self, token_list):

        segment_nr = 0

        for feature_dict in token_list:
            token_class = feature_dict[Tokenizer.TOKEN_FEATURE__BASE][Tokenizer.TOKEN_FEATURE__CLASS]

            # If token is a emoji, URL, email, etc => create a unique segment,
            # since such token are typically not part of proper sentence
            if token_class in Segmenter.TOKEN_FEATURE_CLASSES__INDIVIDUAL_SEGMENTS:
                segment_nr += 1

            feature_dict[Segmenter.TOKEN_FEATURE__BASE][Segmenter.TOKEN_FEATURE__SEGMENT_NUMBER] = segment_nr

            if token_class in Segmenter.TOKEN_FEATURE_CLASSES__SEGMENTATION_SEPARATORS:
                segment_nr += 1

        return token_list

