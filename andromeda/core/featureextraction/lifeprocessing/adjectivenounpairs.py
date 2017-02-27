import re
from andromeda.config import Constants
from andromeda.core.featureextraction.lifeprocessing.lifebase import LifeBase


class AdjectiveNounPairs:

    ANP_REGEX_PREMODIFIERS = r'(W?AW?)(([&,R]*W?AW?)+)*(W?NW?)(([&,]*W?NW?)+)*'
    ANP_REGEX_POSTMODIFIERS = r'(W?N+W?)(&D*W?NW?)*(R*)(V+)([WRD]*)(W?AW?)(([&,R]*W?AW?)+)*'


    def __init__(self):
        pass

    @staticmethod
    def process(token_list, token_feature_class):

        pos_tags_string = LifeBase.calculate_pos_tag_string(token_list,
                                                            wildcard_pos_tags_list=Constants.LIFE__ANP_RULE__POS_WILDCARD_TOKEN_CLASSES,
                                                            unknown_pos_tags_list=Constants.LIFE__ANP_RULE__POS_UNKNOWN_TOKEN_CLASSES)

        AdjectiveNounPairs._process_premodifiers(token_list, pos_tags_string)
        AdjectiveNounPairs._process_postmodifiers(token_list, pos_tags_string)



    @staticmethod
    def _process_premodifiers(token_list, pos_tag_string):
        p = re.compile(AdjectiveNounPairs.ANP_REGEX_PREMODIFIERS)
        for m in p.finditer(pos_tag_string):
            adjective_pos_list = []
            noun_pos_list = []
            # Get positions of all adjectives
            for pos in range(m.start(1), m.end(1)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    adjective_pos_list.append(pos)
            for pos in range(m.start(2), m.end(2)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    adjective_pos_list.append(pos)
            # Assign adjective positions to all nouns
            for pos in range(m.start(4), m.end(4)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    noun_pos_list.append(pos)
            for pos in range(m.start(5), m.end(5)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    noun_pos_list.append(pos)
            # Set the found adjective noun pairs in the token list
            AdjectiveNounPairs._set_anp(token_list, adjective_pos_list, noun_pos_list)


    @staticmethod
    def _process_postmodifiers(token_list, pos_tag_string):
        p = re.compile(AdjectiveNounPairs.ANP_REGEX_POSTMODIFIERS)
        for m in p.finditer(pos_tag_string):
            adjective_pos_list = []
            noun_pos_list = []
            # Get positions of all adjectives
            for pos in range(m.start(6), m.end(6)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    adjective_pos_list.append(pos)
            for pos in range(m.start(7), m.end(7)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    adjective_pos_list.append(pos)
            # Assign adjective positions to all nouns
            for pos in range(m.start(1), m.end(1)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    noun_pos_list.append(pos)
            for pos in range(m.start(2), m.end(2)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    noun_pos_list.append(pos)
            # Set the found adjective noun pairs in the token list
            AdjectiveNounPairs._set_anp(token_list, adjective_pos_list, noun_pos_list)



    @staticmethod
    def _set_anp(token_list, adjective_pos_list, noun_pos_list):
        # Assign the position of the described nouns to each adjective
        for adjective_pos in adjective_pos_list:
            if Constants.LIFE__ANP not in token_list[adjective_pos][Constants.LIFE__TOKEN_FEATURE__BASE]:
                token_list[adjective_pos][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP] = []
            token_list[adjective_pos][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP].extend(noun_pos_list)
        # Assign the position of the describing adjectives to each noun
        for noun_pos in noun_pos_list:
            if Constants.LIFE__ANP not in token_list[noun_pos][Constants.LIFE__TOKEN_FEATURE__BASE]:
                token_list[noun_pos][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP] = []
            token_list[noun_pos][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP].extend(adjective_pos_list)

