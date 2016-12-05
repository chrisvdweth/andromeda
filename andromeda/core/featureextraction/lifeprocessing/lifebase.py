from andromeda.core.preprocessing.text.normalizer import Normalizer
from andromeda.core.preprocessing.text.tokenizer import Tokenizer
from andromeda.core.preprocessing.text.postagger import POSTagger


class LifeBase:

    def __init__(self):
        pass


    @staticmethod
    def get_token(token_list, idx, default=None):
        try:
            if Normalizer.TOKEN_FEATURE__NORMALIZED in token_list[idx][Tokenizer.TOKEN_FEATURE__BASE]:
                return token_list[idx][Tokenizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__NORMALIZED]
            else:
                return token_list[idx][Tokenizer.TOKEN_FEATURE__BASE][Tokenizer.TOKEN_FEATURE__TOKEN]
        except:
            return default


    @staticmethod
    def get_token_class(token_list, idx, default=None):
        try:
            return token_list[idx][Tokenizer.TOKEN_FEATURE__BASE][Tokenizer.TOKEN_FEATURE__CLASS]
        except:
            return default


    @staticmethod
    def get_pos_tag(token_list, idx, default=None):
        try:
            return token_list[idx][Tokenizer.TOKEN_FEATURE__BASE][POSTagger.TOKEN_FEATURE__POS_TAG]
        except:
            return default


    @staticmethod
    def init_word_set(word_set, file_names_list, comment="#"):
        for file_name in file_names_list:
            with open(file_name, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(comment):
                        continue
                    word_set.add(line.split('\t')[0])


    @staticmethod
    def calculate_pos_tag_string(token_list, wildcard_pos_tags_list=[], unknown_pos_tags_list=[]):
        s = ''
        for feature_dict in token_list:
            pos_tag = feature_dict[Tokenizer.TOKEN_FEATURE__BASE][POSTagger.TOKEN_FEATURE__POS_TAG]
            if pos_tag in wildcard_pos_tags_list:
                pos_tag = POSTagger.POS_TAG__WILDCARD
            if pos_tag in unknown_pos_tags_list:
                pos_tag = POSTagger.POS_TAG__UNKNOWN
            s += pos_tag
        return s


    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
