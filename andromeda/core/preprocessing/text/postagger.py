import json
import requests
from andromeda.util.tokenlistutil import TokenListUtil
from andromeda.config.constants import Constants

class POSTagger:

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
            print '[WARNING] POSTagger: len(pos_tagger_result) != len(token_list)',
            self._set_all_to_uknown(token_list)
            return token_list

        for pos in xrange(len(token_list)):
            # Replace pausing POS tag with terminal POS tag
            # (the POS tagger does not distinguish between terminal and pausing punctuation marks)
            if pos_tagger_result[pos][1] == Constants.POSTAGGER__POS_TAG__PUNCTUATION_PAUSING and token_list[pos][Constants.TOKENIZER__TOKEN_FEATURE__BASE][Constants.TOKENIZER__TOKEN_FEATURE__CLASS] in [Constants.TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS, Constants.TOKENIZER__TOKEN_CLASS__PUNCTUATION_TERMINAL_POINTS_REPEATED]:
                token_list[pos][Constants.POSTAGGER__TOKEN_FEATURE__BASE][Constants.POSTAGGER__TOKEN_FEATURE__POS_TAG] = Constants.POSTAGGER__POS_TAG__PUNCTUATION_TERMINAL
            else:
                token_list[pos][Constants.POSTAGGER__TOKEN_FEATURE__BASE][Constants.POSTAGGER__TOKEN_FEATURE__POS_TAG] = pos_tagger_result[pos][1]

        return token_list



    def _generate_string(self, token_list):
        s = ''
        for idx, feature_dict in enumerate(token_list):
            token = TokenListUtil.get_token(token_list, idx)
            # normalizer_data_dict = feature_dict[Normalizer.TOKEN_FEATURE__BASE]
            # if Normalizer.TOKEN_FEATURE__STANDARDIZED in normalizer_data_dict:
            #     token = normalizer_data_dict[Normalizer.TOKEN_FEATURE__STANDARDIZED]
            # elif Normalizer.TOKEN_FEATURE__NORMALIZED in normalizer_data_dict:
            #     token = normalizer_data_dict[Normalizer.TOKEN_FEATURE__NORMALIZED]
            # else:
            #     token = normalizer_data_dict[Tokenizer.TOKEN_FEATURE__TOKEN]
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
            feature_dict[Constants.POSTAGGER__TOKEN_FEATURE__BASE][Constants.POSTAGGER__TOKEN_FEATURE__POS_TAG] = Constants.POSTAGGER__POS_TAG__UNKNOWN


    def _request_pos_tags(self, text):
        print self.api_url
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


