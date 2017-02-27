import sys
import os

from andromeda.app.closeup.text.solrsearchhandler import SolrSearchHandler


class LocationExtractionHandler:

    def __init__(self, config):
        #self.location_candidate_extractor = LocationCandidateExtractor(config['location-candidate-extractor'])
        self.solr_search_handler = SolrSearchHandler(config['solr-search-handler'])
        self._init_commom_words_set(config['location-extraction-handler']['common-words-file-list'])



    def _init_commom_words_set(self, common_words_file_name_list):
        self._common_words_set = set()
        for file_name in common_words_file_name_list:
            with open(os.path.expanduser(file_name), 'r') as f:
                for line in f:
                    word = line.lower().strip().split()[0]
                    self._common_words_set.add(word)


    def process(self, query_str, limit=100):
        # Ignore phrases (not sure if this is a good idea)
        q = query_str.replace('"', '')
        # Get all location candidates using the prefix trie index
        #location_candidates_list = self.location_candidate_extractor.find_all(q, sys.maxint)
        #print location_candidates_list
        location_candidates_list = self.solr_search_handler.find_all(q, sys.maxint)

        # Regenerate the query as list of phrases = location candidates + rest
        query_phrase_list = self._generate_query_phrase_list(q, location_candidates_list, matches_only=True)

        #self._filter_location_cadidates(location_candidates_list)

        search_result_list = self.solr_search_handler.process(query_phrase_list, location_candidates_list)

        #search_result_list = self._filter_solr_search_results(search_result_list)

        search_result_list = search_result_list[:limit]

        return [ { 'name' : r['name'][0], 'id' : r['id'], 'ploc' : { 'lat' : float(r['lat'][0]), 'lng' : float(r['lng'][0]) }, 'tags' : r['tags'] } for r in search_result_list ]



    def _generate_query_phrase_list(self, q, location_candidates_list, matches_only=False):
        # Create copy to ignore the long list of keys
        query_phrases_list = [ (c[0], c[1], c[2]) for c in location_candidates_list ]

        if matches_only is True:
            return [ c[2] for c in query_phrases_list ]

        # Split query into terms
        terms_list = q.split()
        # Extract all pairs if range(start,end) for each location candidate
        range_pairs_list = [ range(c[0], c[1]) for c in query_phrases_list ]
        # Flatten list into a set of all term positions that hold (parts of) a location candidate
        covered_term_pos_set = set([item for sublist in range_pairs_list for item in sublist])
        # Add "leftover" terms as fake location candidates with their position to the list
        leftover_terms_list = []
        for pos, term in enumerate(terms_list):
            if pos not in covered_term_pos_set:
                leftover_terms_list.append((pos, pos+1, term))
                #query_phrases_list.append((pos, pos+1, term))
        # Filter out noisy search terms from list of leftover terms
        leftover_terms_list = self._filter_search_terms(leftover_terms_list)
        # Add leftover terms to list of location candidates
        query_phrases_list.extend(leftover_terms_list)
        # Sort location candidates with respect to order of appearance in query string (as good as possible)
        query_phrases_list.sort(key=lambda tup: tup[0])
        # Return final query as set of phrases and terms
        return query_phrases_list



    def _filter_search_terms(self, search_term_list):
        for i in xrange(len(search_term_list) - 1, -1, -1):
            search_term = search_term_list[i][2]
            if search_term.lower() in self._common_words_set:
                del search_term_list[i]
        return search_term_list


    def _filter_location_cadidates(self, location_cadidates_list):
        print location_cadidates_list


