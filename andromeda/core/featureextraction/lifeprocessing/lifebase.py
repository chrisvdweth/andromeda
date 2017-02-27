import os

from andromeda.config import Constants

class LifeBase:

    def __init__(self):
        pass


    @staticmethod
    def init_word_set(word_set, file_names_list, comment="#"):
        for file_name in file_names_list:
            with open(os.path.expanduser(file_name), 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(comment):
                        continue
                    word_set.add(line.split('\t')[0])


    @staticmethod
    def calculate_pos_tag_string(token_list, wildcard_pos_tags_list=[], unknown_pos_tags_list=[]):
        s = ''
        for feature_dict in token_list:
            pos_tag = feature_dict[Constants.TOKENIZER__TOKEN_FEATURE__BASE][Constants.POSTAGGER__TOKEN_FEATURE__POS_TAG]
            if pos_tag in wildcard_pos_tags_list:
                pos_tag = Constants.POSTAGGER__POS_TAG__WILDCARD
            if pos_tag in unknown_pos_tags_list:
                pos_tag = Constants.POSTAGGER__POS_TAG__UNKNOWN
            s += pos_tag
        return s


    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
