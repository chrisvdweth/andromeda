import re
from andromeda.config import Constants
from andromeda.core.featureextraction.lifeprocessing.lifebase import LifeBase


class AdjectiveNounPairs:

    ANP_REGEX_PREMODIFIERS = r'(W?AW?)(([&,R,P]*W?AW?)+)*(W?NW?)(([&,]*W?NW?)+)*'
    ANP_REGEX_POSTMODIFIERS = r'(W?N+W?)(&D*W?NW?)*(R*)(V+)([WRD]*)(W?AW?)(([&,R,P]*W?AW?)+)*'


    def __init__(self):
        pass

    @staticmethod
    def process(token_list, token_feature_class):

        pos_tags_string = LifeBase.calculate_pos_tag_string(token_list,
                                                            wildcard_pos_tags_list=Constants.LIFE__ANP_RULE__POS_WILDCARD_TOKEN_CLASSES,
                                                            unknown_pos_tags_list=Constants.LIFE__ANP_RULE__POS_UNKNOWN_TOKEN_CLASSES)
        print pos_tags_string
        AdjectiveNounPairs._process_premodifiers(token_list, pos_tags_string)
        AdjectiveNounPairs._process_postmodifiers(token_list, pos_tags_string)
        AdjectiveNounPairs._filter_anp(token_list)



    @staticmethod
    def _process_premodifiers(token_list, pos_tag_string):
        p = re.compile(AdjectiveNounPairs.ANP_REGEX_PREMODIFIERS)
        for m in p.finditer(pos_tag_string):
            adjective_pos_list = []
            noun_pos_list = []
            ignored_adjective_post_list = []
            # Get positions of all adjectives
            for pos in range(m.start(1), m.end(1)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    if AdjectiveNounPairs._is_valid_adjective(pos_tag_string, pos):
                        adjective_pos_list.append(pos)
                    else:
                        ignored_adjective_post_list.append(pos)
            for pos in range(m.start(2), m.end(2)):
                print pos_tag_string[pos+1:pos+2]
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    if AdjectiveNounPairs._is_valid_adjective(pos_tag_string, pos):
                        adjective_pos_list.append(pos)
                    else:
                        ignored_adjective_post_list.append(pos)
            # Assign adjective positions to all nouns
            for pos in range(m.start(4), m.end(4)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    if pos not in ignored_adjective_post_list:
                        noun_pos_list.append(pos)
            for pos in range(m.start(5), m.end(5)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    if pos not in ignored_adjective_post_list:
                        noun_pos_list.append(pos)
            # Set the found adjective noun pairs in the token list
            AdjectiveNounPairs._set_anp(token_list, adjective_pos_list, noun_pos_list)


    @staticmethod
    def _process_postmodifiers(token_list, pos_tag_string):
        p = re.compile(AdjectiveNounPairs.ANP_REGEX_POSTMODIFIERS)
        for m in p.finditer(pos_tag_string):
            adjective_pos_list = []
            noun_pos_list = []
            ignored_adjective_post_list = []
            # Get positions of all adjectives
            for pos in range(m.start(6), m.end(6)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    if AdjectiveNounPairs._is_valid_adjective(pos_tag_string, pos):
                        adjective_pos_list.append(pos)
                    else:
                        ignored_adjective_post_list.append(pos)
            for pos in range(m.start(7), m.end(7)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__ADJECTIVE]:
                    if AdjectiveNounPairs._is_valid_adjective(pos_tag_string, pos):
                        adjective_pos_list.append(pos)
                    else:
                        ignored_adjective_post_list.append(pos)
            # Assign adjective positions to all nouns
            for pos in range(m.start(1), m.end(1)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    if pos not in ignored_adjective_post_list:
                        noun_pos_list.append(pos)
            for pos in range(m.start(2), m.end(2)):
                if pos_tag_string[pos] in [Constants.POSTAGGER__POS_TAG__COMMON_NOUN]:
                    if pos not in ignored_adjective_post_list:
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


    @staticmethod
    def _is_valid_adjective(pos_tag_string, pos):
        next_pos_tag_list = pos_tag_string[pos+1:pos+2]
        if len(next_pos_tag_list) == 0:
            return True
        if next_pos_tag_list[0] == Constants.POSTAGGER__POS_TAG__PRE_POST_POSITION:
            return False
        return True


    @staticmethod
    def _filter_anp(token_list):
        for pos, item in enumerate(token_list):
            pos_tag = item[Constants.POSTAGGER__TOKEN_FEATURE__BASE][Constants.POSTAGGER__TOKEN_FEATURE__POS_TAG]
            # Ignore words that are not an adjective
            if pos_tag != Constants.POSTAGGER__POS_TAG__ADJECTIVE:
                continue
            # Just to be sure, check of adjective describes indeed a noun
            if Constants.LIFE__ANP in item[Constants.LIFE__TOKEN_FEATURE__BASE]:
                noun_pos_list = item[Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP]
            else:
                continue
            # Split between pre- and post-modifier adjectives (the positions)
            pre = [p for p in noun_pos_list if p > pos]
            post = [p for p in noun_pos_list if p < pos]
            # Nothing to do if it's not critical case
            if len(pre) == 0 or len(post) == 0:
                continue
            # By default, pre-modifier adjectives win ==> remove ANP info from post-modifier adjectives
            for p in post:
                AdjectiveNounPairs._remove_anp_entry(token_list, pos, p)
                AdjectiveNounPairs._remove_anp_entry(token_list, p, pos)


    @staticmethod
    def _remove_anp_entry(token_list, pos, anp_pos):
        try:
            token_list[pos][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP].remove(anp_pos)
            if len(token_list[pos][Constants.LIFE__TOKEN_FEATURE__BASE][Constants.LIFE__ANP]) == 0:
                token_list[pos][Constants.LIFE__TOKEN_FEATURE__BASE].pop(Constants.LIFE__ANP, None)
        except:
            pass
