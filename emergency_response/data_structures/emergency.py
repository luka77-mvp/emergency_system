from enum import Enum

class EmergencyType(Enum):
    FIRE = 1        # 火灾
    MEDICAL = 2     # 医疗
    POLICE = 3      # 警察
    TRAFFIC = 4     # 交通事故
    NATURAL = 5     # 自然灾害

class Emergency:
    
    def __init__(self, emergency_id, emergency_type, severity_level, location, coordinates=None):
        """
        初始化紧急情况对象
        
        参数:
            emergency_id: 紧急情况的唯一标识符
            emergency_type: 紧急情况类型，必须是EmergencyType枚举的实例
            severity_level: 严重程度（1-10，1表示最严重/最高优先级）
            location: 位置描述（字符串）
            coordinates: 可选，位置坐标 (x, y)
        """
        if emergency_id < 0:
            raise ValueError("紧急情况ID必须为非负数")
        if severity_level < 1 or severity_level > 10:
            raise ValueError("严重程度必须在1到10之间")
        self.emergency_id = emergency_id
        self._type = None 
        self.type = emergency_type  
        self.severity_level = severity_level
        self.location = location
        self.coordinates = coordinates if coordinates else (0, 0)
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        """设置紧急情况类型，确保是EmergencyType枚举的实例"""
        if not isinstance(value, EmergencyType):
            raise TypeError("类型必须是EmergencyType枚举的实例")
        self._type = value
    
    def __repr__(self):
        """返回紧急情况的字符串表示"""
        return f"Emergency(ID={self.emergency_id}, Type={self.type.name}, Severity={self.severity_level}, Location={self.location})"
    
    def __eq__(self, other):
        """
        比较两个紧急情况是否相等（基于ID、严重程度和位置）
        """
        if not isinstance(other, Emergency):
            return False
        return (self.emergency_id == other.emergency_id and
                self.severity_level == other.severity_level and
                self.location == other.location)
    
    def __lt__(self, other):
        """
        比较两个紧急情况的优先级（基于严重程度）
        
        严重程度数值越小，优先级越高
        当严重程度相同时，ID越小，优先级越高
        """
        if not isinstance(other, Emergency):
            raise TypeError("不能与非Emergency类型对象比较")
        if self.severity_level == other.severity_level:
            return self.emergency_id < other.emergency_id
        return self.severity_level < other.severity_level
    
    def __le__(self, other):
        """
        比较两个紧急情况的优先级（小于等于，基于严重程度）
        
        严重程度数值越小，优先级越高
        当严重程度相同时，ID越小，优先级越高
        """
        if not isinstance(other, Emergency):
            raise TypeError("不能与非Emergency类型对象比较")
        if self.severity_level == other.severity_level:
            return self.emergency_id <= other.emergency_id
        return self.severity_level <= other.severity_level
    
    def __gt__(self, other):
        """
        比较两个紧急情况的优先级（大于，基于严重程度）
        
        严重程度数值越小，优先级越高
        当严重程度相同时，ID越小，优先级越高
        """
        if not isinstance(other, Emergency):
            raise TypeError("不能与非Emergency类型对象比较")
        if self.severity_level == other.severity_level:
            return self.emergency_id > other.emergency_id
        return self.severity_level > other.severity_level
    
    def __ge__(self, other):
        """
        比较两个紧急情况的优先级（大于等于，基于严重程度）
        
        严重程度数值越小，优先级越高
        当严重程度相同时，ID越小，优先级越高
        """
        if not isinstance(other, Emergency):
            raise TypeError("不能与非Emergency类型对象比较")
        if self.severity_level == other.severity_level:
            return self.emergency_id >= other.emergency_id
        return self.severity_level >= other.severity_level
    
    def __hash__(self):
        """让Emergency对象可哈希，以便在集合或字典键中使用"""
        return hash(self.emergency_id)