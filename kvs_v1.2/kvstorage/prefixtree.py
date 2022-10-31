class PrefixTree:
    class TreeNode:
        def __init__(self, char: str = None):
            self.char = char
            self.children = {}
            self.is_word = False

    def __init__(self, words):
        self.root = PrefixTree.TreeNode()
        for word in words:
            self.add_word(word)

    def add_word(self, word: str) -> None:
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = PrefixTree.TreeNode(char)
            current = current.children[char]
        current.is_word = True

    def contains_full_word(self, word: str) -> bool:
        return self.get_node(word).is_word is True

    def starts_with(self, prefix: str) -> list:
        node = self.get_node(prefix)
        if node is None:
            return []
        return list(self.get_words(prefix[:-1], node))

    def get_words(self, prefix: str, node) -> list:
        prefix += str(node.char)
        if node.is_word:
            yield prefix
        if node.children is None:
            return
        for child_node in node.children.values():
            for word in self.get_words(prefix, child_node):
                yield word
        prefix = prefix[:-1]

    def get_node(self, prefix: str) -> TreeNode:
        current = self.root
        for char in prefix:
            if char not in current.children:
                return None
            current = current.children[char]
        return current
