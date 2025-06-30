import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# 导入自定义对话框
from .custom_dialogs import askinteger
import numpy as np
import random
from ..data_structures.emergency import Emergency, EmergencyType
import heapq

class PrioritizedUnit:
    """用于优先队列的EmergencyUnit包装器，其中优先级是距离。"""
    def __init__(self, unit, distance):
        self.unit = unit
        self.severity_level = distance  # 使用severity_level存储距离以便与优先队列兼容

    def __repr__(self):
        return f"PrioritizedUnit(unit={self.unit.unit_id}, distance={self.severity_level})"
        
    def __lt__(self, other):
        """比较两个PrioritizedUnit对象（基于距离）"""
        if not isinstance(other, PrioritizedUnit):
            raise TypeError("不能与非PrioritizedUnit类型对象比较")
        return self.severity_level < other.severity_level
        
    def __eq__(self, other):
        """比较两个PrioritizedUnit对象是否相等（基于距离）"""
        if not isinstance(other, PrioritizedUnit):
            return False
        return self.severity_level == other.severity_level
        
    def __le__(self, other):
        """比较两个PrioritizedUnit对象（小于等于，基于距离）"""
        if not isinstance(other, PrioritizedUnit):
            raise TypeError("不能与非PrioritizedUnit类型对象比较")
        return self.severity_level <= other.severity_level
        
    def __gt__(self, other):
        """比较两个PrioritizedUnit对象（大于，基于距离）"""
        if not isinstance(other, PrioritizedUnit):
            raise TypeError("不能与非PrioritizedUnit类型对象比较")
        return self.severity_level > other.severity_level
        
    def __ge__(self, other):
        """比较两个PrioritizedUnit对象（大于等于，基于距离）"""
        if not isinstance(other, PrioritizedUnit):
            raise TypeError("不能与非PrioritizedUnit类型对象比较")
        return self.severity_level >= other.severity_level

class EmergencyUnit:
    """表示紧急响应单元（如消防车、救护车、警车等）"""
    
    def __init__(self, unit_id, unit_type, location_x, location_y):
        """
        初始化紧急响应单元
        
        Parameters:
            unit_id: 单位ID
            unit_type: 单位类型（如消防车、救护车、警车等）
            location_x: X坐标
            location_y: Y坐标
        """
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.location_x = location_x
        self.location_y = location_y
    
    def __repr__(self):
        return f"EmergencyUnit(id={self.unit_id}, type={self.unit_type}, loc=({self.location_x}, {self.location_y}))"

