import Levenshtein
import re
import os

import soundex

from andromeda.util import NlpUtil


class ExlenNormalizer:


    def __init__(self, word_file_names_list):
        self.nlp_util = NlpUtil()
        self.soundex = soundex.getInstance()
        self.soundex_dict = {}
        self.word_set = set()

        #self.pattern_min_repetition = re.compile(r"\b\w*([a-zA-Z0-9])\1\1+\w+\b", re.IGNORECASE)
        self.pattern_min_repetition = re.compile(r"\b\w*([a-zA-Z0-9])\1\1+\w*\b", re.IGNORECASE)

        for word_file_name in word_file_names_list:
            self._initialize_soundex_dict(word_file_name)



    def _initialize_soundex_dict(self, word_file_name, comment='#'):
        self.soundex_dict = {}
        with open(os.path.expanduser(word_file_name), 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith(comment):
                    continue

                word = line.split('\t')[0].lower()
                self.word_set.add(word)
                try:
                    soundex_code = self.soundex.soundex(word, 10)
                    if soundex_code in self.soundex_dict:
                        self.soundex_dict[soundex_code].add(word)
                    else:
                        s = set()
                        s.add(word)
                        self.soundex_dict[soundex_code] = s
                except Exception, e:
                    pass



    def normalize(self, word, min_levensthein_ratio):

        in_word_set = False
        if word.lower() in self.word_set:
            in_word_set = True

        # Check if word is not empty
        if len(word) == 0:
            return False, in_word_set, word

        # Check if word has at least 3 repeated Characters
        match_list = re.findall(self.pattern_min_repetition, word)

        # If not match, then no (obvious) expressive lengthenings found => return input word
        if len(match_list) == 0:
            return False, in_word_set, word

        # Preprocess word
        word_processed = word.strip().lower()

        # Replace 2+ repeated letters by 2 letters -- cannot hurt in the very most cases
        word_processed = self.nlp_util.replace_repeated_letters(word_processed, 2, 2)
        candidate_list = self._calculate_candidate_list(word_processed, min_levensthein_ratio)

        # Reduce now to 1 repeated character + merge lists
        word_processed = self.nlp_util.replace_repeated_letters(word_processed, 1, 1)
        candidate_list = candidate_list + self._calculate_candidate_list(word_processed, min_levensthein_ratio)

        # Return original word if there are no candidates
        if len(candidate_list) == 0:
            return False, in_word_set, word

        candidate_list = sorted(candidate_list, key=lambda x:x[1], reverse=True)
        result_word = candidate_list[0][0] # If still multiple matches, give priority to standard English words

        # Match the original capitalization as good as possible
        result_word = NlpUtil.match_word_capitalization(word, result_word)

        in_word_set = False
        if result_word.lower() in self.word_set:
            in_word_set = True

        return True, in_word_set, result_word



    def _calculate_candidate_list(self, word, min_levensthein_ratio):
        soundex_code = self.soundex.soundex(word, 10)

        if soundex_code in self.soundex_dict:
            word_list = list(self.soundex_dict[soundex_code])
        else:
            return [(word, 0.0)]

        # Remove all candidates that do not contain the same basic letter sequence.
        # For example, "netter" has "neater" as candidate, but "neter" != "neater"
        word_minimized = self.nlp_util.replace_repeated_letters(word, 1, 1)
        word_list_minimized = [w.lower() for w in word_list if word_minimized == NlpUtil.replace_repeated_letters(w, 1, 1)]

        # Calculate Levenshtein similarities for each word in word_list with input word
        similarities  = [(word, Levenshtein.ratio(str(word), str(w))) for w in word_list_minimized]

        # Filter results given max similarity
        similarities[:] = [tup for tup in similarities if tup[1] >= min_levensthein_ratio]

        # if now words a similar enough, return empty list
        if len(similarities) == 0:
            return []

        # Sort results according to distances/similarity
        similarities = sorted(similarities, key=lambda x:x[1], reverse=True)

        # Get max similarity
        max_similarity = similarities[0][1]

        # Filter  results given max similarity and return list
        return [tup for tup in similarities if tup[1] == max_similarity]






if __name__ == "__main__":

    #sc = ExlenNormalizer(['/home/christian/work/development/git/sesame-social/somesing/data/vocabulary-files/english-lowercase.text'])
    sc = ExlenNormalizer(['/home/christian/work/development/git/sesame-social/somesing/data/vocabulary-files/inet-slangs-words.txt'])

    sentence = 'WTFF WTFFFF LOOOL WTFFF'
    word_list = sentence.split()

    word_list_checked = []
    for word in word_list:
        word_checked = sc.normalize(word, 0.7)
        print word_checked
        word_list_checked.append(word_checked[1])

    sentence_checked = ' '.join(word_list_checked)

    print sentence, '=>', sentence_checked

