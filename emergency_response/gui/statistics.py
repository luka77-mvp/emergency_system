import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import Counter
from ..data_structures.emergency import EmergencyType

class StatisticsGUI:
    """紧急情况统计分析与可视化界面"""
    
    def __init__(self, root, emergencies):
        """
        初始化GUI
        
        Parameters:
            root: tkinter根窗口
            emergencies: 紧急情况对象列表
        """
        self.root = root
        self.root.title("Emergency Statistics Analysis")
        self.root.geometry("900x700")
        
        # 存储紧急情况
        self.emergencies = emergencies
        
        # 创建界面组件
        self._create_widgets()
        
        # 更新统计数据
        self._update_statistics()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部信息面板
        info_frame = ttk.LabelFrame(main_frame, text="Statistics Information", padding="10")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 紧急情况总数
        self.total_var = tk.StringVar(value="Total Emergencies: 0")
        ttk.Label(info_frame, textvariable=self.total_var).grid(row=0, column=0, sticky=tk.W, padx=10)
        
        # 按类型计数
        self.fire_var = tk.StringVar(value="Fire: 0")
        ttk.Label(info_frame, textvariable=self.fire_var).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        self.medical_var = tk.StringVar(value="Medical: 0")
        ttk.Label(info_frame, textvariable=self.medical_var).grid(row=0, column=2, sticky=tk.W, padx=10)
        
        self.police_var = tk.StringVar(value="Police: 0")
        ttk.Label(info_frame, textvariable=self.police_var).grid(row=0, column=3, sticky=tk.W, padx=10)
        
        # 平均严重程度
        self.avg_severity_var = tk.StringVar(value="Average Severity: 0.0")
        ttk.Label(info_frame, textvariable=self.avg_severity_var).grid(row=1, column=0, sticky=tk.W, padx=10)
        
        # 最高严重程度
        self.max_severity_var = tk.StringVar(value="Maximum Severity: 0")
        ttk.Label(info_frame, textvariable=self.max_severity_var).grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # 创建图表框架
        charts_frame = ttk.Frame(main_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧图表 - 类型分布
        type_frame = ttk.LabelFrame(charts_frame, text="Emergency Type Distribution", padding="10")
        type_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.type_figure = plt.Figure(figsize=(4, 4), dpi=100)
        self.type_canvas = FigureCanvasTkAgg(self.type_figure, master=type_frame)
        self.type_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 右侧图表 - 严重程度分布
        severity_frame = ttk.LabelFrame(charts_frame, text="Severity Distribution", padding="10")
        severity_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.severity_figure = plt.Figure(figsize=(4, 4), dpi=100)
        self.severity_canvas = FigureCanvasTkAgg(self.severity_figure, master=severity_frame)
        self.severity_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建底部按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 刷新按钮
        ttk.Button(
            button_frame, 
            text="Refresh Statistics",
            command=self._update_statistics
        ).pack(side=tk.LEFT, padx=5)
        
        # 关闭按钮
        ttk.Button(
            button_frame, 
            text="Close",
            command=self.root.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _update_statistics(self):
        """更新统计数据和图表"""
        if not self.emergencies:
            messagebox.showinfo("Notice", "No emergency data available for analysis")
            return
        
        # 计算基本统计信息
        total = len(self.emergencies)
        
        # 按类型计数
        type_counts = Counter(e.type for e in self.emergencies)
        fire_count = type_counts.get(EmergencyType.FIRE, 0)
        medical_count = type_counts.get(EmergencyType.MEDICAL, 0)
        police_count = type_counts.get(EmergencyType.POLICE, 0)
        
        # 计算严重程度统计
        severities = [e.severity_level for e in self.emergencies]
        avg_severity = sum(severities) / len(severities) if severities else 0
        max_severity = max(severities) if severities else 0
        
        # 更新信息标签
        self.total_var.set(f"Total Emergencies: {total}")
        self.fire_var.set(f"Fire: {fire_count}")
        self.medical_var.set(f"Medical: {medical_count}")
        self.police_var.set(f"Police: {police_count}")
        self.avg_severity_var.set(f"Average Severity: {avg_severity:.1f}")
        self.max_severity_var.set(f"Maximum Severity: {max_severity}")
        
        # 更新类型分布图
        self._update_type_chart(fire_count, medical_count, police_count)
        
        # 更新严重程度分布图
        self._update_severity_chart(severities)
    
    def _update_type_chart(self, fire_count, medical_count, police_count):
        """更新类型分布图"""
        # 清除之前的图表
        self.type_figure.clear()
        
        # 创建子图
        ax = self.type_figure.add_subplot(111)
        
        # 准备数据
        labels = ['Fire', 'Medical', 'Police']
        sizes = [fire_count, medical_count, police_count]
        colors = ['red', 'green', 'blue']
        explode = (0.1, 0, 0)  # 突出显示火灾
        
        # 绘制饼图
        ax.pie(
            sizes, 
            explode=explode, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90
        )
        
        ax.axis('equal')  # 确保饼图是圆形的
        ax.set_title('Emergency Type Distribution')
        
        # 刷新画布
        self.type_canvas.draw()
    
    def _update_severity_chart(self, severities):
        """更新严重程度分布图"""
        # 清除之前的图表
        self.severity_figure.clear()
        
        # 创建子图
        ax = self.severity_figure.add_subplot(111)
        
        # 准备数据
        severity_counts = Counter(severities)
        x = list(range(1, 11))
        y = [severity_counts.get(i, 0) for i in x]
        
        # 绘制条形图
        bars = ax.bar(x, y, color='skyblue', edgecolor='black')
        
        # 在条形图顶部添加数值标签
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height + 0.1,
                    str(int(height)),
                    ha='center', 
                    va='bottom'
                )
        
        # 设置标签和标题
        ax.set_xlabel('Severity')
        ax.set_ylabel('Count')
        ax.set_title('Emergency Severity Distribution')
        ax.set_xticks(x)
        ax.set_xlim(0.5, 10.5)
        
        # 刷新画布
        self.severity_canvas.draw()
    

    


def run_statistics_gui(emergencies):
    """运行统计分析GUI"""
    # 创建一个新窗口
    stats_window = tk.Toplevel()
    
    # 创建统计GUI
    app = StatisticsGUI(stats_window, emergencies)
    
    # 返回窗口对象，使其不会被垃圾回收
    return stats_window

if __name__ == '__main__':
    # 仅用于测试目的
    from ..data_structures.emergency import Emergency, EmergencyType
    
    # 创建示例数据
    sample_emergencies = [
        Emergency(1, EmergencyType.FIRE, 8, "Downtown", (20, 30)),
        Emergency(2, EmergencyType.MEDICAL, 5, "Hospital", (40, 60)),
        Emergency(3, EmergencyType.POLICE, 3, "Mall", (70, 20)),
        Emergency(4, EmergencyType.FIRE, 6, "Industrial Zone", (10, 80)),
        Emergency(5, EmergencyType.MEDICAL, 2, "Residential Area", (80, 50)),
    ]
    
    # 运行GUI
    run_statistics_gui(sample_emergencies) 