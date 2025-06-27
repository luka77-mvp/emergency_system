import os
import sys
import argparse

from emergency_response.data_structures.linked_list import LinkedListPriorityQueue
from emergency_response.data_structures.binary_tree import BinaryTreePriorityQueue
from emergency_response.data_structures.heap import HeapPriorityQueue
from emergency_response.utils.data_loader import load_emergency_data, initialize_priority_queues
from emergency_response.utils.performance_analyzer import PerformanceAnalyzer, compare_performance
from emergency_response.gui.main_app import run_application

def main():
    """程序主入口"""
    parser = argparse.ArgumentParser(description='Emergency Response Management System')
    parser.add_argument('--data', default='data/emergency_dataset.csv', help='紧急情况数据文件的路径')
    parser.add_argument('--analyze', action='store_true', help='运行性能分析')
    parser.add_argument('--sizes', type=int, nargs='+', default=[100, 500, 1000, 5000, 10000], help='用于性能分析的数据大小')
    parser.add_argument('--cli', action='store_true', help='启动命令行界面（无GUI）')
    args = parser.parse_args()
    
    # 默认为GUI，除非指定了 --cli
    if not args.cli:
        print("Starting graphical user interface...")
        run_application()
        return
    
    # 命令行界面代码如下
    # 获取数据文件的绝对路径
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.data)
    
    # 创建三种类型的优先级队列
    linked_list_queue = LinkedListPriorityQueue()
    binary_tree_queue = BinaryTreePriorityQueue()
    heap_queue = HeapPriorityQueue()
    
    # 加载紧急情况数据
    print(f"Loading emergency data from {data_path}...")
    emergencies = load_emergency_data(data_path)
    
    if not emergencies:
        print("Error: Failed to load any emergency data, exiting program")
        sys.exit(1)
    
    # 初始化优先级队列
    print("Initializing three types of priority queues...")
    initialize_priority_queues(emergencies, linked_list_queue, binary_tree_queue, heap_queue)
    
    # 从每个队列中打印最重要的紧急情况
    print("\nTop 3 emergencies in Linked List priority queue:")
    for _ in range(min(3, len(linked_list_queue))):
        emergency = linked_list_queue.dequeue()
        print(f"  {emergency}")
    
    # 重新初始化队列
    linked_list_queue = LinkedListPriorityQueue()
    binary_tree_queue = BinaryTreePriorityQueue()
    heap_queue = HeapPriorityQueue()
    initialize_priority_queues(emergencies, linked_list_queue, binary_tree_queue, heap_queue)
    
    print("\nTop 3 emergencies in Binary Tree priority queue:")
    for _ in range(min(3, len(binary_tree_queue))):
        emergency = binary_tree_queue.dequeue()
        print(f"  {emergency}")
    
    # 重新初始化队列
    linked_list_queue = LinkedListPriorityQueue()
    binary_tree_queue = BinaryTreePriorityQueue()
    heap_queue = HeapPriorityQueue()
    initialize_priority_queues(emergencies, linked_list_queue, binary_tree_queue, heap_queue)
    
    print("\nTop 3 emergencies in Heap priority queue:")
    for _ in range(min(3, len(heap_queue))):
        emergency = heap_queue.dequeue()
        print(f"  {emergency}")
    
    # 如果指定，则运行性能分析
    if args.analyze:
        print("\nRunning performance analysis...")
        
        # 方法1：使用PerformanceAnalyzer类
        # 创建性能分析器
        analyzer = PerformanceAnalyzer(
            LinkedListPriorityQueue(),
            BinaryTreePriorityQueue(),
            HeapPriorityQueue()
        )
        
        # 运行性能测试
        analyzer.run_all_tests(args.sizes)
        
        # 打印复杂度分析
        analyzer.print_complexity_analysis()
        
        # 方法2：使用compare_performance函数（简化版）
        print("\nUsing simplified performance comparison:")
        results = compare_performance(emergencies, test_sizes=[100, 500, 1000])
        print(results)
    
    print("\nProgram execution completed!")

if __name__ == "__main__":
    main()
