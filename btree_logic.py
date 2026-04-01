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
    

    def delete(self, k):
        if not self.root.keys:
            return
        
        self._delete_recursive(self.root, k)
        
        # Nếu sau khi xóa mà Root rỗng, hãy kéo con lên làm Root mới
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]
        # Nếu Root là lá và rỗng, vẫn giữ nguyên là 1 node lá rỗng

    def _delete_recursive(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == k:
            if node.leaf:
                node.keys.pop(i)
                node.values.pop(i)
            else:
                self._delete_from_internal(node, i)
        else:
            if node.leaf:
                return # Không tìm thấy
            
            # TRƯỚC KHI XUỐNG CON: Nếu con quá nghèo (chỉ có 1 khóa), phải fill nó ngay
            if len(node.children[i].keys) < 1:
                self._fill(node, i)
            
            # Sau khi fill, vị trí i có thể đã thay đổi
            if i > len(node.keys):
                self._delete_recursive(node.children[i-1], k)
            else:
                self._delete_recursive(node.children[i], k)

    def _delete_from_internal(self, node, i):
        k = node.keys[i]
        left = node.children[i]
        right = node.children[i+1]

        # Chỉ mượn từ con nếu con đó có dư (với m=3 là có > 1 khóa)
        if len(left.keys) > 1:
            pred_key, pred_val = self._get_predecessor(left)
            node.keys[i] = pred_key
            node.values[i] = pred_val
            self._delete_recursive(left, pred_key)
        elif len(right.keys) > 1:
            succ_key, succ_val = self._get_successor(right)
            node.keys[i] = succ_key
            node.values[i] = succ_val
            self._delete_recursive(right, succ_key)
        else:
            # Cả hai đều nghèo (chỉ có 1 khóa) -> GỘP
            self._merge(node, i)
            self._delete_recursive(left, k)

    def _fill(self, parent, i): 
        if i != 0 and len(parent.children[i-1].keys) > 1:
            self._borrow_from_prev(parent, i)
        elif i != len(parent.keys) and len(parent.children[i+1].keys) > 1:
            self._borrow_from_next(parent, i)
        else:
            if i != len(parent.keys):
                self._merge(parent, i)
            else:
                self._merge(parent, i-1)

    def _get_predecessor(self, node):
        curr = node
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1], curr.values[-1]

    def _get_successor(self, node):
        curr = node
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0], curr.values[0]

    def _borrow_from_prev(self, parent, i):
        child = parent.children[i]
        sibling = parent.children[i-1]
        
        child.keys.insert(0, parent.keys[i-1])
        child.values.insert(0, parent.values[i-1])
        parent.keys[i-1] = sibling.keys.pop(-1)
        parent.values[i-1] = sibling.values.pop(-1)
        
        if not child.leaf:
            child.children.insert(0, sibling.children.pop(-1))

    def _borrow_from_next(self, parent, i):
        child = parent.children[i]
        sibling = parent.children[i+1]
        
        child.keys.append(parent.keys[i])
        child.values.append(parent.values[i])
        parent.keys[i] = sibling.keys.pop(0)
        parent.values[i] = sibling.values.pop(0)
        
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, parent, i):
        left = parent.children[i]
        right = parent.children[i+1]
        
        left.keys.append(parent.keys.pop(i))
        left.values.append(parent.values.pop(i))
        left.keys.extend(right.keys)
        left.values.extend(right.values)
        
        if not left.leaf:
            left.children.extend(right.children)
            
        parent.children.pop(i+1)
        

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
    
