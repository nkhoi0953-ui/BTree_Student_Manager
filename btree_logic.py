from graphviz import Digraph

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

    def insert(self, student):
        # Chèn đệ quy từ root xuống
        self._insert_recursive(self.root, student)
        
        # Nếu sau khi chèn mà Root bị quá tải (3 khóa), thì tách Root
        if len(self.root.keys) > 2:
            new_root = BTreeNode(False)
            new_root.children.append(self.root)
            self._split_node(new_root, 0)
            self.root = new_root

    def _insert_recursive(self, node, student):
        if node.leaf:
            # Chèn tạm thời vào lá (có thể lên tới 3 khóa)
            node.keys.append(student.ma_sv)
            node.values.append(student)
            
            # Sắp xếp lại danh sách khóa và giá trị theo Mã SV
            combined = sorted(zip(node.keys, node.values), key=lambda x: x[0])
            node.keys, node.values = [list(t) for t in zip(*combined)]
        else:
            # Tìm đường xuống con phù hợp
            i = 0
            while i < len(node.keys) and student.ma_sv > node.keys[i]:
                i += 1
            
            self._insert_recursive(node.children[i], student)
            
            # Sau khi con chèn xong, kiểm tra nếu con bị quá tải thì tách ngay
            if len(node.children[i].keys) > 2:
                self._split_node(node, i)

    def _split_node(self, parent, i):
        node_to_split = parent.children[i]
        new_node = BTreeNode(node_to_split.leaf)
        
        # Với bậc 3: Index 1 là khóa giữa sẽ được đưa lên cha
        mid_key = node_to_split.keys[1]
        mid_val = node_to_split.values[1]
        
        # Phần bên phải (index 2) sẽ sang node mới
        new_node.keys = [node_to_split.keys[2]]
        new_node.values = [node_to_split.values[2]]
        
        if not node_to_split.leaf:
            new_node.children = node_to_split.children[2:]
            node_to_split.children = node_to_split.children[:2]
            
        # Phần bên trái (index 0) ở lại node cũ
        node_to_split.keys = [node_to_split.keys[0]]
        node_to_split.values = [node_to_split.values[0]]
        
        # Đưa khóa giữa lên parent
        parent.keys.insert(i, mid_key)
        parent.values.insert(i, mid_val)
        parent.children.insert(i + 1, new_node)


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


    def get_graphviz_source(self):
        dot = Digraph(comment='B-Tree Index')
        dot.attr('node', shape='record', style='filled', fillcolor='lightblue')
        
        if self.root:
            self._build_graph(self.root, dot)
        return dot

    def _build_graph(self, node, dot):
        
        node_id = str(id(node))
        label = " | ".join(map(str, node.keys))
        dot.node(node_id, label=f"{{ {label} }}")
        
        # Nếu không phải lá, vẽ mũi tên đến các con
        if not node.leaf:
            for i, child in enumerate(node.children):
                child_id = str(id(child))
                self._build_graph(child, dot)
                dot.edge(node_id, child_id)
        

    
