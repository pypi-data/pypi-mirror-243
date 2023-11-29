class TrieNode:
    # Class variable for unique identifier
    _identifier_counter = 0

    def __init__(self):
        self.identifier = TrieNode._identifier_counter
        TrieNode._identifier_counter += 1

        self.children = {}
        self.parent = None
        self.freq_and_word = None

    def __eq__(self, other):
        if isinstance(other, TrieNode):
            return self.identifier == other.identifier
        return False

    def __hash__(self):
        return hash(self.identifier)

    def get_freq_and_word_of_all_leaf_nodes(self):
        result = []

        if self.freq_and_word is not None:
            result.append(self.freq_and_word)

        for child in self.children.values():
            result.extend(child.get_freq_and_word_of_all_leaf_nodes())

        return result


def build_trie(corpus_words, corpus_freq):
    root = TrieNode()
    root.parent = None
    word_freq = dict(zip(corpus_words, corpus_freq))

    for word, freq in word_freq.items():
        node = root
        for i, char in enumerate(word):
            if char not in node.children:
                node.children[char] = TrieNode()
                node.children[char].parent = node
            node = node.children[char]

            if i == len(word) - 1:
                node.freq_and_word = (freq, word)

    return root


def update_valid_nodes(old_valid_nodes, new_char_list, root):
    new_valid_nodes = []

    if not old_valid_nodes:
        for new_char in new_char_list:
            if new_char in root.children:
                new_valid_nodes.append(root.children[new_char])
    else:
        for valid_node in old_valid_nodes:
            for new_char in new_char_list:
                if new_char in valid_node.children:
                    new_valid_nodes.append(valid_node.children[new_char])

    return new_valid_nodes


def get_autocomplete_candidates(valid_nodes, max_candidates, alpha):
    if not valid_nodes:
        return []

    freq_and_word_list = []
    for node in valid_nodes:
        freq_and_word_list.extend(node.get_freq_and_word_of_all_leaf_nodes())

    user_input_len = calc_node_depth(valid_nodes[0])
    alpha_applied = [
        (apply_alpha_penalty(freq, len(word), user_input_len, alpha), word)
        for freq, word in freq_and_word_list
    ]

    alpha_applied.sort(key=lambda x: x[0], reverse=True)
    return [word for _, word in alpha_applied[:max_candidates]]


def apply_alpha_penalty(freq, target_word_len, user_input_len, alpha):
    return freq * alpha ** (target_word_len - user_input_len)


def calc_node_depth(node):
    count = 0
    current_node = node
    while current_node.parent is not None:
        count += 1
        current_node = current_node.parent
    return count
