from andromeda.core.featureextraction.lifeprocessing.lifeconstants import LifeConstants
from andromeda.core.featureextraction.lifeprocessing.lifebase import LifeBase
from andromeda.core.preprocessing.text.postagger import POSTagger


class WordTagger:

    def __init__(self, config):
        self.adjective_basics_set = set()
        self.adjective_comparatives_set = set()
        self.adjective_superlatives_set = set()
        self.adjective_relevance_set = set()

        LifeBase.init_word_set(self.adjective_basics_set, config['adjective-words-files'])
        LifeBase.init_word_set(self.adjective_comparatives_set, config['comparative-words-files'])
        LifeBase.init_word_set(self.adjective_superlatives_set, config['superlative-words-files'])
        LifeBase.init_word_set(self.adjective_relevance_set, config['adjective-relevance-words-files'])


    def process(self, token_list, token_feature_class):

        for idx, feature_dict in enumerate(token_list):

            token = LifeBase.get_token(token_list, idx)
            token_pos_tag = LifeBase.get_pos_tag(token_list, idx)

            if token_pos_tag == POSTagger.POS_TAG__ADJECTIVE:
                token_pref = LifeBase.get_pos_tag(token_list, idx-1, default='[NONE]')
                adjective_types_list = self._tag_adjective(token, preceeding_word=token_pref)
                WordTagger._set_tags(feature_dict, adjective_types_list)



    def _tag_adjective(self, adjective_word, preceeding_word=''):
        types_set = set()

        adjective_word = adjective_word.lower()

        # Check if comparative or superlative
        if adjective_word in self.adjective_comparatives_set:
            types_set.add(LifeConstants.WORD_TYPE__ADJECTIVE__COMPARATIVE)
        elif adjective_word in self.adjective_superlatives_set or preceeding_word == 'most':
            types_set.add(LifeConstants.WORD_TYPE__ADJECTIVE__SUPERLATIVE)
        elif adjective_word in self.adjective_basics_set:
            if preceeding_word == 'more':
                types_set.add(LifeConstants.WORD_TYPE__ADJECTIVE__COMPARATIVE)
            elif preceeding_word == 'most':
                types_set.add(LifeConstants.WORD_TYPE__ADJECTIVE__SUPERLATIVE)

        # Check if adjective of relevance (e.g., "significant", "important")
        if adjective_word in self.adjective_relevance_set:
            types_set.add(LifeConstants.WORD_TYPE__ADJECTIVE__RELEVANCE)

        return types_set


    @staticmethod
    def _set_tags(feature_dict, tags_list):
        # do nothing of list of tags is empty (no need to clutter the token list)
        if len(tags_list) == 0:
            return
        # Check if corresponding field already existe; if not, add empty list
        if LifeConstants.LIFE__TAG not in feature_dict[LifeConstants.TOKEN_FEATURE__BASE]:
            feature_dict[LifeConstants.TOKEN_FEATURE__BASE][LifeConstants.LIFE__TAG] = []
        # Extend current tags list by the new tags from tags_list
        feature_dict[LifeConstants.TOKEN_FEATURE__BASE][LifeConstants.LIFE__TAG].extend(tags_list)
