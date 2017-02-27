import os

from andromeda.util import NlpUtil


class SlangNormalizer:

    def __init__(self, input_file_names_list):
        self.slang_dict = {}

        for input_file_name in input_file_names_list:
            self._init_slang_dict(input_file_name)


    def _init_slang_dict(self, input_file_name):
        with open(os.path.expanduser(input_file_name), 'r') as f:
            for line in f:
                line = line.strip()
                try:
                    short_form, long_form = line.split('\t')
                    self.slang_dict[short_form] = long_form
                except Exception, e:
                    pass



    def normalize(self, word):

        try:
            deslanged = self.slang_dict[word.lower()]
        except KeyError:
            deslanged = None

        if deslanged is not None:
            # Match cepitalization as good as possible
            return True, NlpUtil.match_word_capitalization(word, deslanged)

        return False, deslanged







if __name__ == "__main__":

    normalizer = SlangNormalizer(['/home/christian/work/development/git/sesame-social/somesing/data/vocabulary-files/inet-slangs-words.txt'])


    print normalizer.normalize('WTF')