class KNNVisualizationGUI:
    """K最近邻紧急响应推荐可视化界面"""
    
    def __init__(self, root, priority_queue):
        """
        初始化GUI
        
        Parameters:
            root: tkinter根窗口
            priority_queue: 优先级队列实例
        """
        self.root = root
        self.root.title("KNN Emergency Response Recommendation")
        self.root.geometry("800x600")
        
        # 存储优先级队列
        self.priority_queue = priority_queue
        
        # 存储紧急响应单位
        self.emergency_units = []
        
        # 存储当前紧急事件
        self.current_emergency = None
        
        # 存储队列中的紧急事件（用于在地图上显示）
        self.emergencies = list(self.priority_queue)
        
        # 存储K值
        self.k_value = tk.IntVar(value=3)
        
        # 创建界面组件
        self._create_widgets()
        
        # 生成样本紧急响应单位
        self._generate_sample_units()
        
        # 初始地图绘制
        self._draw_map()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建控制面板
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # K值选择
        k_frame = ttk.Frame(control_frame)
        k_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(k_frame, text="K value:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(
            k_frame, 
            from_=1, 
            to=10, 
            textvariable=self.k_value,
            width=5,
            command=self._update_recommendation
        ).pack(side=tk.LEFT, padx=5)
        
        # 添加紧急事件按钮
        ttk.Button(
            control_frame, 
            text="Add Emergency",
            command=self._add_emergency
        ).pack(side=tk.LEFT, padx=5)
        
        # 生成随机紧急响应单位按钮
        ttk.Button(
            control_frame, 
            text="Generate Random Units",
            command=self._generate_sample_units
        ).pack(side=tk.LEFT, padx=5)
        
        # 清除所有按钮
        ttk.Button(
            control_frame, 
            text="Clear All",
            command=self._clear_all
        ).pack(side=tk.LEFT, padx=5)
        
        # 创建地图显示区域
        map_frame = ttk.LabelFrame(main_frame, text="Map", padding="10")
        map_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建图表
        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=map_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 添加工具栏
        toolbar_frame = ttk.Frame(map_frame)
        toolbar_frame.pack(fill=tk.X)
        
        # 创建结果显示区域
        results_frame = ttk.LabelFrame(main_frame, text="Recommended Units", padding="10")
        results_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建Treeview以显示推荐结果
        columns = ("id", "type", "distance")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=5)
        
        # 设置列标题
        self.results_tree.heading("id", text="Unit ID")
        self.results_tree.heading("type", text="Unit Type")
        self.results_tree.heading("distance", text="Distance")
        
        # 设置列宽
        self.results_tree.column("id", width=100)
        self.results_tree.column("type", width=100)
        self.results_tree.column("distance", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)
        
        # 放置组件
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建状态栏
        status_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, padding=(2, 2, 2, 2))
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=2)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(fill=tk.X)
    
    def _generate_sample_units(self):
        """生成样本紧急响应单位"""
        # 清除现有单位
        self.emergency_units = []
        
        # 生成随机单位
        unit_types = ["Fire Truck", "Ambulance", "Police Car"]
        
        for i in range(20):
            unit_type = random.choice(unit_types)
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            
            unit = EmergencyUnit(i+1, unit_type, x, y)
            self.emergency_units.append(unit)
        
        # 更新地图
        self._draw_map()
        
        # 更新状态
        self.status_var.set(f"Generated {len(self.emergency_units)} random emergency response units")
    
    def _add_emergency(self):
        """添加新紧急事件或选择现有紧急事件"""
        # 创建一个顶级窗口
        dialog = tk.Toplevel(self.root)
        dialog.title("Select or Add Emergency")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建主框架
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建用于选择现有紧急事件的框架
        select_frame = ttk.LabelFrame(main_frame, text="Select Existing Emergency", padding="10")
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建选择列表
        emergency_listbox = tk.Listbox(select_frame, height=5)
        emergency_listbox.pack(fill=tk.X, expand=True)
        
        # 将紧急事件添加到列表
        for emergency in self.emergencies:
            emergency_listbox.insert(tk.END, f"ID: {emergency.emergency_id}, Type: {emergency.type.name}, Severity: {emergency.severity_level}")
        
        # 添加选择按钮
        def on_select():
            # 获取所选索引
            selection = emergency_listbox.curselection()
            if not selection:
                messagebox.showinfo("Notice", "Please select an emergency")
                return
            
            # 获取所选紧急事件
            index = selection[0]
            self.current_emergency = self.emergencies[index]
            
            # 更新地图和推荐
            self._draw_map()
            self._update_recommendation()
            
            # 关闭对话框
            dialog.destroy()
            
            # 更新状态
            self.status_var.set(f"Selected emergency ID: {self.current_emergency.emergency_id}")
        
        ttk.Button(select_frame, text="Select", command=on_select).pack(pady=5)
        
        # 创建用于添加新紧急事件的框架
        add_frame = ttk.LabelFrame(main_frame, text="Add New Emergency", padding="10")
        add_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 紧急事件ID
        ttk.Label(add_frame, text="Emergency ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_var = tk.IntVar(value=random.randint(1000, 9999))
        ttk.Entry(add_frame, textvariable=id_var, width=20).grid(row=0, column=1, pady=5)
        
        # 紧急事件类型
        ttk.Label(add_frame, text="Emergency Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar(value="FIRE")
        type_combo = ttk.Combobox(add_frame, textvariable=type_var, width=18)
        type_combo['values'] = [e.name for e in EmergencyType]
        type_combo.grid(row=1, column=1, pady=5)
        
        # 严重级别
        ttk.Label(add_frame, text="Severity Level (1-10):").grid(row=2, column=0, sticky=tk.W, pady=5)
        severity_var = tk.IntVar(value=5)
        ttk.Spinbox(add_frame, from_=1, to=10, textvariable=severity_var, width=18).grid(row=2, column=1, pady=5)
        
        # 位置
        ttk.Label(add_frame, text="Location:").grid(row=3, column=0, sticky=tk.W, pady=5)
        location_var = tk.StringVar(value="Downtown")
        ttk.Entry(add_frame, textvariable=location_var, width=20).grid(row=3, column=1, pady=5)
        
        # 坐标
        ttk.Label(add_frame, text="Coordinates (x, y):").grid(row=4, column=0, sticky=tk.W, pady=5)
        coord_frame = ttk.Frame(add_frame)
        coord_frame.grid(row=4, column=1, pady=5)
        
        x_var = tk.DoubleVar(value=round(random.uniform(0, 100), 2))
        y_var = tk.DoubleVar(value=round(random.uniform(0, 100), 2))
        
        ttk.Entry(coord_frame, textvariable=x_var, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(coord_frame, text=",").pack(side=tk.LEFT)
        ttk.Entry(coord_frame, textvariable=y_var, width=8).pack(side=tk.LEFT, padx=2)
        
        # 提交按钮
        def on_submit():
            try:
                # 从表单获取值
                emergency_id = id_var.get()
                emergency_type_str = type_var.get()
                severity_level = severity_var.get()
                location = location_var.get()
                x = x_var.get()
                y = y_var.get()
                
                # 验证输入
                if not location:
                    messagebox.showerror("Error", "Please enter a location")
                    return
                
                if not (1 <= severity_level <= 10):
                    messagebox.showerror("Error", "Severity level must be between 1 and 10")
                    return
                
                # 将字符串转换为EmergencyType枚举
                emergency_type = EmergencyType[emergency_type_str]
                
                # 创建紧急事件对象
                emergency = Emergency(
                    emergency_id=emergency_id,
                    emergency_type=emergency_type,
                    severity_level=severity_level,
                    location=location,
                    coordinates=(x, y)
                )
                
                # 设置为当前紧急事件
                self.current_emergency = emergency
                
                # 添加到紧急事件列表
                self.emergencies.append(emergency)
                
                # 更新地图和推荐
                self._draw_map()
                self._update_recommendation()
                
                # 关闭对话框
                dialog.destroy()
                
                # 更新状态
                self.status_var.set(f"Added new emergency ID: {emergency_id}")
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(add_frame, text="Add", command=on_submit).grid(row=5, column=0, columnspan=2, pady=10)
    
    def _clear_all(self):
        """清除所有数据并重置可视化"""
        # 清除当前紧急事件
        self.current_emergency = None
        
        # 清除紧急响应单位
        self.emergency_units = []
        
        # 清除结果树
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # 重绘地图
        self._draw_map()
        
        # 更新状态
        self.status_var.set("All data cleared")
    
    def _draw_map(self):
        """绘制包含紧急事件和响应单位的地图"""
        # 清除以前的图表
        self.figure.clear()
        
        # 创建子图
        ax = self.figure.add_subplot(111)
        
        # 设置图表限制
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # 绘制网格
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 绘制紧急响应单位
        for unit in self.emergency_units:
            if unit.unit_type == "Fire Truck":
                color = 'red'
                marker = 's'  # 方形
            elif unit.unit_type == "Ambulance":
                color = 'green'
                marker = '^'  # 三角形
            else:  # 警车
                color = 'blue'
                marker = 'o'  # 圆形
            
            ax.scatter(unit.location_x, unit.location_y, color=color, marker=marker, s=50, label=f"{unit.unit_type}")
        
        # 绘制队列中的紧急事件
        for emergency in self.emergencies:
            if hasattr(emergency, 'coordinates') and emergency.coordinates:
                x, y = emergency.coordinates
                
                if emergency.type == EmergencyType.FIRE:
                    color = 'red'
                elif emergency.type == EmergencyType.MEDICAL:
                    color = 'green'
                else:  # 警察
                    color = 'blue'
                
                ax.scatter(x, y, color=color, marker='*', s=100, alpha=0.5)
                ax.text(x, y+2, f"ID: {emergency.emergency_id}", fontsize=8)
        
        # 突出显示当前紧急事件并绘制KNN
        if self.current_emergency and hasattr(self.current_emergency, 'coordinates') and self.current_emergency.coordinates:
            x, y = self.current_emergency.coordinates
            
            # 用更大的标记绘制当前紧急事件
            ax.scatter(x, y, color='black', marker='*', s=200, edgecolor='yellow', linewidth=2)
            ax.text(x, y+3, f"Current: {self.current_emergency.emergency_id}", fontsize=10, weight='bold')
            
            # 查找K个最近的单位
            k = self.k_value.get()
            nearest_units = self._find_k_nearest_units(x, y, k)
            
            # 绘制到最近单位的线
            for unit, distance in nearest_units:
                ax.plot([x, unit.location_x], [y, unit.location_y], 'k--', alpha=0.5)
                
                # 添加距离标签
                mid_x = (x + unit.location_x) / 2
                mid_y = (y + unit.location_y) / 2
                ax.text(mid_x, mid_y, f"{distance:.2f}", fontsize=8, backgroundcolor='white')
        
        # 添加图例（仅显示唯一的单位类型）
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')
        
        # 设置标签和标题
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Emergency Response Units and Emergencies')
        
        # 刷新画布
        self.canvas.draw()
    
    def _find_k_nearest_units(self, x, y, k):
        """使用heapq查找给定坐标的k个最近的紧急响应单位。"""
        # 创建一个最大堆（使用负距离作为优先级）
        pq = []
        
        # 计算从每个单位到紧急事件的距离并添加到优先队列
        for unit in self.emergency_units:
            # 计算欧几里得距离
            distance = np.sqrt((unit.location_x - x)**2 + (unit.location_y - y)**2)
            
            # 创建PrioritizedUnit对象（使用距离作为优先级）
            prioritized_unit = PrioritizedUnit(unit, distance)
            
            # 如果队列未满，直接添加
            if len(pq) < k:
                heapq.heappush(pq, prioritized_unit)
            # 如果队列已满但当前单位更近，则替换最远的单位
            elif distance < pq[0].severity_level:
                heapq.heappushpop(pq, prioritized_unit)
        
        # 将结果格式转换为[(unit, distance), ...]
        nearest_units = [(p_unit.unit, p_unit.severity_level) for p_unit in pq]
        
        # 按距离排序（最近的在前）
        nearest_units.sort(key=lambda x: x[1])
        
        return nearest_units
    
    def _update_recommendation(self):
        """根据当前紧急事件和K值更新推荐"""
        # 清除以前的结果
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # 检查是否已设置当前紧急事件
        if not self.current_emergency or not hasattr(self.current_emergency, 'coordinates') or not self.current_emergency.coordinates:
            return
        
        # 获取坐标
        x, y = self.current_emergency.coordinates
        
        # 查找K个最近的单位
        k = self.k_value.get()
        nearest_units = self._find_k_nearest_units(x, y, k)
        
        # 添加到结果树
        for i, (unit, distance) in enumerate(nearest_units):
            self.results_tree.insert(
                "", 
                "end", 
                values=(
                    unit.unit_id,
                    unit.unit_type,
                    f"{distance:.2f}"
                )
            )
        
        # 更新地图
        self._draw_map()
        
        # 更新状态
        self.status_var.set(f"Found {len(nearest_units)} nearest units for emergency ID: {self.current_emergency.emergency_id}")

def run_knn_gui(priority_queue):
    """运行KNN可视化GUI"""
    # 创建一个新窗口
    knn_window = tk.Toplevel()
    
    # 创建KNN可视化GUI
    app = KNNVisualizationGUI(knn_window, priority_queue)
    
    # 返回窗口对象，以免被垃圾回收
    return knn_window

if __name__ == "__main__":
    # 仅用于测试目的
    from ..data_structures.emergency import Emergency, EmergencyType
    
    # 创建一个样本优先队列
    class SampleQueue:
        def __iter__(self):
            return iter([
                Emergency(1, EmergencyType.FIRE, 8, "Downtown", (20, 30)),
                Emergency(2, EmergencyType.MEDICAL, 5, "Hospital", (40, 60)),
                Emergency(3, EmergencyType.POLICE, 3, "Mall", (70, 20))
            ])
    
    # 运行GUI
    root = tk.Tk()
    app = KNNVisualizationGUI(root, SampleQueue())
    root.mainloop() 