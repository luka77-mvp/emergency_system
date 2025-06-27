import time
import random
import matplotlib.pyplot as plt

from ..data_structures.emergency import Emergency, EmergencyType

class PerformanceAnalyzer:
    """性能分析器，用于比较不同优先队列实现的性能"""
    
    def __init__(self, linked_list_queue, binary_tree_queue, heap_queue):
        """
        初始化性能分析器
        
        参数:
            linked_list_queue: 链表优先队列实例
            binary_tree_queue: 二叉树优先队列实例
            heap_queue: 堆优先队列实例
        """
        self.linked_list_queue = linked_list_queue
        self.binary_tree_queue = binary_tree_queue
        self.heap_queue = heap_queue
        self.results = {}
    
    def generate_random_emergencies(self, count):
        """
        生成随机紧急情况数据
        
        参数:
            count: 要生成的紧急情况数量
            
        返回:
            随机生成的紧急情况对象列表
        """
        emergencies = []
        emergency_types = [EmergencyType.FIRE, EmergencyType.MEDICAL, EmergencyType.POLICE]
        locations = ["Downtown", "Suburbs", "City Center", "Industrial Area", "Residential Area"]
        
        for i in range(count):
            emergency_id = i + 1
            emergency_type = random.choice(emergency_types)
            severity_level = random.randint(1, 10)
            location = random.choice(locations)
            
            emergency = Emergency(
                emergency_id=emergency_id,
                emergency_type=emergency_type,
                severity_level=severity_level,
                location=location
            )
            
            emergencies.append(emergency)
        
        return emergencies
    
    def measure_enqueue_performance(self, data_sizes):
        """
        测量入队操作性能
        
        参数:
            data_sizes: 要测试的数据大小列表
            
        返回:
            包含三种队列类型的性能测试结果的字典
        """
        results = {
            'linked_list': [],
            'binary_tree': [],
            'heap': []
        }
        
        for size in data_sizes:
            # 生成随机紧急情况
            emergencies = self.generate_random_emergencies(size)
            
            # 执行多次测量并取平均值以提高准确性
            repeat_count = 5
            
            # 测量链表入队性能
            linked_list_total = 0
            for _ in range(repeat_count):
                # 确保队列为空
                while not self.linked_list_queue.is_empty():
                    self.linked_list_queue.dequeue()
                
                start_time = time.perf_counter()  # 使用高精度计时器
                for emergency in emergencies:
                    self.linked_list_queue.enqueue(emergency)
                end_time = time.perf_counter()
                linked_list_total += (end_time - start_time)
            
            linked_list_time = linked_list_total / repeat_count
            results['linked_list'].append(linked_list_time)
            
            # 测量二叉树入队性能
            binary_tree_total = 0
            for _ in range(repeat_count):
                # 确保队列为空
                while not self.binary_tree_queue.is_empty():
                    self.binary_tree_queue.dequeue()
                    
                start_time = time.perf_counter()
                for emergency in emergencies:
                    self.binary_tree_queue.enqueue(emergency)
                end_time = time.perf_counter()
                binary_tree_total += (end_time - start_time)
            
            binary_tree_time = binary_tree_total / repeat_count
            results['binary_tree'].append(binary_tree_time)
            
            # 测量堆入队性能
            heap_total = 0
            for _ in range(repeat_count):
                # 确保队列为空
                while not self.heap_queue.is_empty():
                    self.heap_queue.dequeue()
                    
                start_time = time.perf_counter()
                for emergency in emergencies:
                    self.heap_queue.enqueue(emergency)
                end_time = time.perf_counter()
                heap_total += (end_time - start_time)
            
            heap_time = heap_total / repeat_count
            results['heap'].append(heap_time)
            
            print(f"数据大小: {size}, 链表: {linked_list_time:.6f} 秒, 二叉树: {binary_tree_time:.6f} 秒, 堆: {heap_time:.6f} 秒")
            
            # 清空队列
            while not self.linked_list_queue.is_empty():
                self.linked_list_queue.dequeue()
            while not self.binary_tree_queue.is_empty():
                self.binary_tree_queue.dequeue()
            while not self.heap_queue.is_empty():
                self.heap_queue.dequeue()
        
        self.results['enqueue'] = results
        return results
    
    def measure_dequeue_performance(self, data_sizes):
        """
        测量出队操作性能
        
        参数:
            data_sizes: 要测试的数据大小列表
            
        返回:
            包含三种队列类型的性能测试结果的字典
        """
        results = {
            'linked_list': [],
            'binary_tree': [],
            'heap': []
        }
        
        for size in data_sizes:
            # 执行多次测量并取平均值以提高准确性
            repeat_count = 5
            
            # 测量链表出队性能
            linked_list_total = 0
            for _ in range(repeat_count):
                # 准备数据
                emergencies = self.generate_random_emergencies(size)
                
                # 填充链表队列
                for emergency in emergencies:
                    self.linked_list_queue.enqueue(emergency)
                
                # 测量出队时间
                start_time = time.perf_counter()
                for _ in range(size):
                    if not self.linked_list_queue.is_empty():
                        self.linked_list_queue.dequeue()
                end_time = time.perf_counter()
                linked_list_total += (end_time - start_time)
            
            linked_list_time = linked_list_total / repeat_count
            results['linked_list'].append(linked_list_time)
            
            # 测量二叉树出队性能
            binary_tree_total = 0
            for _ in range(repeat_count):
                # 准备数据
                emergencies = self.generate_random_emergencies(size)
                
                # 填充二叉树队列
                for emergency in emergencies:
                    self.binary_tree_queue.enqueue(emergency)
                
                # 测量出队时间
                start_time = time.perf_counter()
                for _ in range(size):
                    if not self.binary_tree_queue.is_empty():
                        self.binary_tree_queue.dequeue()
                end_time = time.perf_counter()
                binary_tree_total += (end_time - start_time)
            
            binary_tree_time = binary_tree_total / repeat_count
            results['binary_tree'].append(binary_tree_time)
            
            # 测量堆出队性能
            heap_total = 0
            for _ in range(repeat_count):
                # 准备数据
                emergencies = self.generate_random_emergencies(size)
                
                # 填充堆队列
                for emergency in emergencies:
                    self.heap_queue.enqueue(emergency)
                
                # 测量出队时间
                start_time = time.perf_counter()
                for _ in range(size):
                    if not self.heap_queue.is_empty():
                        self.heap_queue.dequeue()
                end_time = time.perf_counter()
                heap_total += (end_time - start_time)
            
            heap_time = heap_total / repeat_count
            results['heap'].append(heap_time)
            
            print(f"数据大小: {size}, 链表: {linked_list_time:.6f} 秒, 二叉树: {binary_tree_time:.6f} 秒, 堆: {heap_time:.6f} 秒")
        
        self.results['dequeue'] = results
        return results
    
    def measure_search_performance(self, data_sizes):
        """
        测量搜索操作性能
        
        参数:
            data_sizes: 要测试的数据大小列表
            
        返回:
            包含三种队列类型的性能测试结果的字典
        """
        results = {
            'linked_list': [],
            'binary_tree': [],
            'heap': []
        }
        
        for size in data_sizes:
            # 执行多次测量并取平均值以提高准确性
            repeat_count = 5
            
            # 测量链表搜索性能
            linked_list_total = 0
            for _ in range(repeat_count):
                # 准备数据
                emergencies = self.generate_random_emergencies(size)
                search_target = emergencies[random.randint(0, len(emergencies)-1)]
                
                # 填充链表队列
                for emergency in emergencies:
                    self.linked_list_queue.enqueue(emergency)
                
                # 测量搜索时间
                start_time = time.perf_counter()
                found = search_target in self.linked_list_queue
                end_time = time.perf_counter()
                linked_list_total += (end_time - start_time)
                
                # 清空队列
                while not self.linked_list_queue.is_empty():
                    self.linked_list_queue.dequeue()
            
            linked_list_time = linked_list_total / repeat_count
            results['linked_list'].append(linked_list_time)
            
            # 测量二叉树搜索性能
            binary_tree_total = 0
            for _ in range(repeat_count):
                # 准备数据
                emergencies = self.generate_random_emergencies(size)
                search_target = emergencies[random.randint(0, len(emergencies)-1)]
                
                # 填充二叉树队列
                for emergency in emergencies:
                    self.binary_tree_queue.enqueue(emergency)
                
                # 测量搜索时间
                start_time = time.perf_counter()
                found = search_target in self.binary_tree_queue
                end_time = time.perf_counter()
                binary_tree_total += (end_time - start_time)
                
                # 清空队列
                while not self.binary_tree_queue.is_empty():
                    self.binary_tree_queue.dequeue()
            
            binary_tree_time = binary_tree_total / repeat_count
            results['binary_tree'].append(binary_tree_time)
            
            # 测量堆搜索性能
            heap_total = 0
            for _ in range(repeat_count):
                # 准备数据
                emergencies = self.generate_random_emergencies(size)
                search_target = emergencies[random.randint(0, len(emergencies)-1)]
                
                # 填充堆队列
                for emergency in emergencies:
                    self.heap_queue.enqueue(emergency)
                
                # 测量搜索时间
                start_time = time.perf_counter()
                found = search_target in self.heap_queue
                end_time = time.perf_counter()
                heap_total += (end_time - start_time)
                
                # 清空队列
                while not self.heap_queue.is_empty():
                    self.heap_queue.dequeue()
            
            heap_time = heap_total / repeat_count
            results['heap'].append(heap_time)
            
            print(f"数据大小: {size}, 链表: {linked_list_time:.6f} 秒, 二叉树: {binary_tree_time:.6f} 秒, 堆: {heap_time:.6f} 秒")
        
        self.results['search'] = results
        return results
    
    def plot_results(self, operation, data_sizes, figure=None, ax=None):
        """
        绘制性能测试结果
        
        参数:
            operation: 操作类型('enqueue', 'dequeue', 或 'search')
            data_sizes: 数据大小列表
            figure: matplotlib图形对象(可选)
            ax: matplotlib轴对象(可选)
        
        返回:
            figure: matplotlib图形对象
        """
        if operation not in self.results:
            print(f"错误: 操作 '{operation}' 的结果不可用，请先运行相应的性能测试")
            return None
        
        results = self.results[operation]
        
        if figure is None or ax is None:
            figure, ax = plt.subplots(figsize=(10, 6))
        else:
            ax.clear()
        
        ax.plot(data_sizes, results['linked_list'], 'o-', label='链表队列')
        ax.plot(data_sizes, results['binary_tree'], 's-', label='二叉树队列')
        ax.plot(data_sizes, results['heap'], '^-', label='堆队列')
        
        ax.set_xlabel('数据大小')
        ax.set_ylabel('执行时间(秒)')
        
        operation_name = {
            'enqueue': '入队',
            'dequeue': '出队',
            'search': '搜索'
        }.get(operation, operation)
        
        ax.set_title(f'{operation_name}操作性能比较')
        ax.legend()
        ax.grid(True)
        
        if figure is not None:
            figure.tight_layout()
            
            if ax is None:
                # 将图表保存到文件
                plt.savefig(f"{operation}_performance.png")
                plt.close()
                print(f"性能图表已保存为 {operation}_performance.png")
        
        return figure
    
    def run_all_tests(self, data_sizes, figure=None, ax=None):
        """
        运行所有性能测试
        
        参数:
            data_sizes: 要测试的数据大小列表
            figure: 可选的matplotlib图形对象(用于GUI显示)
            ax: 可选的matplotlib轴对象(用于GUI显示)
        """
        print("运行入队性能测试...")
        self.measure_enqueue_performance(data_sizes)
        self.plot_results('enqueue', data_sizes, figure, ax)
        
        print("\n运行出队性能测试...")
        self.measure_dequeue_performance(data_sizes)
        self.plot_results('dequeue', data_sizes, figure, ax)
        
        print("\n运行搜索性能测试...")
        self.measure_search_performance(data_sizes)
        self.plot_results('search', data_sizes, figure, ax)
        
        return self.get_complexity_analysis()
    
    def get_complexity_analysis(self):
        """
        获取三种队列实现的时间和空间复杂度分析
        
        返回:
            包含时间和空间复杂度分析的字典
        """
        complexity_data = {
            'time_complexity': {
                'operations': ['入队', '出队', '搜索'],
                'linked_list': ['O(n)', 'O(1)', 'O(n)'],
                'binary_tree': ['O(log n)', 'O(log n)', 'O(n)'],
                'heap': ['O(log n)', 'O(log n)', 'O(n)']
            },
            'space_complexity': {
                'data_structures': ['链表队列', '二叉树队列', '堆队列'],
                'complexity': ['O(n)', 'O(n)', 'O(n)']
            }
        }
        
        # 打印复杂度分析
        print("\n时间复杂度分析:")
        print("-" * 60)
        print("| 操作 | 链表队列 | 二叉树队列 | 堆队列 |")
        print("-" * 60)
        print("| 入队 | O(n)    | O(log n)  | O(log n) |")
        print("| 出队 | O(1)    | O(log n)  | O(log n) |")
        print("| 搜索 | O(n)    | O(n)      | O(n)     |")
        print("-" * 60)
        print("\n空间复杂度分析:")
        print("-" * 60)
        print("| 数据结构 | 空间复杂度 |")
        print("-" * 60)
        print("| 链表队列 | O(n)      |")
        print("| 二叉树队列 | O(n)      |")
        print("| 堆队列   | O(n)      |")
        print("-" * 60)
        
        return complexity_data

