from andromeda.core.featureextraction.lifeprocessing.lifebase import LifeBase
from andromeda.core.featureextraction.lifeprocessing.lifeconstants import LifeConstants


class Negation:

    def __init__(self, config):
        self.negation_word_set = set()
        self.negation_delimiter_word_set = set()
        self.negation_inhibitor_word_set = set()
        self.negation_nonscope_word_set = set()

        LifeBase.init_word_set(self.negation_word_set, config['negation-words-files'])
        LifeBase.init_word_set(self.negation_delimiter_word_set, config['negation-delimiter-words-files'])
        LifeBase.init_word_set(self.negation_inhibitor_word_set, config['negation-inhibitor-words-files'])
        LifeBase.init_word_set(self.negation_nonscope_word_set, config['negation-nonscope-words-files'])

        # Just to be sure; might already be added as part of the input file
        self.negation_word_set.add("n't")



    def process(self, token_list, token_feature_class):

        do_negate = False
        scope_size = 0

        for idx, feature_dict in enumerate(token_list):
            token = LifeBase.get_token(token_list, idx).lower()
            token_class = LifeBase.get_token_class(token_list, idx)
            token_pos_tag = LifeBase.get_pos_tag(token_class, idx)

            # Get the preceding token
            next_token = LifeBase.get_token(token_list, idx+1, default='')

            # Check if do_negate has to be set to False (if it was True at this point)
            do_negate = self._do_negate(do_negate, token, token_class, token_pos_tag, scope_size)

            # Reset size of negation scope if negation has ended
            if not do_negate:
                scope_size = 0

            if do_negate and token_class in LifeConstants.NEGATED_WORD_TOKEN_CLASSES:
                # Set information that token is considered to be negated
                feature_dict[LifeConstants.TOKEN_FEATURE__BASE][token_feature_class] = 1
                # Ignore auxiliary verbs etc. when determining the size of the scope
                if token not in self.negation_nonscope_word_set:
                    scope_size += 1

            # Check if word is a negtion word (e.g., not)
            if token in self.negation_word_set:
                # No common, but a negation can negate a negation
                if do_negate:
                    do_negate = False
                # Check if negation can be stopped "prematurely"
                elif next_token not in self.negation_inhibitor_word_set:
                    do_negate = True
                # Some handcrafted special case
                bigram = token + ' ' + next_token
                if bigram in ["can't wait"]:
                    do_negate = False



    def _do_negate(self, do_negate, token, token_class, token_pos_tag, scope_size):
        # If the negtion scope has reached maximim size, stop negating
        if scope_size >= LifeConstants.NEGATION_MAX_SCOPE_SIZE:
            return False

        # If token is "context-splitting" (e.g., punctuation mark, url, email, hashtag), stop negating
        if token_class in LifeConstants.NEGATION_BOUNDARY_TOKEN_CLASSES or token_pos_tag in LifeConstants.NEGATION_BOUNDARY_POS_TAGS:
            if token_class not in LifeConstants.NEGATION_BOUNDARY_TOKEN_EXCEPTION_CLASSES:
                return False

        # If token is a "context-splitting" word (e.g., "but", "unless"), stop negating
        if token in self.negation_delimiter_word_set:
            return False

        # As default, return the current state of do_negate (note that we only check if has to be set to False)
        return do_negate
