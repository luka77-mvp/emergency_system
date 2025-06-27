class HeapPriorityQueue:
    """使用二叉堆实现的优先队列（最小堆）"""
    
    def __init__(self, max_size=1000):
        """
        初始化空的优先队列
        
        参数:
            max_size: 堆的最大容量，默认为1000
        """
        self.max_size = max_size
        self.heap = [None]  # 索引0不使用，从索引1开始
        self.count = 0  # 当前堆中的元素数量
        self.id_to_index = {}  # 用于快速查找：紧急情况ID -> 堆索引
    
    def is_empty(self):
        """检查队列是否为空"""
        return self.count == 0
    
    def enqueue(self, item):
        """
        将项目添加到优先队列中
        
        参数:
            item: 要添加的紧急情况对象
        """
        # 检查堆是否已满
        if self.count >= self.max_size:
            raise Exception("优先队列已满")
        
        # 1. 将新项目添加到堆的末尾
        self.count += 1
        if len(self.heap) <= self.count:
            self.heap.append(item)
        else:
            self.heap[self.count] = item
        
        # 更新ID到索引的映射
        self.id_to_index[item.emergency_id] = self.count
        
        # 2. 通过"上浮"操作恢复堆属性
        self._shift_up(self.count)
    
    def _shift_up(self, index):
        """
        上浮操作 (bubble up)，将新添加的元素移动到正确的位置
        
        参数:
            index: 要上浮的元素索引
        """
        # 当索引大于1（不是根节点）时，比较与父节点的优先级
        if index > 1:
            parent = index // 2
            # 如果当前元素优先级高于父元素，则交换位置并继续上浮
            if self._is_higher_priority(index, parent):
                self._swap(index, parent)
                self._shift_up(parent)
    
    def dequeue(self):
        """
        移除并返回最高优先级的项目（堆顶元素）
        
        返回:
            最高优先级的紧急情况对象，如果队列为空则返回None
        """
        if self.is_empty():
            return None
        
        # 1. 保存最高优先级的项目（根节点）
        highest_priority_item = self.heap[1]
        del self.id_to_index[highest_priority_item.emergency_id]
        
        # 2. 将最后一个元素移动到根位置
        self.heap[1] = self.heap[self.count]
        self.id_to_index[self.heap[1].emergency_id] = 1
        
        # 3. 减少堆大小
        self.count -= 1
        
        # 4. 通过"下沉"操作恢复堆属性
        if self.count > 0:  # 如果堆不为空
            self._shift_down(1)
        
        return highest_priority_item
    
    def peek(self):
        """
        查看最高优先级的项目但不移除它
        
        返回:
            最高优先级的紧急情况对象，如果队列为空则返回None
        """
        if self.is_empty():
            return None
        return self.heap[1]
    
    def _shift_down(self, index):
        """
        下沉操作 (shift down)，将根部元素移动到正确的位置
        
        参数:
            index: 要下沉的元素索引
        """
        if index <= self.count:
            # 计算左右子节点的索引
            left = 2 * index
            right = 2 * index + 1
            smallest = index
            
            # 找出当前节点、左子节点和右子节点中的最高优先级（最小严重度）
            if left <= self.count and self._is_higher_priority(left, smallest):
                smallest = left
            
            if right <= self.count and self._is_higher_priority(right, smallest):
                smallest = right
            
            # 如果子节点中有更高优先级的，则交换位置并继续下沉
            if smallest != index:
                self._swap(index, smallest)
                self._shift_down(smallest)
    
    def _is_higher_priority(self, index1, index2):
        """
        比较两个索引上的元素的优先级。
        严重性越小，优先级越高。如果严重性相同，ID越小，优先级越高。
        
        参数:
            index1, index2: 要比较的两个元素的索引
            
        返回:
            如果索引1对应的元素优先级高于索引2的元素，则返回True
        """
        item1 = self.heap[index1]
        item2 = self.heap[index2]
        
        # 首先按严重程度比较（值越小，优先级越高）
        if item1.severity_level < item2.severity_level:
            return True
        # 严重程度相同时，按ID比较
        elif item1.severity_level == item2.severity_level and item1.emergency_id < item2.emergency_id:
            return True
        
        return False

    def _swap(self, i, j):
        """
        交换堆中两个元素的位置，并更新其在id_to_index映射中的索引
        
        参数:
            i, j: 要交换的元素索引
        """
        # 更新ID到索引的映射
        self.id_to_index[self.heap[i].emergency_id] = j
        self.id_to_index[self.heap[j].emergency_id] = i
        
        # 交换元素
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def search(self, emergency_id):
        """
        搜索具有指定ID的紧急情况
        
        参数:
            emergency_id: 要搜索的紧急情况ID
            
        返回:
            找到的紧急情况对象，如果未找到则返回None
        """
        if emergency_id in self.id_to_index:
            index = self.id_to_index[emergency_id]
            return self.heap[index]
        return None
    
    def change_priority(self, emergency_id, new_severity):
        """
        更改指定ID紧急情况的优先级
        
        参数:
            emergency_id: 要更改优先级的紧急情况ID
            new_severity: 新的严重程度值
            
        返回:
            布尔值，表示操作是否成功
        """
        if emergency_id not in self.id_to_index:
            return False
        
        index = self.id_to_index[emergency_id]
        old_severity = self.heap[index].severity_level
        self.heap[index].severity_level = new_severity
        
        # 根据优先级变化，执行上浮或下沉操作
        if new_severity < old_severity:  # 优先级提高
            self._shift_up(index)
        else:  # 优先级降低
            self._shift_down(index)
        
        return True
    
    def __len__(self):
        """返回队列中的元素数量"""
        return self.count
    
    def __iter__(self):
        """
        使队列可迭代。注意：这不会按优先级顺序返回。
        """
        for i in range(1, self.count + 1):
            yield self.heap[i]