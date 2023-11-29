from wordpredict.utils import (
    build_trie,
    get_autocomplete_candidates,
    update_valid_nodes,
)


class WordPredict:
    def __init__(self, corpus_words, corpus_freq, alpha=0.62):
        self.root = build_trie(corpus_words, corpus_freq)
        self.alpha = alpha
        self.valid_nodes = []

    def update(self, new_char_list, max_candidates=6):
        if new_char_list:
            self.valid_nodes = update_valid_nodes(
                self.valid_nodes, new_char_list, self.root
            )
        return get_autocomplete_candidates(self.valid_nodes, max_candidates, self.alpha)

    def reset(self):
        self.valid_nodes = []

    def get_current_candidates(self, max_candidates=6):
        return get_autocomplete_candidates(self.valid_nodes, max_candidates, self.alpha)

    def undo(self, max_candidates=6):
        if not self.valid_nodes:
            return []

        if self.valid_nodes[0].parent.identifier == self.root.identifier:
            self.valid_nodes = []
            return []
        else:
            unique_parents = {node.parent for node in self.valid_nodes}
            self.valid_nodes = list(unique_parents)
            return get_autocomplete_candidates(
                self.valid_nodes, max_candidates, self.alpha
            )
