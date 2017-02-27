from andromeda.config.constants import Constants


class Segmenter:

    def __init__(self):
        pass


    def segment(self, token_list):

        segment_nr = 0

        for feature_dict in token_list:
            token_class = feature_dict[Constants.TOKENIZER__TOKEN_FEATURE__BASE][Constants.TOKENIZER__TOKEN_FEATURE__CLASS]

            # If token is a emoji, URL, email, etc => create a unique segment,
            # since such token are typically not part of proper sentence
            if token_class in Constants.SEGMENTER__TOKEN_FEATURE_CLASSES__INDIVIDUAL_SEGMENTS:
                segment_nr += 1

            feature_dict[Constants.SEGMENTER__TOKEN_FEATURE__BASE][Constants.SEGMENTER__TOKEN_FEATURE__SEGMENT_NUMBER] = segment_nr

            if token_class in Constants.SEGMENTER__TOKEN_FEATURE_CLASSES__SEGMENTATION_SEPARATORS:
                segment_nr += 1

        return token_list

