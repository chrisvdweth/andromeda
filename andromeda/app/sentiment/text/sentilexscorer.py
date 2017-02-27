#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os

from andromeda.app.sentiment.text.sentilexindex import SentilexIndex

class SentilexScorer:

    LEXICON_AFINN = 1
    LEXICON_OPINIONOBSERVER = 2
    LEXICON_SENTISTRENGTH = 3
    LEXICON_VADER = 4

    def __init__(self, config):
        self.config = config
        self.lexicon_list = []
        self.sentilex_index = SentilexIndex()


    def initialize_word_lexicons(self, lexicon_list=None):
        self.lexicon_list = lexicon_list
        if lexicon_list is None or SentilexScorer.LEXICON_AFINN in lexicon_list:
            self._initialize_word_lexicon_afinn()
        if lexicon_list is None or SentilexScorer.LEXICON_OPINIONOBSERVER in lexicon_list:
            self._initialize_word_lexicon_opinionobserver()
        if lexicon_list is None or SentilexScorer.LEXICON_SENTISTRENGTH in lexicon_list:
            self._initialize_word_lexicon_sentistrength()
        if lexicon_list is None or SentilexScorer.LEXICON_VADER in lexicon_list:
            self._initialize_word_lexicon_vader()


    def _initialize_word_lexicon_afinn(self):
        try:
            with codecs.open(os.path.expanduser(self.config['sentilex-words-files']['afinn']), encoding='UTF-8') as f:
                for line in f:
                    word, value = line.strip().split('\t')
                    sentiment_value = float(value) / 5.0
                    self.sentilex_index.add_word(word, SentilexScorer.LEXICON_AFINN, sentiment_value)
            f.close()
        except Exception, e:
            print "[Error] SentilexScorer._initialize_word_lexicon_afinn"
            print e


    def _initialize_word_lexicon_opinionobserver(self):
        try:
            with codecs.open(os.path.expanduser(self.config['sentilex-words-files']['opinion-observer']), encoding='UTF-8') as f:
                for line in f:
                    word, value = line.strip().split('\t')
                    sentiment_value = float(value) / 2.0
                    self.sentilex_index.add_word(word, SentilexScorer.LEXICON_OPINIONOBSERVER, sentiment_value)
            f.close()
        except Exception, e:
            print "[Error] SentilexScorer._initialize_word_lexicon_opinionobserver"
            print e


    def _initialize_word_lexicon_sentistrength(self):
        try:
            with codecs.open(os.path.expanduser(self.config['sentilex-words-files']['senti-strength']), encoding='UTF-8') as f:
                for line in f:
                    word, value = line.strip().split('\t')[0:2]
                    sentiment_value = float(value) / 5.0
                    self.sentilex_index.add_word(word, SentilexScorer.LEXICON_SENTISTRENGTH, sentiment_value)
            f.close()
        except Exception, e:
            print "[Error] SentilexScorer._initialize_word_lexicon_sentistrength"
            print e


    def _initialize_word_lexicon_vader(self):
        try:
            with codecs.open(os.path.expanduser(self.config['sentilex-words-files']['vader'])) as f:
                for line in f:
                    word, value = line.strip().split('\t')[0:2]
                    sentiment_value = float(value) / 4.0
                    self.sentilex_index.add_word(word, SentilexScorer.LEXICON_VADER, sentiment_value)
            f.close()
        except Exception, e:
            print "[Error] SentilexScorer._initialize_word_lexicon_vader"
            print e



    def get_score_by_lexicon(self, token, lexicon_id):
        if lexicon_id not in self.lexicon_list:
            self.sentilex_index.get_value_by_lexicon(token, lexicon_id)


    def get_average_score(self, token):
        return self.sentilex_index.get_average_value(token)


