import numpy as np


class SentilexIndex:

    VALID_WILDCARD__MIN_DEPTH = 3

    def __init__(self):
        self.index = ({}, {})


    def get_average_value(self, word, wildcard_char='*'):
        value_dict = self.__get_value_dict(self.index, list(word), {}, wildcard_char)

        if len(value_dict) == 0:
            return None
        else:
            return np.mean(value_dict.values())


    def get_value_by_lexicon(self, word, lexicon_id, wildcard_char='*'):
        value_dict = self.__get_value_dict(self.index, list(word), {}, wildcard_char)
        if lexicon_id in value_dict:
            return value_dict[lexicon_id]
        else:
            return None


    def add_word(self, word, lexicon_id, sentiment_value, wildcard_char='*'):
        self._add_phrase_to_index(self.index, list(word), lexicon_id, sentiment_value, wildcard_char)


    def _add_phrase_to_index(self, index, character_list, lexicon_id, sentiment_value, wildcard_char='*'):
        if len(character_list) == 0:
            index[1][lexicon_id] = sentiment_value
            return

        if len(character_list) == 1:
            if character_list[0] == wildcard_char:
                index[1][lexicon_id] = sentiment_value

        try:
            character = character_list[0].lower()
            tail = character_list[1:]

            if character in index[0]:
                self._add_phrase_to_index(index[0][character], tail, lexicon_id, sentiment_value)
            else:
                index[0][character] = ({}, {})
                self._add_phrase_to_index(index[0][character], tail, lexicon_id, sentiment_value)
        except Exception, e:
            print e


    def __get_value_dict(self, index, char_list, value_dict, wildcard_char, depth=0):
        try:
            character = char_list[0]
            tail = char_list[1:]

            if wildcard_char in index[0]:
                value_dict = index[0][wildcard_char][1].copy() # Copy needed, otherwise the index get modified by the upadate command later on

            if character in index[0]:
                return self.__get_value_dict(index[0][character], tail, value_dict, wildcard_char, depth=depth+1)
            else:
                if wildcard_char in index[0] and depth >= SentilexIndex.VALID_WILDCARD__MIN_DEPTH:
                    return index[0][wildcard_char][1]
                else:
                    return {}
        except:
            if len(index[1]) == 0:
                return value_dict
            else:
                value_dict.update(index[1])
                return value_dict




if __name__ == "__main__":

    sli = SentilexIndex()

    sli.add_word('(*', 1, -1)
    sli.add_word('ab', 2, -2)
    sli.add_word('ac', 3, -5)
    #sli.add_word('abc', 2, -3)




    #print sli.get_value_by_lexicon('abk', 1)
    print sli.get_average_value('ab')
    #print sli.get_average_value('aXXX')
    #print sli.get_average_value('aXXX')
