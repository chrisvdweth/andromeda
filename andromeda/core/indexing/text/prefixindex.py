import os

class PrefixIndex:

    def __init__(self, do_lower_case=True, **kwargs):
        self._do_lower_case = do_lower_case
        self._wildcard_char_set = {" ", "'", "."}


        if 'ingored_prefix_tokens_file_name_list' in kwargs:
            self._init_ignored_prefix_tokens_from_file(kwargs['ingored_prefix_tokens_file_name_list'])
        elif 'ingored_prefix_tokens_list' in kwargs:
            self._init_ignored_prefix_tokens_from_list(kwargs['ingored_prefix_tokens_list'])

        if 'input_file_name_list' in kwargs:
            self._create_index_from_file(kwargs['input_file_name_list'])
        elif 'input_list' in kwargs:
            self._create_index_from_list(kwargs['input_list'])





    def _create_index_from_file(self, input_file_name_list):
        # Initial prefix trie data structure
        self.index = ({}, set())

        if input_file_name_list is None:
            return

        if len(input_file_name_list) == 0:
            return

        # Go through all files
        for input_file_name in input_file_name_list:
            with open(os.path.expanduser(input_file_name), 'r') as f:
                for line in f:
                    line = line.strip()
                    if line[0] == '#': # Ignored commented lines
                        continue
                    line_elememts = line.split('\t')

                    try:
                        phrase = line_elememts[0]
                        key = line_elememts[1]

                        if self._do_lower_case:
                            phrase = phrase.lower()

                        self._handle_phrase(phrase, key)
                    except:
                        pass





    def _create_index_from_list(self, input_list):
        # Initial prefix trie data structure
        self.index = ({}, set())

        if input_list is None:
            return

        if len(input_list) == 0:
            return

        # Go through list of tuples (string, key)
        for tup in input_list:
            try:
                phrase = tup[0]
                key = tup[1]

                if self._do_lower_case:
                    phrase = phrase.lower()

                self._handle_phrase(phrase, key)
            except:
                pass



    def _handle_phrase(self, phrase, key):
        try:
            # Add whole phrase to index (default step)
            self._add_phrase_to_index(self.index, list(phrase), key)

            # Add all tails with successively ignored prefix tokens
            token_list = phrase.split()
            while True:
                first_token = token_list[0]
                if first_token.lower() in self.ignored_prefix_tokens_set:
                    token_list = token_list[1:]
                    if len(token_list) == 0:
                        break
                    indexed_phrase = ' '.join(token_list)
                    self._add_phrase_to_index(self.index, list(indexed_phrase), key)
                else:
                    break

        except Exception, e:
            print phrase
            print e



    def get_index_entries(self, phrase):
        if self._do_lower_case:
            phrase = phrase.lower()
        match_phrase, entries_list = self.lookup_phrase(phrase)
        if phrase == match_phrase:
            return entries_list
        return []


    def is_in_index(self, phrase):
        if self._do_lower_case:
            phrase = phrase.lower()
        match_phrase, _ = self.lookup_phrase(phrase)
        if phrase == match_phrase:
            return True
        return False


    def lookup_phrase(self, phrase):
        # Minimize phrase => remove ignored prefixes
        phrases_list = self._generated_alternative_phrase(phrase)
        #print '>>>', phrases_list
        for phrase in phrases_list:
            # Lowercase phrase if that is the setting
            if self._do_lower_case:
                phrase = phrase.lower()
            # Ignore phrase if it contains only ignored prefix tokens
            if not self._is_valid_phrase(phrase):
                continue
            # Do actual lookup
            #print "Lookup:", phrase
            match_phrase, key_list = self._lookup_phrase(self.index, list(phrase), '')
            # If longer phrase already yields a non-empty resuly, we can stop
            if len(key_list) > 0:
                return match_phrase, key_list

        return None, set([])




    def _lookup_phrase(self, index, character_list, matching_prefix_str):
        try:
            # Get first character (head) and rest (tail) of character list, throws exception if empty
            head, tail = character_list[0], character_list[1:]
            #print head, tail
            # Check if first character (head) is in index, if so continue recursively
            if head in index[0]:
                matching_prefix_str += head
                return self._lookup_phrase(index[0][head], tail, matching_prefix_str)
            elif head in self._wildcard_char_set:
                # "Special case": phrase contains a wildcard character that might be wrong (e.g., "Vivo City" instead of "Vivocity")
                # => make a new lookup with same phrase but removed wildcard
                match_phrase, key_list = self.lookup_phrase(matching_prefix_str+''.join(tail))
                if len(match_phrase) > len(matching_prefix_str):
                    return match_phrase.strip(), key_list
                else:
                    return self.lookup_phrase(matching_prefix_str)
            else:
                # "Special case": if wildcard is index at this position
                # "jump over it" and continue recursively
                char_interesect = set(index[0].keys()).intersection(self._wildcard_char_set)
                if len(char_interesect):
                    wildcard_char = next(iter(char_interesect))
                    #return self._lookup_phrase(index[0][wildcard_char], character_list, matching_prefix_str+wildcard_char)
                    return self._lookup_phrase(index[0][wildcard_char], character_list, matching_prefix_str)
                else:
                    # "Special case": if last character is a whitespace, the prefix up this point is in the index
                    # => make new lookup over valid prefix which is bound to succeed
                    return self.lookup_phrase(self._short_prefix(matching_prefix_str))

        # Exaception if there is no head anymore => end of string
        except:
            # if there are no keys for the full phrase, return for the next shortest valid prefix
            if len(index[1]) == 0:
                return self.lookup_phrase(self._short_prefix(matching_prefix_str))
            # Otherwise, return the prefix that matched and the non-empty list of keys
            else:
                return matching_prefix_str.strip(), index[1]


    def _short_prefix(self, prefix_str):
        s = prefix_str
        while len(s) > 0:
            if s[-1] not in self._wildcard_char_set:
                s = s[0:-1]
            else:
                break
        return s.strip()



    def _generated_alternative_phrase(self, phrase):
        # Add original phrase to result list
        phrases_list = [phrase]
        token_list = phrase.split()
        while True:
            try:
                head, token_list = token_list[0], token_list[1:]
                # If firs token (head) is an ignored prefix token, tail is a valid alternative to consider
                if head.lower() in self.ignored_prefix_tokens_set:
                    tail_phrase = ' '.join(token_list).strip()
                    # Double-check if tail phrase is indeed valid
                    if self._is_valid_phrase(tail_phrase):
                        phrases_list.append(' '.join(token_list))
                else:
                    # After the first "not-ignored" token, we are done
                    return phrases_list
            except:
                # Is thrown when end of phrase is reached
                return phrases_list
        # Just for safety; should not be called ever
        return phrases_list



    def _is_valid_phrase(self, phrase):
        # Return FALSE if phrase is None
        if phrase is None:
            return False
        # Return FALSE if phrase is empty string
        if len(phrase) == 0:
            return False
        # Return FALSE if phrase consists only of ignored prefix tokens
        token_list = phrase.split()
        if len(self.ignored_prefix_tokens_set.intersection(set(token_list))) == len(token_list):
            return False
        # Return TRUE otherwise
        return True


    def _add_phrase_to_index(self, index, character_list, key):
        # If at the end of the phrase, add key to current index position -- and then done
        if len(character_list) == 0:
            index[1].add(key)
            return

        try:
            # Get first character (head) and rest (tail) of non-empty character list
            head, tail = character_list[0], character_list[1:]
            # "Special case": store key for each prefix of words (i.e., at whitespaces)
            #if head == " ":
            if head in self._wildcard_char_set:
                index[1].add(key)
            # If first character (head) does exist at this position in the index, create new sub-trie entry here
            if head not in index[0]:
                index[0][head] = ({}, set())
            # Recusrsively keep adding phrase to index
            self._add_phrase_to_index(index[0][head], tail, key)

        except Exception, e:
            print e


    def _init_ignored_prefix_tokens_from_file(self, ingored_prefix_tokens_file_name_list):
        # Set set of ignored prefixes to empty set
        self.ignored_prefix_tokens_set = set()

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
                    self.ignored_prefix_tokens_set.add(line)


    def _init_ignored_prefix_tokens_from_list(self, ingored_prefix_tokens_list):
        # Set set of ignored prefixes to empty set
        self.ignored_prefix_tokens_set = set()

        # Do nothing if no list is given
        if ingored_prefix_tokens_list is None:
            return
        # Do nothing if no list is empty
        if len(ingored_prefix_tokens_list) == 0:
            return
        # Otherwise, go through list and handle each file name
        for token in ingored_prefix_tokens_list:
            self.ignored_prefix_tokens_set.add(token.lower())




if __name__ == "__main__":

    pi = PrefixIndex(input_file_name_list=['/home/christian/data/app-data/google-places/google-places-names-prefix-trie.txt'],
                     ingored_prefix_tokens_file_name_list=['/home/christian/data/app-data/google-places/prefix-trie-ignored-prefix-words.txt'])

    #example_list = [('vivocity', '1'), ('marina bay sands', '2')]
    #ignored_list = ['the', 'singapore', 'hotel']

    #pi = PrefixIndex(input_list=example_list, ingored_prefix_tokens_list=ignored_list)

    result_list =  pi.lookup_phrase("vivo city")
    #match_phrase, key_list =  pi.lookup_phrase("waiting")
    print result_list

    #match_phrase, candidate_phrases =  pi.lookup_phrase('McDonald\'s Sentosa')
    #print match_phrase, candidate_phrases
