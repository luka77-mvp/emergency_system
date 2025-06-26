class TreeNode:
    """二叉搜索树节点类"""
    
    def __init__(self, data):
        """
        初始化二叉搜索树节点
        
        参数:
            data: 节点存储的数据（Emergency对象）
        """
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    """标准二叉搜索树实现"""
    
    def __init__(self):
        """初始化空的二叉搜索树"""
        self.root = None
        self.size = 0
    
    def is_empty(self):
        """检查树是否为空"""
        return self.root is None
    
    def insert(self, item):
        """
        将项目插入到二叉搜索树中
        
        参数:
            item: 要添加的紧急情况对象
            
        搜索树规则:
            - 节点的左子树只包含严重程度小于（优先级高于）当前节点的节点
            - 节点的右子树只包含严重程度大于（优先级低于）当前节点的节点
        """
        self.size += 1
        
        # 如果树为空，创建根节点
        if self.is_empty():
            self.root = TreeNode(item)
            return
        
        # 否则，使用迭代方式找到合适的插入位置
        self._insert_iterative(item)
    
    def _insert_iterative(self, item):
        """
        迭代方式插入节点
        
        参数:
            item: 要插入的紧急情况对象
        """
        current = self.root
        
        while True:
            # 如果新项目严重程度小于（优先级高于）当前节点，放在左子树
            if item < current.data:
                if current.left is None:
                    current.left = TreeNode(item)
                    return
                else:
                    current = current.left
            # 如果新项目严重程度大于（优先级低于）当前节点，放在右子树
            elif item > current.data:
                if current.right is None:
                    current.right = TreeNode(item)
                    return
                else:
                    current = current.right
            # 如果严重程度相同，我们按照ID递增排序
            else:
                if item.emergency_id < current.data.emergency_id:
                    if current.left is None:
                        current.left = TreeNode(item)
                        return
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = TreeNode(item)
                        return
                    else:
                        current = current.right
    
    def get_min(self):
        """
        获取树中优先级最高（严重程度数值最小）的项目
        
        返回:
            优先级最高的紧急情况对象，如果树为空则返回None
        """
        if self.is_empty():
            return None
        
        # 在二叉搜索树中，最小值总是在最左边的叶子节点
        current = self.root
        while current.left:
            current = current.left
            
        return current.data
    
    def remove_min(self):
        """
        移除并返回优先级最高（严重程度数值最小）的项目
        
        返回:
            优先级最高的紧急情况对象，如果树为空则返回None
        """
        if self.is_empty():
            return None
            
        min_item = self.get_min()
        self.remove(min_item.emergency_id)
        return min_item
    
    def search_by_id(self, emergency_id):
        """
        根据ID搜索紧急情况
        
        参数:
            emergency_id: 要搜索的紧急情况ID
            
        返回:
            找到的紧急情况对象，如果未找到则返回None
        """
        if self.root is None:
            return None
        
        # 需要执行完整的树搜索，因为二叉搜索树是按严重程度组织的，不是ID
        return self._search_by_id_bfs(emergency_id)
    
    def _search_by_id_bfs(self, emergency_id):
        """
        使用广度优先搜索，根据ID查找紧急情况
        
        参数:
            emergency_id: 要搜索的紧急情况ID
            
        返回:
            找到的紧急情况对象，如果未找到则返回None
        """
        if self.root is None:
            return None
        
        # 创建队列用于BFS
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            
            # 检查当前节点
            if node.data.emergency_id == emergency_id:
                return node.data
            
            # 将子节点添加到队列
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # 未找到
        return None
    
    def search_by_severity(self, severity):
        """
        搜索具有指定严重程度的紧急情况
        
        参数:
            severity: 要搜索的严重程度级别
            
        返回:
            找到的紧急情况对象列表，如果未找到则返回空列表
        """
        results = []
        self._search_by_severity_recursive(self.root, severity, results)
        return results
    
    def _search_by_severity_recursive(self, node, severity, results):
        """
        递归搜索具有指定严重程度的节点
        
        参数:
            node: 当前节点
            severity: 要搜索的严重程度级别
            results: 结果列表
        """
        if node is None:
            return
        
        # 利用二叉搜索树的特性进行剪枝
        if node.data.severity_level == severity:
            results.append(node.data)
            # 可能有同样严重程度的紧急情况在左右子树
            self._search_by_severity_recursive(node.left, severity, results)
            self._search_by_severity_recursive(node.right, severity, results)
        elif severity < node.data.severity_level:
            # 如果要搜索的严重程度小于当前节点，只需搜索左子树
            self._search_by_severity_recursive(node.left, severity, results)
        else:
            # 如果要搜索的严重程度大于当前节点，只需搜索右子树
            self._search_by_severity_recursive(node.right, severity, results)
    
    def update_severity(self, emergency_id, new_severity):
        """
        更新指定ID紧急情况的严重程度
        
        参数:
            emergency_id: 要更新的紧急情况ID
            new_severity: 新的严重程度值
            
        返回:
            布尔值，表示操作是否成功
        """
        # 在二叉搜索树中，更新键值需要先删除后插入
        emergency = self.remove(emergency_id)
        
        # 如果未找到，返回失败
        if not emergency:
            return False
        
        # 更新严重程度
        emergency.severity_level = new_severity
        
        # 重新插入
        self.insert(emergency)
        return True
    
    def remove(self, emergency_id):
        """
        从树中移除指定ID的紧急情况
        
        参数:
            emergency_id: 要移除的紧急情况ID
            
        返回:
            找到并移除的紧急情况对象，如果未找到则返回None
        """
        if self.is_empty():
            return None
        
        # 先找到带删除的节点和其父节点
        emergency, parent, is_left_child, current = self._find_node_and_parent(emergency_id)
        
        # 如果未找到，返回None
        if not current:
            return None
            
        self.size -= 1
        
        # 执行删除操作
        self._delete_node(parent, current, is_left_child)
        
        return emergency
    
    def _find_node_and_parent(self, emergency_id):
        """
        查找指定ID的节点及其父节点
        
        参数:
            emergency_id: 要查找的紧急情况ID
            
        返回:
            (emergency, parent, is_left_child, current) 元组
        """
        if self.root is None:
            return None, None, False, None
        
        parent = None
        current = self.root
        is_left_child = False
        emergency = None
        
        # 广度优先搜索查找节点
        queue = []
        queue.append((None, self.root, False))
        
        while queue:
            parent, current, is_left = queue.pop(0)
            
            if current.data.emergency_id == emergency_id:
                emergency = current.data
                return emergency, parent, is_left, current
            
            if current.left:
                queue.append((current, current.left, True))
            
            if current.right:
                queue.append((current, current.right, False))
        
        return None, None, False, None
    
    def _delete_node(self, parent, node, is_left_child):
        """
        删除指定的节点
        
        参数:
            parent: 要删除节点的父节点
            node: 要删除的节点
            is_left_child: 指示节点是否为其父节点的左子节点
        """
        # 情况1: 叶子节点
        if node.left is None and node.right is None:
            if node == self.root:
                self.root = None
            elif is_left_child:
                parent.left = None
            else:
                parent.right = None
        
        # 情况2: 只有一个子节点
        elif node.left is None:
            if node == self.root:
                self.root = node.right
            elif is_left_child:
                parent.left = node.right
            else:
                parent.right = node.right
        elif node.right is None:
            if node == self.root:
                self.root = node.left
            elif is_left_child:
                parent.left = node.left
            else:
                parent.right = node.left
        
        # 情况3: 有两个子节点
        else:
            # 查找中序后继（右子树中的最小节点）
            successor, successor_parent = self._find_min_node_and_parent(node.right, node)
            
            # 保存后继节点的数据
            node.data = successor.data
            
            # 删除后继节点
            if successor_parent == node:
                node.right = successor.right
            else:
                successor_parent.left = successor.right
    
    def _find_min_node_and_parent(self, node, parent):
        """
        查找以给定节点为根的子树中的最小值节点及其父节点
        
        参数:
            node: 子树的根节点
            parent: node的父节点
            
        返回:
            (min_node, parent) 元组
        """
        current = node
        parent_node = parent
        
        while current.left:
            parent_node = current
            current = current.left
            
        return current, parent_node
    
    def __len__(self):
        """返回树中的节点数量"""
        return self.size
    
    def __iter__(self):
        """使树可迭代，按照中序遍历（升序）返回节点"""
        if self.root is None:
            return iter([])
        
        # 使用迭代方式的中序遍历
        return self._inorder_traversal_iterative()
    
    def _inorder_traversal_iterative(self):
        """
        迭代方式的中序遍历
        
        返回:
            中序遍历结果列表
        """
        result = []
        stack = []
        current = self.root
        
        while current or stack:
            # 到达最左边的节点
            while current:
                stack.append(current)
                current = current.left
            
            # 弹出栈顶节点并处理
            current = stack.pop()
            result.append(current.data)
            
            # 处理右子树
            current = current.right
        
        return iter(result)
    
    def print_tree(self):
        """
        打印树的结构（用于调试）
        """
        if self.root is None:
            print("空树")
            return
            
        self._print_tree_recursive(self.root, 0)
        
    def _print_tree_recursive(self, node, level):
        """
        递归打印树结构
        
        参数:
            node: 当前节点
            level: 当前层级
        """
        if node:
            self._print_tree_recursive(node.right, level + 1)
            print(' ' * 4 * level + '-> ' + str(node.data))
            self._print_tree_recursive(node.left, level + 1)


# 为了兼容旧代码，保留原来的类名，但实现使用新的二叉搜索树
class BinaryTreePriorityQueue(BinarySearchTree):
    """使用二叉搜索树实现的优先队列（兼容层）"""
    
    def enqueue(self, item):
        """将项目添加到优先队列"""
        self.insert(item)
        
    def dequeue(self):
        """移除并返回最高优先级的项目"""
        return self.remove_min()
        
    def search(self, emergency_id):
        """搜索具有指定ID的紧急情况"""
        return self.search_by_id(emergency_id)
        
    def change_priority(self, emergency_id, new_severity):
        """更改指定ID紧急情况的优先级"""
        return self.update_severity(emergency_id, new_severity)