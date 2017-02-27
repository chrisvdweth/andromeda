from andromeda.config import Constants
from andromeda.util import TokenListUtil



class AllCaps():

    @staticmethod
    def process(token_list, token_feature_class):
        for idx, feature_dict in enumerate(token_list):
            token_class = TokenListUtil.get_token_class(token_list, idx)
            # Ignore tokens that are nore "normal" words
            if token_class not in Constants.LIFE__ALL_CAPS_RULE__VALID_TOKEN_CLASSES:
                continue
            # Fetch token
            token = TokenListUtil.get_token(token_list, idx)
            # Check if word is all caps AND that its length is larger than 1
            if token.isupper() == True and len(token) > 1:
                feature_dict[Constants.LIFE__TOKEN_FEATURE__BASE][token_feature_class] = 1


