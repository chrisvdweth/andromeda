from andromeda.config.constants import Constants


class TokenListUtil:



    def __init__(self):
        pass


    @staticmethod
    def get_token(token_list, idx, default=None):
        try:
            if Constants.NORMALIZER__TOKEN_FEATURE__STANDARDIZED in token_list[idx][Constants.NORMALIZER__TOKEN_FEATURE__BASE]:
                return token_list[idx][Constants.NORMALIZER__TOKEN_FEATURE__BASE][Constants.NORMALIZER__TOKEN_FEATURE__STANDARDIZED]
            elif Constants.NORMALIZER__TOKEN_FEATURE__NORMALIZED in token_list[idx][Constants.NORMALIZER__TOKEN_FEATURE__BASE]:
                return token_list[idx][Constants.NORMALIZER__TOKEN_FEATURE__BASE][Constants.NORMALIZER__TOKEN_FEATURE__NORMALIZED]
            else:
                return token_list[idx][Constants.TOKENIZER__TOKEN_FEATURE__BASE][Constants.TOKENIZER__TOKEN_FEATURE__TOKEN]
        except:
            return default


    @staticmethod
    def get_token_class(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.TOKENIZER__TOKEN_FEATURE__BASE][Constants.TOKENIZER__TOKEN_FEATURE__CLASS]
        except:
            return default


    @staticmethod
    def get_pos_tag(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.TOKENIZER__TOKEN_FEATURE__BASE][Constants.POSTAGGER__TOKEN_FEATURE__POS_TAG]
        except:
            return default



    @staticmethod
    def get_token_deslanged(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.TOKENIZER__TOKEN_FEATURE__BASE][Constants.NORMALIZER__TOKEN_FEATURE__DESLANGED]
        except:
            return default


    @staticmethod
    def get_token_segmented(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.TOKENIZER__TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__SEGMENTED]
        except:
            return default


    @staticmethod
    def get_life_anp(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP]
        except:
            return default


    @staticmethod
    def get_life_negation(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__NEGATION]
        except:
            return default


    @staticmethod
    def get_life_quotation(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__QUOTED]
        except:
            return default


    @staticmethod
    def get_sentiment_score(token_list, idx, default=0.0):
        try:
            return token_list[idx][Constants.SENTIGRADE__TOKEN_FEATURE__BASE][Constants.SENTIGRADE__TOKEN_SENTIMENT_SCORE]
        except:
            return default

    @staticmethod
    def get_life_word_tag(token_list, idx, default=None):
        try:
            return token_list[idx][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__TAG]
        except:
            return default
