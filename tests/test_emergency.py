import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emergency_response.data_structures.emergency import Emergency, EmergencyType

class TestEmergency(unittest.TestCase):
    
    def setUp(self):
        """每个测试前设置测试环境"""
        self.emergency1 = Emergency(1, EmergencyType.FIRE, 1, "市中心", (10, 20))
        self.emergency2 = Emergency(2, EmergencyType.MEDICAL, 3, "北区医院", (15, 25))
        self.emergency3 = Emergency(3, EmergencyType.POLICE, 2, "南区商场", (5, 15))
        self.emergency4 = Emergency(4, EmergencyType.FIRE, 1, "西区住宅", (8, 18))
    
    def test_initialization(self):
        """测试紧急情况对象的初始化"""
        self.assertEqual(self.emergency1.emergency_id, 1)
        self.assertEqual(self.emergency1.type, EmergencyType.FIRE)
        self.assertEqual(self.emergency1.severity_level, 1)
        self.assertEqual(self.emergency1.location, "市中心")
        self.assertEqual(self.emergency1.coordinates, (10, 20))
    
    def test_type_validation(self):
        """测试类型验证"""
        # 应该引发TypeError
        with self.assertRaises(TypeError):
            Emergency(5, "FIRE", 1, "测试位置")
    
    def test_equality(self):
        """
        测试相等性比较
        """
        # 创建一个与self.emergency1相同的紧急情况对象
        emergency_same = Emergency(1, EmergencyType.FIRE, 1, "市中心", (10, 20))
        self.assertEqual(self.emergency1, emergency_same)  # 确保相等
        
        # 不同的紧急情况对象
        self.assertNotEqual(self.emergency1, self.emergency2)  # 确保不相等
    
    def test_less_than(self):
        """测试小于比较（优先级比较）"""
        # 严重程度1应该比严重程度2优先级高（更小）
        self.assertLess(self.emergency1, self.emergency3)
        
        # 严重程度2应该比严重程度3优先级高（更小）
        self.assertLess(self.emergency3, self.emergency2)
    
    def test_repr(self):
        """测试字符串表示"""
        expected = "Emergency(ID=1, Type=FIRE, Severity=1, Location=市中心)"
        self.assertEqual(repr(self.emergency1), expected)

    def test_initialization_invalid_id(self):
        """
        测试使用无效参数初始化紧急情况
        """
        with self.assertRaises(ValueError):
            Emergency(-1, EmergencyType.FIRE, 1, "Invalid Location", (10, 20))  # 负ID
        with self.assertRaises(ValueError):
            Emergency(1, EmergencyType.FIRE, -1, "Invalid Location", (10, 20))  # 负优先级
        with self.assertRaises(TypeError):
            Emergency(1, "FIRE", 1, "Invalid Location", (10, 20))  # 无效类型

    def test_enqueue_same_id(self):
        """
        测试插入两个具有相同ID的紧急情况
        """
        emergency5 = Emergency(1, EmergencyType.FIRE, 1, "Duplicate Location", (10, 20))
        self.assertEqual(self.emergency1.emergency_id, emergency5.emergency_id)  # 确保ID相同
        self.assertNotEqual(self.emergency1, emergency5)  # 确保对象不同

if __name__ == '__main__':
    unittest.main() 