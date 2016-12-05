from andromeda.core.featureextraction.lifeprocessing.lifebase import LifeBase
from andromeda.core.featureextraction.lifeprocessing.lifeconstants import LifeConstants


class AllCaps(LifeBase):

    @staticmethod
    def process(token_list, token_feature_class):
        for idx, feature_dict in enumerate(token_list):
            token_class = LifeBase.get_token_class(token_list, idx)
            # Ignore tokens that are nore "normal" words
            if token_class not in LifeConstants.ALL_CAPS_RULE__VALID_TOKEN_CLASSES:
                continue
            # Fetch token
            token = LifeBase.get_token(token_list, idx)
            # Check if word is all caps AND that its length is larger than 1
            if token.isupper() == True and len(token) > 1:
                feature_dict[LifeConstants.TOKEN_FEATURE__BASE][token_feature_class] = 1


