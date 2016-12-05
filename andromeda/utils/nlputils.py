import regex as re
import string



class NlpUtils:

    def __init__(self):
        pass

    @staticmethod
    def match_word_capitalization(source_word, target_word):
        result_word = target_word
        if source_word.isupper():
            result_word = result_word.upper()
        elif source_word.islower():
            result_word = result_word.lower()
        elif source_word[0].istitle():
            result_word = string.capwords(result_word)
        return result_word


    @staticmethod
    def replace_repeated_letters(s, min_repeated_count, replace_count):
        replace_string = r''
        for i in range(0, replace_count):
            replace_string += r'\1'
        s = re.sub(r'(.)\1{'+str(min_repeated_count)+',}', replace_string, s)
        return s







#print NlpUtil.replace_repeated_letters('aaawesome', 2, 1)
#print NlpUtil.match_word_capitalization('Yat', 'lOlllO')
