import json

import requests

from andromeda.core.preprocessing.text.normalizer import Normalizer
from andromeda.core.preprocessing.text.tokenizer import Tokenizer


class POSTagger:

    TOKEN_FEATURE__BASE = 'core'
    TOKEN_FEATURE__POS_TAG = 'pos_tag'

    POS_TAG__COMMON_NOUN = "N"
    POS_TAG__PRONOUN = "O"
    POS_TAG__NOMINAL_POSSESSIVE = "S"
    POS_TAG__PROPER_NOUN = "^"
    POS_TAG__PROPER_NOUN_WITH_POSSESSIVE = "Z"
    POS_TAG__NOMINAL_WITH_VERBAL = "L"
    POS_TAG__PROPER_NOUN_WITH_VERBAL = "M"

    POS_TAG__VERB_INCL_COPULA_AUX = "V"
    POS_TAG__ADJECTIVE = "A"
    POS_TAG__ADVERB = "R"
    POS_TAG__INTERJECTION = "!"

    POS_TAG__DETERMINER = "D"
    POS_TAG__PRE_POST_POSITION = "P"
    POS_TAG__COORDINATING_CONJUNCTION = "&"
    POS_TAG__VERB_PARTICLE = "T"
    POS_TAG__EXISTENTIAL = "X"
    POS_TAG__EXISTENTIAL_WITH_VERBAL = "Y"

    POS_TAG__HASHTAG = "#"
    POS_TAG__AT_MENTION = "@"
    POS_TAG__DISCOURSE_MARKER = "~"
    POS_TAG__URL_OR_EMAIL = "U"
    POS_TAG__EMOTICON = "E"

    POS_TAG__NUMERAL = "$"
    POS_TAG__PUNCTUATION = ","
    POS_TAG__OTHER_ABBREVIATIONS = "G"

    POS_TAG__UNKNOWN = "?"
    POS_TAG__WILDCARD = "W"

    def __init__(self, config):
        self.api_url = config['api-url']


    def tag(self, token_list):
        s = self._generate_string(token_list)

        try:
            pos_tagger_result = self._request_pos_tags(s)
        except requests.exceptions.RequestException, e:
            print '[ERROR] POSTagger:', e
            self._set_all_to_uknown(token_list)
            return token_list
        except ValueError, e:
            print '[ERROR] POSTagger:', e
            self._set_all_to_uknown(token_list)
            return token_list

        if len(pos_tagger_result) != len(token_list):
            print pos_tagger_result
            print '[WARNING] POSTagger: len(pos_tagger_result) != len(token_list)',
            self._set_all_to_uknown(token_list)
            return token_list

        for pos in range(len(token_list)):
            token_list[pos][POSTagger.TOKEN_FEATURE__BASE][POSTagger.TOKEN_FEATURE__POS_TAG] = pos_tagger_result[pos][1]

        return token_list



    def _generate_string(self, token_list):
        s = ''
        for feature_dict in token_list:
            normalizer_data_dict = feature_dict[Normalizer.TOKEN_FEATURE__BASE]
            if Normalizer.TOKEN_FEATURE__STANDARDIZED in normalizer_data_dict:
                token = normalizer_data_dict[Normalizer.TOKEN_FEATURE__STANDARDIZED]
            elif Normalizer.TOKEN_FEATURE__NORMALIZED in normalizer_data_dict:
                token = normalizer_data_dict[Normalizer.TOKEN_FEATURE__NORMALIZED]
            else:
                token = normalizer_data_dict[Tokenizer.TOKEN_FEATURE__TOKEN]
            token = self._tweak_token(token)
            s += token + ' '
        return s.strip()


    def _tweak_token(self, token):
        if token.endswith("'") and not token.startswith("'"):
            token += '###'
        elif token.startswith("'") and not token.endswith("'"):
            token = '###' + token
        return token


    def _set_all_to_uknown(self, token_list):
        for feature_dict in token_list:
            feature_dict[POSTagger.TOKEN_FEATURE__BASE][POSTagger.TOKEN_FEATURE__POS_TAG] = POSTagger.POS_TAG__UNKNOWN


    def _request_pos_tags(self, text):
        payload = { "text": text }
        try:
            r = requests.post(self.api_url, data=json.dumps(payload))
        except requests.exceptions.RequestException, e:
            raise requests.exceptions.RequestException('Connection to POS Tagger server failed.')

        try:
            return r.json()["token-tags"]
        except ValueError, e:
            raise ValueError("Could not decode JSON from response.")



    def request_post_tags(self, text):
        return  self._request_pos_tags(text)


    @staticmethod
    def calculate_pos_tag_string(self, token_list):
        s = ''
        for feature_dict in token_list:
            s += feature_dict[POSTagger.TOKEN_FEATURE__POS_TAG]
        return s



if __name__ == "__main__":


    s = "This ain 't good"
    #s = '@DemoUser Can I do it? \U0001F61E \U0001F52B'


    pos_tagger = POSTagger('http://172.29.32.195:11065/postag/')
    print pos_tagger.request_post_tags(s)


    #cleaned_tweet = tokenizer.generate_minimized_document(token_list=None, valid_token_list=[Tokenizer.TOKEN_CLASS_ALPHANUM, Tokenizer.TOKEN_CLASS_PUNCTUATION_TERMINAL_POINTS, Tokenizer.TOKEN_CLASS_PUNCTUATION_PAUSING_POINTS, Tokenizer.TOKEN_CLASS_QUOTE_OPEN, Tokenizer.TOKEN_CLASS_QUOTE_CLOSE, Tokenizer.TOKEN_CLASS_BRACKET_OPEN, Tokenizer.TOKEN_CLASS_BRACKET_CLOSE, Tokenizer.TOKEN_CLASS_UNICODE, Tokenizer.TOKEN_CLASS_NUMBER])
    #print cleaned_tweet
