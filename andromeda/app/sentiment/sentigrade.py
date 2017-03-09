import os
import re
import json
import falcon
from andromeda.util import  TokenListUtil
from andromeda.config import ConfigReader
from andromeda.core.featureextraction import LifeProcessor
from andromeda.app.sentiment.text.sentiscorecalculator import SentiScoreCalculator


class Sentigrade:

    METHOD__LEXICON_SCORING = 0

    def __init__(self):
        self.config = ConfigReader(os.path.join(ConfigReader.CONFIG_DIR, 'sentigrade.yaml')).data

        self.life_processor = LifeProcessor()
        self.senti_score_calculator = SentiScoreCalculator(self)


    def process(self, s):
        token_list = self.life_processor.process(s)
        self.senti_score_calculator.process(token_list)
        return token_list




class SentigradeApiResource(object):

    def __init__(self):
        self.sentigrade = Sentigrade()


    def on_get(self, req, resp):
        text = req.get_param('text') or ''
        method = req.get_param('text') or ''

        try:
            method = int(method)
        except:
            method = Sentigrade.METHOD__LEXICON_SCORING

        try:
            text = text.decode('unicode-escape')
        except Exception, e:
            pass # Do nothing in case the string is already in unicode

        text = re.sub(' +',' ', text).strip()

        if method == Sentigrade.METHOD__LEXICON_SCORING:
            data_json = self.sentigrade.process(text)
        else:
            data_json = {}

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps( data_json )





if __name__ == "__main__":

    sentigrade = Sentigrade()

    s = u"This was a horrible luck."

    token_list = sentigrade.process(s)
    for idx, _ in enumerate(token_list):
        token = TokenListUtil.get_token(token_list, idx)
        score = TokenListUtil.get_sentiment_score(token_list, idx)
        print token, score
