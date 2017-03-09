import requests
import os
from andromeda.util import NlpUtil


class SolrSearchHandler:

    MAX_PHRASE_LENGTH = 5

    def __init__(self, config):
        self._ignored_prefixes_list = set()
        self._init_ignored_prefix_tokens_from_file(config['prefix-trie-ignored-prefixes-file-list'])
        self._solr_url = config['base-url']


    def process(self, query_phrase_list, location_candidate_phrases_list):
        phrases_list = ([ '"%s"' % tup for tup in query_phrase_list])
        phrases_list.extend([ p.replace(' ', '') for p in phrases_list])
        q_str = ' '.join(list(set(phrases_list)))

        fq_str = ''
        prefix_str = '|'.join(self._ignored_prefixes_list)
        if len(prefix_str) == 0:
            fq_str += ' OR '.join([ 'name_indexed:/'+l[2].replace(' ', '[ ]*')+'.*/' for l in location_candidate_phrases_list])
        else:
            fq_str += ' OR '.join([ 'name_indexed:/(^|'+'|'.join(self._ignored_prefixes_list)+')*[ ]*'+l[2].replace(' ', '[ ]*')+'.*/' for l in location_candidate_phrases_list])

        #fq_str = ''
        search_result_list = self._search(q_str, fq_str, 999999)

        return search_result_list



    def find_all(self, s, max_match_count):
        s = NlpUtil.simplify_location_name_phrase(s)

        word_list = s.split()

        key_lists_dict = {}
        tag_lists_dict = {}
        longest_matches_dict = {}
        backlink_dict = {}

        for start_pos in range(len(word_list)):

            for end_pos in range(start_pos, start_pos+SolrSearchHandler.MAX_PHRASE_LENGTH):
                if end_pos >= len(word_list):
                    break

                phrase = ' '.join(word_list[start_pos:end_pos+1])

                # If match phrase contains only stopwords => ignore
                if all(NlpUtil.is_stop_word(w.lower()) for w in phrase.split()):
                    continue

                q_str = "name_indexed:/.*" + '[ ]*'.join(word_list[start_pos:end_pos+1]) + ".*/"

                result_list = self._search(q_str, "", 1000)

                if len(result_list) > 0 and len(result_list) <= max_match_count:
                    if end_pos not in backlink_dict:
                        key_lists_dict[(start_pos,end_pos)] = [r['id'] for r in result_list]
                        tag_lists_dict[(start_pos,end_pos)] = [r['tags'] for r in result_list]
                        backlink_dict[end_pos] = start_pos
                    if backlink_dict[end_pos] >= start_pos:
                        longest_matches_dict[start_pos] = (end_pos+1, phrase)

                else:
                    continue



        result_list = []
        for start_pos, val in longest_matches_dict.iteritems():
            result_list.append((start_pos, val[0], val[1], key_lists_dict[(start_pos, val[0]-1)], tag_lists_dict[(start_pos, val[0]-1)]))

        return result_list






    def _search(self, q_str, fq_str, limit):
        try:
            r = requests.get("{}/closeupplaces/select?q={}&fq={}&rows={}&wt=json".format(self._solr_url, q_str, fq_str, limit))
            return r.json()['response']['docs']
        except Exception, e:
            print e
            return []


    def _init_ignored_prefix_tokens_from_file(self, ingored_prefix_tokens_file_name_list):
        # Set set of ignored prefixes to empty set
        self._ignored_prefix_tokens_set = set()

        # Do nothing if no list is given
        if ingored_prefix_tokens_file_name_list is None:
            return
        # Do nothing if no list is empty
        if len(ingored_prefix_tokens_file_name_list) == 0:
            return
        # Otherwise, go through list and handle each file name
        for ingored_prefix_words_file_name in ingored_prefix_tokens_file_name_list:
            with open(os.path.expanduser(ingored_prefix_words_file_name), 'r') as f:
                for line in f:
                    line = line.strip().lower()
                    if line.startswith('#'):
                        continue
                    self._ignored_prefix_tokens_set.add(line)




if __name__ == "__main__":

    solr_search_handler = SolrSearchHandler({ 'prefix-trie-ignored-prefixes-file-list' : ['~/andromeda-data/indexer-files/prefix-trie-ignored-prefix-words.txt'], 'base-url' : 'http://localhost:8983/solr'})

    q = ["bbrrww", "at", "marina", "bay", "sands", "open", "now"]
    q = ['time', 'kinokuniya', 'queue', 'time']
    q = ['time', 'kinokuniya', 'queue']
    #q = ["time singapore flyer"]

    print ' '.join(q)
    search_result_list = solr_search_handler.process(q, [])
    for search_result in search_result_list:
        print search_result
    #result_list = solr_search_handler.find_all(' '.join(q), 1000)
    #for result in result_list:
    #    print result
