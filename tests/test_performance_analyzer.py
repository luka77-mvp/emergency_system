import unittest
import sys
import os
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，避免在没有GUI的环境中出错

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emergency_response.utils.performance_analyzer import PerformanceAnalyzer
from emergency_response.data_structures.linked_list import LinkedListPriorityQueue
from emergency_response.data_structures.binary_tree import BinaryTreePriorityQueue
from emergency_response.data_structures.heap import HeapPriorityQueue

class TestPerformanceAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """每个测试前设置测试环境"""
        self.analyzer = PerformanceAnalyzer()
    
    def test_generate_random_emergencies(self):
        """测试生成随机紧急情况数据"""
        count = 10
        emergencies = self.analyzer.generate_random_emergencies(count)
        
        # 验证生成的数据数量
        self.assertEqual(len(emergencies), count)
        
        # 验证每个紧急情况的属性
        for i, emergency in enumerate(emergencies):
            self.assertEqual(emergency.emergency_id, i + 1)
            self.assertIn(emergency.severity_level, range(1, 11))
            self.assertIsNotNone(emergency.location)
    
    def test_measure_enqueue_performance(self):
        """测试测量入队操作性能"""
        data_sizes = [10, 20]
        self.analyzer.measure_enqueue_performance(data_sizes)
        
        # 验证结果格式
        self.assertIn('enqueue', self.analyzer.results)
        results = self.analyzer.results['enqueue']
        self.assertIn('Linked List', results)
        self.assertIn('Binary Tree', results)
        self.assertIn('Heap', results)
        
        # 验证结果数量
        self.assertEqual(len(results['Linked List']), len(data_sizes))
        self.assertEqual(len(results['Binary Tree']), len(data_sizes))
        self.assertEqual(len(results['Heap']), len(data_sizes))
    
    def test_measure_dequeue_performance(self):
        """测试测量出队操作性能"""
        data_sizes = [10, 20]
        self.analyzer.measure_dequeue_performance(data_sizes)
        
        # 验证结果格式
        self.assertIn('dequeue', self.analyzer.results)
        results = self.analyzer.results['dequeue']
        self.assertIn('Linked List', results)
        self.assertIn('Binary Tree', results)
        self.assertIn('Heap', results)
        
        # 验证结果数量
        self.assertEqual(len(results['Linked List']), len(data_sizes))
        self.assertEqual(len(results['Binary Tree']), len(data_sizes))
        self.assertEqual(len(results['Heap']), len(data_sizes))
    
    def test_measure_search_performance(self):
        """测试测量搜索操作性能"""
        data_sizes = [10, 20]
        self.analyzer.measure_search_performance(data_sizes)
        
        # 验证结果格式
        self.assertIn('search', self.analyzer.results)
        results = self.analyzer.results['search']
        self.assertIn('Linked List', results)
        self.assertIn('Binary Tree', results)
        self.assertIn('Heap', results)
        
        # 验证结果数量
        self.assertEqual(len(results['Linked List']), len(data_sizes))
        self.assertEqual(len(results['Binary Tree']), len(data_sizes))
        self.assertEqual(len(results['Heap']), len(data_sizes))
    
    def test_plot_results(self):
        """测试绘制性能测试结果图表"""
        # 首先生成一些测试数据
        data_sizes = [10, 20]
        self.analyzer.measure_enqueue_performance(data_sizes)
        
        # 测试绘图功能
        try:
            # 创建图形对象用于测试
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            
            # 使用figure和ax参数调用plot_results
            self.analyzer.plot_results('enqueue', data_sizes, fig, ax)
            
            # 验证没有异常抛出
            plt.close(fig)
        except Exception as e:
            self.fail(f"绘制图表失败: {e}")
    
    def test_run_small_test(self):
        """测试运行小规模测试"""
        try:
            # 使用非常小的数据大小进行测试，以加快测试速度
            data_sizes = [5, 10]
            
            # 运行所有测试
            self.analyzer.measure_enqueue_performance(data_sizes)
            self.analyzer.measure_dequeue_performance(data_sizes)
            self.analyzer.measure_search_performance(data_sizes)
            
            # 验证结果是否生成
            self.assertIn('enqueue', self.analyzer.results)
            self.assertIn('dequeue', self.analyzer.results)
            self.assertIn('search', self.analyzer.results)
            
        except Exception as e:
            self.fail(f"运行测试失败: {e}")
    
    def test_get_complexity_analysis(self):
        """测试获取复杂度分析结果"""
        try:
            result = self.analyzer.get_complexity_analysis()
            # 验证返回的结果是否有效
            self.assertIsNotNone(result)
            self.assertIn('time', result)
            self.assertIn('space', result)
        except Exception as e:
            self.fail(f"复杂度分析失败: {e}")

if __name__ == '__main__':
    unittest.main() 