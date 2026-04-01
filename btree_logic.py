class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []      
        self.values = []    
        self.children = []  

class BTree:
    def __init__(self, m=3):
        self.root = BTreeNode(True)
        self.m = m  # m=3

    def search(self, k, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return node.values[i]
        if node.leaf:
            return None
        return self.search(k, node.children[i])