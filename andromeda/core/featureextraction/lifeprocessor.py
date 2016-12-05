import os
import json
import falcon

from andromeda.config import ConfigReader
from andromeda.core.preprocessing import TextPreprocessor
from andromeda.core.featureextraction.lifeprocessing.lifeconstants import LifeConstants
from andromeda.core.featureextraction.lifeprocessing.allcaps import AllCaps
from andromeda.core.featureextraction.lifeprocessing.negation import Negation
from andromeda.core.featureextraction.lifeprocessing.wordtagger import WordTagger
from andromeda.core.featureextraction.lifeprocessing.adjectivenounpairs import AdjectiveNounPairs
from andromeda.core.featureextraction.lifeprocessing.quotation import Quotation


class LifeProcessor:

    def __init__(self):
        self.config = ConfigReader(os.path.join(ConfigReader.CONFIG_DIR, 'lifeprocessor.yaml')).data
        self.text_preprocessor = TextPreprocessor()

        self.negation = Negation(self.config['negation'])
        self.word_tagger = WordTagger(self.config['word-tagger'])


    def process(self, s, life_rules_set=None):
        token_list = self.text_preprocessor.process(s)

        for feature_dict in token_list:
            feature_dict[LifeConstants.TOKEN_FEATURE__BASE] = {}

        if life_rules_set is None or LifeConstants.LIFE__ALL_CAPS in life_rules_set:
            AllCaps.process(token_list, LifeConstants.LIFE__ALL_CAPS)

        if life_rules_set is None or LifeConstants.LIFE__NEGATION in life_rules_set:
            self.negation.process(token_list, LifeConstants.LIFE__NEGATION)

        if life_rules_set is None or LifeConstants.LIFE__ANP in life_rules_set:
            AdjectiveNounPairs.process(token_list, LifeConstants.LIFE__ANP)

        if life_rules_set is None or LifeConstants.LIFE__TAG in life_rules_set:
            self.word_tagger.process(token_list, LifeConstants.LIFE__TAG)

        if life_rules_set is None or LifeConstants.LIFE__QUOTED in life_rules_set:
            Quotation.process(token_list, LifeConstants.LIFE__QUOTED)

        return token_list




class LifeProcessorApiResource(object):

    def __init__(self):
        self.life_processor = LifeProcessor()


    def on_get(self, req, resp):
        text = req.get_param('text') or ''

        try:
            text = text.decode('unicode-escape')
        except Exception, e:
            pass # Do nothing in case the string is already in unicode

        token_list = self.life_processor.process(text, life_rules_set=None)

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({ 'token_list' : token_list} )





if __name__ == '__main__':

    life = LifeProcessor()


    s = 'The "weekend" was "nicer and better".'

    life_rules_set = set(['allcaps', 'neg', 'anp', 'tag', 'quoted'])

    print life.process(s)
