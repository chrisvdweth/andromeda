from andromeda.config import Constants
from andromeda.util.tokenlistutil import TokenListUtil
from andromeda.app.sentiment.text.sentilexscorer import SentilexScorer


class SentiScoreCalculator:

    def __init__(self, sentigrade):
        self.sentigrade = sentigrade
        self.config = self.sentigrade.config['senti-score-calculator']
        self.sentilex_scorer = SentilexScorer(self.config['sentilex-scorer'])

        self.sentilex_scorer.initialize_word_lexicons()


    def process(self, token_list):
        # Basic token-wise processing of sentiment value
        for idx in range(len(token_list)):
            self._process_token(token_list, idx)

        # Check attribute-noun pairs
        for idx in range(len(token_list)):
            if TokenListUtil.get_life_anp(token_list, idx) is not None and TokenListUtil.get_pos_tag(token_list, idx) in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                self._process_anp(token_list, idx)


    def _process_token(self, token_list, idx):
        token_list[idx][Constants.SENTIGRADE__TOKEN_FEATURE__BASE] = {}

        # Get token (standaradized => normalized => default) and token class
        token = TokenListUtil.get_token(token_list, idx).lower()
        token_class = TokenListUtil.get_token_class(token_list, idx)

        sentiment_value = None

        # Check if token is an emoji or emoticon
        if token_class in [Constants.TOKENIZER__TOKEN_CLASS__EMOTICON, Constants.TOKENIZER__TOKEN_CLASS__UNICODE]:
            sentiment_value = self._score_emo_token(token)
        elif token_class in [Constants.TOKENIZER__TOKEN_CLASS__ALPHANUM]:
            sentiment_value = self._score_alphanum_token(token)

        # Set default sentiment value of token to 0.0 as default (just in case not condition applies)
        if sentiment_value is None:
            sentiment_value = 0.0

        # For segmented tokens, perform calculation completely recursively
        # (i.e., treat phrase as new input)
        token_segmented = TokenListUtil.get_token_segmented(token_list, idx)
        if token_segmented is not None:
            self.sentigrade.process(token_segmented)

        # If the sentiment value is 0.0, there's not need to check if it need s to be flipped or modulated
        if sentiment_value == 0.0:
            return

        # Check if there are (simple) linguistic data that causes the polarity to flip
        # (negation, quoted words)
        sentiment_value = self._handle_polarity_changer(sentiment_value, token, idx, token_list)

        # Add sentiment value to token list if the value is not 0.0
        if sentiment_value is not None and sentiment_value != 0.0:
            token_list[idx][Constants.SENTIGRADE__TOKEN_FEATURE__BASE][Constants.SENTIGRADE__TOKEN_SENTIMENT_SCORE] = round(sentiment_value, 3)




    def _score_emo_token(self, token):
        if token.lower() == Constants.UNICODE_NORMALIZER__SENTIMENT_POSITIVE_STRING.lower() or \
           token.lower() == Constants.EMOTICON_NORMALIZER__SENTIMENT_POSITIVE_STRING.lower():
            return 1.0
        if token.lower() == Constants.UNICODE_NORMALIZER__SENTIMENT_NEGATIVE_STRING.lower() or \
           token.lower() == Constants.EMOTICON_NORMALIZER__SENTIMENT_NEGATIVE_STRING.lower():
            return -1.0
        return 0.0


    def _score_alphanum_token(self, token):
        if token.lower() == Constants.EMOTEXT_NORMALIZER__SENTIMENT_POSITIVE_STRING.lower():
            return 1.0
        if token.lower() == Constants.EMOTEXT_NORMALIZER__SENTIMENT_NEGATIVE_STRING.lower():
            return -1.0
        else:
            return self.sentilex_scorer.get_average_score(token)


    def _handle_polarity_changer(self, sentiment_value, token, idx, token_list):
        life_negation_value = TokenListUtil.get_life_negation(token_list, idx, default=0)
        life_quotation_value = TokenListUtil.get_life_quotation(token_list, idx, default=0)
        if life_negation_value == 1:
            sentiment_value *= -1
        if life_quotation_value == 1:
            sentiment_value *= -1
        return sentiment_value



    def _process_anp(self, token_list, idx):
        noun_anp_list = TokenListUtil.get_life_anp(token_list, idx)
        noun_sentiment_score = TokenListUtil.get_sentiment_score(token_list, idx)

        # Shouldn't be needed actually
        if noun_anp_list is None or len(noun_anp_list) == 0:
            return

        # Get the sentiment score of all (sentiment-carrying) adjectives modifying the noun
        adjective_sentiment_scores_list = []
        for adjective_pos in noun_anp_list:
            adjective_sentiment_score = TokenListUtil.get_sentiment_score(token_list, adjective_pos)
            if adjective_sentiment_score is not None and adjective_sentiment_score != 0.0:
                adjective_sentiment_scores_list.append(adjective_sentiment_score)

        # if not attribute carries a sentiment, ignore
        if len(adjective_sentiment_scores_list) == 0:
            return

        # if sentiments of the attributes differ, ignore
        if not (all(item >= 0 for item in adjective_sentiment_scores_list) or all(item < 0 for item in adjective_sentiment_scores_list)):
            return

        # if sentiments of attributes is the same as for the noun, ignore
        if ((adjective_sentiment_scores_list[0] < 0) == (noun_sentiment_score < 0)) or ((adjective_sentiment_scores_list[0] > 0) == (noun_sentiment_score > 0)):
            return 0

        #
        # Who's the winner?
        #
        contains_relevance_adjective = False
        for adjective_pos in noun_anp_list:
            word_types_list = TokenListUtil.get_life_word_tag(token_list, adjective_pos)
            if word_types_list is not None and Constants.LIFE__WORD_TYPE__ADJECTIVE__RELEVANCE in word_types_list:
                contains_relevance_adjective = True
                break

        # noun wins
        if contains_relevance_adjective == True:
            if noun_sentiment_score < 0:
                for adjective_pos in noun_anp_list:
                    try:
                        print adjective_pos
                        token_list[adjective_pos][Constants.SENTIGRADE__TOKEN_FEATURE__BASE][Constants.SENTIGRADE__TOKEN_SENTIMENT_SCORE] *= -1
                    except:
                        pass
        # adjective wins
        else:
            try:
                token_list[idx][Constants.SENTIGRADE__TOKEN_FEATURE__BASE][Constants.SENTIGRADE__TOKEN_SENTIMENT_SCORE] = 0.0
            except:
                pass
