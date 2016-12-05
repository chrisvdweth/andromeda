#!/usr/bin/python
# -*- coding: utf-8 -*-
import falcon
import json
import os

from andromeda.core.preprocessing.text.cleaner import Cleaner
from andromeda.core.preprocessing.text.normalizer import Normalizer
from andromeda.core.preprocessing.text.postagger import POSTagger
from andromeda.core.preprocessing.text.segmenter import Segmenter
from andromeda.core.preprocessing.text.tokenizer import Tokenizer

from andromeda.config import ConfigReader


class TextPreprocessor:

    PROCESSING_LEVEL__TOKENIZE = 0
    PROCESSING_LEVEL__NORMALIZE = 1
    PROCESSING_LEVEL__POSTAG = 2


    def __init__(self):
        self.config = ConfigReader(os.path.join(ConfigReader.CONFIG_DIR, 'textpreprocessor.yaml')).data
        self.cleaner = Cleaner(self.config['cleaner'])
        self.tokenizer = Tokenizer()
        self.segmenter = Segmenter()
        self.normalizer = Normalizer(self.config['normalizer'])
        self.pos_tagger = POSTagger(self.config['pos-tagger'])


    def process(self, s, processing_level=PROCESSING_LEVEL__POSTAG):

        s = self.cleaner.clean(s)

        token_list = self.tokenizer.tokenize(s)

        token_list = self.segmenter.segment(token_list)

        if processing_level == TextPreprocessor.PROCESSING_LEVEL__TOKENIZE:
            return token_list

        token_list = self.normalizer.normalize(token_list)
        if processing_level == TextPreprocessor.PROCESSING_LEVEL__NORMALIZE:
            return token_list

        token_list = self.pos_tagger.tag(token_list)
        if processing_level == TextPreprocessor.PROCESSING_LEVEL__POSTAG:
            return token_list

        return []


    def tokenize(self, s):
        return self.process(s, processing_level=TextPreprocessor.PROCESSING_LEVEL__TOKENIZE)


    def normalize(self, s):
        return self.process(s, processing_level=TextPreprocessor.PROCESSING_LEVEL__NORMALIZE)


    def pos_tag(self, s):
        return self.process(s, processing_level=TextPreprocessor.PROCESSING_LEVEL__POSTAG)





class TextPreprocessorApiResource(object):

    def __init__(self):
        self.text_preprocessor = TextPreprocessor()


    def on_get(self, req, resp, level):
        text = req.get_param('text') or ''

        try:
            text = text.decode('unicode-escape')
        except Exception, e:
            pass # Do nothing in case the string is already in unicode

        token_list = self.text_preprocessor.process(text, processing_level=int(level))

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({ 'token_list' : token_list} )





if __name__ == "__main__":


    s = '@DemoUser Watched Spectre yesterday HAHAHAHA It was good, but not the "masterpiece" everyone had expected :('
    #s = '@DemoUser Can I do it? \U0001F61E \U0001F52B'
    #s = 'peoples\' consumers \'decide on what they really want\': SINGAPORE An elderly customer bought... http://t.co/dwSxPnUbJJ #singapore'
    #s = 'new \'Your Signature Emoji\' feature (http://bla.com)'
    #s = ':\'( :\'( \'test\' yep'
    #s = ':\'( :\'( "test" yes'
    s = u'@Alice \U0001F602 International Baccalaureate\\'


    pp = TextPreprocessor()

    token_list = pp.process(s, processing_level=TextPreprocessor.PROCESSING_LEVEL__TOKENIZE)

    print token_list
