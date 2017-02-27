from andromeda.config import Constants
from andromeda.util import TokenListUtil
from andromeda.core.featureextraction.lifeprocessing.lifebase import LifeBase




class Quotation:

    def __init__(self):
        pass

    @staticmethod
    def process(token_list, token_feature_class):
        indices = [idx for idx, _ in enumerate(token_list) if TokenListUtil.get_token(token_list, idx) == '"']
        for idx_pair in LifeBase.chunks(indices, 2):
            # If the the number of quotation marks is odd, we have a problem
            if len(idx_pair) < 2:
                return
            # Calculate number of tokens between quotation marks
            token_count = idx_pair[1] - idx_pair[0] - 1

            if token_count == 1:
                Quotation._set_feature(token_list, idx_pair[0]+1, idx_pair[1], token_feature_class, Constants.LIFE__QUOTATION__QUOTED_WORD)
            elif token_count > 1:
                Quotation._set_feature(token_list, idx_pair[0]+1, idx_pair[1], token_feature_class, Constants.LIFE__QUOTATION__QUOTED_PHRASE)


    @staticmethod
    def _set_feature(token_list, start_pos, end_pos, token_feature_class, value):
        for pos in range(start_pos, end_pos):
            token_list[pos][Constants.LIFE__TOKEN_FEATURE__BASE][token_feature_class] = value