def compare_performance(arg1=None, arg2=None, arg3=None, test_sizes=None):
    """
    比较不同优先队列实现的性能
    
    此函数支持两种调用风格:
    1. 新风格(用于GUI): compare_performance(linked_list_queue, binary_tree_queue, heap_queue, test_sizes=None)
    2. 旧风格: compare_performance(emergencies, sample_size, test_sizes)
    
    参数将基于第一个参数的类型进行解释。
    
    返回:
        analyzer: PerformanceAnalyzer实例(结果)
    """
    # 导入所需类
    from ..data_structures.linked_list import LinkedListPriorityQueue
    from ..data_structures.binary_tree import BinaryTreePriorityQueue
    from ..data_structures.heap import HeapPriorityQueue
    
    # 确定使用的调用风格
    if isinstance(arg1, list):  # 旧风格: 第一个参数是紧急情况列表
        # 提取旧风格参数
        emergencies = arg1
        sample_size = arg2
        if arg3 is not None:
            test_sizes = arg3
        
        # 创建队列实例
        linked_list_queue = LinkedListPriorityQueue()
        binary_tree_queue = BinaryTreePriorityQueue()
        heap_queue = HeapPriorityQueue()
        
        # 如果提供了样本大小，使用紧急情况的子集
        if sample_size is not None and sample_size < len(emergencies):
            import random
            emergencies = random.sample(emergencies, sample_size)
        
        # 用紧急情况初始化队列
        for emergency in emergencies:
            linked_list_queue.enqueue(emergency)
            binary_tree_queue.enqueue(emergency)
            heap_queue.enqueue(emergency)
    else:  # 新风格: 参数是队列实例
        # 提取新风格参数
        linked_list_queue = arg1
        binary_tree_queue = arg2
        heap_queue = arg3
    
    # 如果未提供测试大小，设置默认值
    if test_sizes is None:
        test_sizes = [10, 20, 50, 100]
    
    # 创建性能分析器
    analyzer = PerformanceAnalyzer(linked_list_queue, binary_tree_queue, heap_queue)
    
    # 返回分析器对象
    return analyzer 