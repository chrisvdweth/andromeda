import math

from andromeda.utils import NlpUtils


def memoize(f):
    cache = {}

    def memoizedFunction(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    memoizedFunction.cache = cache
    return memoizedFunction




class SegmentNormalizer:

    def __init__(self, word_list_file_name_list):
        self.word_probabilities = WordDistribution(word_list_file_name_list)


    def normalize(self, s):
        segment_list = self.segment(s)
        segment = ' '.join(segment_list)

        # Match the original capitalization as good as possible
        segment = NlpUtils.match_word_capitalization(s, segment)

        if len(segment_list) == 1:
            return False, segment
        else:
            return True, segment


    @memoize
    def segment(self, word):
        if not word: return []
        #word = word.lower() # change to lower case
        all_segmentations = [[first] + self.segment(rest) for (first,rest) in self.split_pairs(word.lower())]
        return max(all_segmentations, key = self.word_sequence_score)


    def split_pairs(self, word, maxLen=20):
        return [(word[:i+1], word[i+1:]) for i in range(max(len(word), maxLen))]

    @memoize
    def segment_with_probability(self, word):
        segmented = self.segment(word)
        return (self.word_sequence_score(segmented), segmented)


    def word_sequence_score(self, words):
        return sum(math.log10(self.word_probabilities(w)) for w in words)




class WordDistribution(dict):

    def __init__(self, word_list_file_name_list):
        self.gramCount = 0

        for word_list_file_name in word_list_file_name_list:
            for line in open(word_list_file_name):
                (word, count) = line[:-1].split('\t')
                self[word] = int(count)
                self.gramCount += self[word]


    def __call__(self, key):
        if key in self:
            return float(self[key]) / self.gramCount
        else:
            return 1.0 / (self.gramCount * 10**(len(key)-2))







if __name__ == '__main__':

    segment_normalizer = SegmentNormalizer(['/home/christian/work/development/git/sesame-social/somesing/data/vocabulary-files/english-segmenter-words.text'])

    print segment_normalizer.normalize("NotFunny")
