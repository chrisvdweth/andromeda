from andromeda.util import NlpUtil
from andromeda.core.indexing import PrefixIndex


class LocationCandidateExtractor:

    MAX_PHRASE_LENGTH = 5

    def __init__(self, config):
        self.config = config
        self.prefix_index = PrefixIndex(input_file_name_list=config['location-name-prefix-trie-file-list'],
                                        ingored_prefix_tokens_file_name_list=config['prefix-trie-ignored-prefixes-file-list'])



    def find_all(self, s, max_match_count):
        s = NlpUtil.simplify_location_name_phrase(s)

        word_list = s.split()

        key_lists_dict = {}
        longest_matches_dict = {}
        backlink_dict = {}
        last_match_phrase = ''

        for start_pos in range(len(word_list)):

            for end_pos in range(start_pos, start_pos+LocationCandidateExtractor.MAX_PHRASE_LENGTH):
                if end_pos >= len(word_list):
                    break

                phrase = ' '.join(word_list[start_pos:end_pos+1])

                match_phrase, key_list = self.prefix_index.lookup_phrase(phrase)

                if match_phrase is None:
                    continue

                if match_phrase.lower() == last_match_phrase.lower():
                    continue
                last_match_phrase = match_phrase

                # If match phrase contains only stopwords => ignore
                if all(NlpUtil.is_stop_word(w.lower()) for w in match_phrase.split()):
                    continue


                if len(match_phrase) > 0:
                    if end_pos not in backlink_dict:
                        key_lists_dict[(start_pos,end_pos)] = key_list
                        backlink_dict[end_pos] = start_pos

                    if len(key_list) > max_match_count:
                        continue

                    if backlink_dict[end_pos] >= start_pos:
                        longest_matches_dict[start_pos] = (end_pos+1, match_phrase)

        result_list = []
        for start_pos, val in longest_matches_dict.iteritems():
            result_list.append((start_pos, val[0], val[1], key_lists_dict[(start_pos, val[0]-1)]))

        return result_list

