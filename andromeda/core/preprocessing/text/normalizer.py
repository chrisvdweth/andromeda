'''
Created on Oct 20, 2016

@author: christian
'''

from andromeda.core.preprocessing.text.normalizing.emotextnormalizer import EmotextNormalizer
from andromeda.core.preprocessing.text.normalizing.emoticonnormalizer import EmoticonNormalizer
from andromeda.core.preprocessing.text.normalizing.exlennormalizer import ExlenNormalizer
from andromeda.core.preprocessing.text.normalizing.segmentnormalizer import SegmentNormalizer
from andromeda.core.preprocessing.text.normalizing.unicodenormalizer import UnicodeNormalizer
from andromeda.core.preprocessing.text.tokenizer import Tokenizer

from andromeda.core.preprocessing.text.normalizing.slangnormalizer import SlangNormalizer


class Normalizer:

    MIN_LEVENSHTEIN_RATIO = 0.7

    TOKEN_CLASS_LIST__ALPHANUM = [Tokenizer.TOKEN_CLASS__ALPHANUM,
                                  Tokenizer.TOKEN_CLASS__ALPHANUM_NEGATION_ABBREVIATION]

    TOKEN_FEATURE__BASE = 'core'
    TOKEN_FEATURE__NORMALIZED = 'normalized'
    TOKEN_FEATURE__DESLANGED = 'deslanged'
    TOKEN_FEATURE__STANDARDIZED = 'standardized'
    TOKEN_FEATURE__SEGMENTED = 'segmented'


    def __init__(self, config):
        self.exlen_normalizer = ExlenNormalizer(config['exlen-files'])
        self.exlen_normalizer_slang = ExlenNormalizer(config['slang-exlen-files'])
        self.slang_normalizer = SlangNormalizer(config['slang-files'])
        self.unicode_normalizer = UnicodeNormalizer(config['unicode-files'])
        self.emotext_normalizer = EmotextNormalizer(config['emotext-files'])
        self.emoticon_normalizer = EmoticonNormalizer()
        self.segment_normalizer = SegmentNormalizer(config['segmenter-files'])





    def normalize(self, token_list, min_levenshtein_ratio=MIN_LEVENSHTEIN_RATIO):

        for feature_dict in token_list:
            token = feature_dict[Tokenizer.TOKEN_FEATURE__BASE][Tokenizer.TOKEN_FEATURE__TOKEN]
            token_class = feature_dict[Tokenizer.TOKEN_FEATURE__BASE][Tokenizer.TOKEN_FEATURE__CLASS]

            # Add empty token feature that will contain all normalizer features
            # (not needed if tokinzer and normalizer etc. share the same "root")
            if Normalizer.TOKEN_FEATURE__BASE not in feature_dict:
                feature_dict[Normalizer.TOKEN_FEATURE__BASE] = {}


            # Set default value to be sure; can be overwritten
            #feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__NORMALIZED] = token

            # Handle ALPHANUM tokeb (can be slang or an emotext!)
            if token_class in Normalizer.TOKEN_CLASS_LIST__ALPHANUM:

                # Check if token is an emotext (e.g., hahaha). If so, go to next token
                is_emotext, token_normalized, token_standardized = self.emotext_normalizer.normalize(token)
                if is_emotext:
                    feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__NORMALIZED] = token_normalized
                    feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__STANDARDIZED] = token_standardized
                    continue

                # Check if token is proper word
                is_normalized, in_proper_word_set, token_normalized = self.exlen_normalizer.normalize(token, min_levenshtein_ratio)
                if is_normalized:
                    feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__NORMALIZED] = token_normalized

                if not in_proper_word_set:
                    is_normalized, in_slang_word_set, token_normalized = self.exlen_normalizer_slang.normalize(token, min_levenshtein_ratio)
                    if is_normalized:
                        feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__NORMALIZED] = token_normalized



                if not in_proper_word_set:
                    is_deslanged, token_deslanged = self.slang_normalizer.normalize(token_normalized)
                    if is_deslanged:
                        feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__DESLANGED] = token_deslanged

            # Handle emoticons
            elif token_class == Tokenizer.TOKEN_CLASS__EMOTICON:
                is_emoticon, is_normalized, token_normalized, token_standardized = self.emoticon_normalizer.normalize(token)
                if is_emoticon:
                    feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__STANDARDIZED] = token_standardized
                    if is_normalized:
                        feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__NORMALIZED] = token_normalized

            # Handle unicode
            elif token_class == Tokenizer.TOKEN_CLASS__UNICODE:
                is_known_unicode, token_normalized = self.unicode_normalizer.normalize(token)
                if is_known_unicode:
                    feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__NORMALIZED] = token_normalized
                    feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__STANDARDIZED] = token_normalized


            elif token_class == Tokenizer.TOKEN_CLASS__SPECIAL_TERM_TOPIC:
                token_stripped = token.replace('#', '')
                is_segmented, token_segmented = self.segment_normalizer.normalize(token_stripped)
                if is_segmented:
                    feature_dict[Normalizer.TOKEN_FEATURE__BASE][Normalizer.TOKEN_FEATURE__SEGMENTED] = token_segmented


        return token_list

if __name__ == "__main__":

    normalizer = Normalizer()
