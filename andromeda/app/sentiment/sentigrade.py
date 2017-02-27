import os
from andromeda.util import  TokenListUtil
from andromeda.config import ConfigReader
from andromeda.core.featureextraction import LifeProcessor
from andromeda.app.sentiment.text.sentiscorecalculator import SentiScoreCalculator


class Sentigrade:

    def __init__(self):
        self.config = ConfigReader(os.path.join(ConfigReader.CONFIG_DIR, 'sentigrade.yaml')).data

        self.life_processor = LifeProcessor()
        self.senti_score_calculator = SentiScoreCalculator(self)


    def process(self, s):
        token_list = self.life_processor.process(s)
        self.senti_score_calculator.process(token_list)
        return token_list


if __name__ == "__main__":

    sentigrade = Sentigrade()

    s = u"This was a horrible luck."

    token_list = sentigrade.process(s)
    for idx, _ in enumerate(token_list):
        token = TokenListUtil.get_token(token_list, idx)
        score = TokenListUtil.get_sentiment_score(token_list, idx)
        print token, score
