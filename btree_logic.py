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
        root = self.root
        # Nếu Root đã có 2 khóa, phải tách Root để tăng chiều cao cây
        if len(root.keys) == 2:
            new_root = BTreeNode(False)
            self.root = new_root
            new_root.children.insert(0, root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, student)
        else:
            self._insert_non_full(root, student)

    def _insert_non_full(self, node, student):
        i = len(node.keys) - 1
        if node.leaf:
            # Chèn vào lá và giữ thứ tự tăng dần của Mã SV
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and student.ma_sv < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
            node.keys[i+1] = student.ma_sv
            node.values[i+1] = student
        else:
            # Tìm con phù hợp để xuống
            while i >= 0 and student.ma_sv < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2:
                self._split_child(node, i)
                if student.ma_sv > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], student)

    def _split_child(self, parent, i):
        m = self.m
        full_node = parent.children[i]
        new_node = BTreeNode(full_node.leaf)
        
        # Bậc 3: Lấy khóa ở giữa (index 1) đẩy lên cha
        mid_key = full_node.keys[1]
        mid_val = full_node.values[1]
        
        # Node mới nhận phần bên phải (khóa index 2)
        if len(full_node.keys) > 2:
            new_node.keys = [full_node.keys[2]]
            new_node.values = [full_node.values[2]]
        
        if not full_node.leaf:
            new_node.children = full_node.children[2:]
            full_node.children = full_node.children[:2]

        # Cập nhật node cũ (chỉ giữ lại khóa index 0)
        full_node.keys = [full_node.keys[0]]
        full_node.values = [full_node.values[0]]

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