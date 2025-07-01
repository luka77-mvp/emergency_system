import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from emergency_response.data_structures.emergency import Emergency, EmergencyType
from emergency_response.data_structures.linked_list import LinkedListPriorityQueue
from emergency_response.data_structures.binary_tree import BinaryTreePriorityQueue
from emergency_response.data_structures.heap import HeapPriorityQueue
from emergency_response.utils.data_loader import load_emergency_data
from emergency_response.utils.performance_analyzer import PerformanceAnalyzer

from .interface import EmergencyResponseGUI
from .knn_visualization import run_knn_gui
from .statistics import run_statistics_gui
from .emergency_simulation import run_simulation_gui

class MainApplication:
    """主应用程序的应急响应管理系统"""
    
    def __init__(self, root):
        """
        初始化主应用程序
        
        Parameters:
            root: tkinter根窗口
        """
        self.root = root
        self.root.title("Emergency Response Management System")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 创建优先级队列实例
        self.linked_list_queue = LinkedListPriorityQueue()
        self.binary_tree_queue = BinaryTreePriorityQueue()
        self.heap_queue = HeapPriorityQueue()
        
        # 当前选择的队列类型
        self.current_queue_type = tk.StringVar(value="linked_list")
        
        # 当前选择的队列
        self.current_queue = self.linked_list_queue
        
        # 创建界面组件
        self._create_widgets()
        
        # 设置样式
        self._setup_styles()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题标签
        title_label = ttk.Label(
            main_frame, 
            text="Emergency Response Management System", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=20)
        
        # 创建描述标签
        desc_label = ttk.Label(
            main_frame,
            text="This system uses three different data structures (linked list, binary tree, and heap) to implement priority queues for managing urban emergencies.",
            wraplength=600,
            justify="center"
        )
        desc_label.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        
        # 创建主功能按钮
        self.buttons = []
        
        # 应急管理按钮
        emergency_button = ttk.Button(
            button_frame,
            text="Emergency Management",
            width=25,
            command=self._open_emergency_management
        )
        emergency_button.grid(row=0, column=0, padx=10, pady=10)
        self.buttons.append(emergency_button)
        
        # KNN可视化按钮
        knn_button = ttk.Button(
            button_frame,
            text="KNN Visualization",
            width=25,
            command=self._open_knn_visualization
        )
        knn_button.grid(row=0, column=1, padx=10, pady=10)
        self.buttons.append(knn_button)
        
        # 统计分析按钮
        stats_button = ttk.Button(
            button_frame,
            text="Statistical Analysis",
            width=25,
            command=self._open_statistics
        )
        stats_button.grid(row=1, column=0, padx=10, pady=10)
        self.buttons.append(stats_button)
        
        # 性能比较按钮
        perf_button = ttk.Button(
            button_frame,
            text="Performance Comparison",
            width=25,
            command=self._run_performance_comparison
        )
        perf_button.grid(row=1, column=1, padx=10, pady=10)
        self.buttons.append(perf_button)
        
        # 应急调度模拟按钮
        simulation_button = ttk.Button(
            button_frame,
            text="Emergency Dispatch Simulation",
            width=25,
            command=self._open_simulation
        )
        simulation_button.grid(row=2, column=0, padx=10, pady=10)
        self.buttons.append(simulation_button)
        
        # 加载数据按钮
        load_button = ttk.Button(
            button_frame,
            text="Load Data",
            width=25,
            command=self._load_data
        )
        load_button.grid(row=2, column=1, padx=10, pady=10)
        self.buttons.append(load_button)
        
        # 退出按钮
        exit_button = ttk.Button(
            button_frame,
            text="Exit",
            width=25,
            command=self.root.destroy
        )
        exit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.buttons.append(exit_button)
        
        # 创建状态栏
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=5)
        
        # 队列信息标签
        self.queue_info_var = tk.StringVar(value="Queue size: 0")
        queue_info_label = ttk.Label(status_frame, textvariable=self.queue_info_var, anchor=tk.E)
        queue_info_label.pack(side=tk.RIGHT, padx=5)
    
    def _setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        
        # 配置按钮样式
        style.configure(
            "TButton",
            font=("Arial", 11),
            padding=5
        )
        
        # 配置标签样式
        style.configure(
            "TLabel",
            font=("Arial", 11)
        )
        
        # 配置框架样式
        style.configure(
            "TFrame",
            background="#f0f0f0"
        )
    
    def _open_emergency_management(self):
        """打开应急管理界面"""
        # 创建新窗口
        management_window = tk.Toplevel(self.root)
        
        # 创建应急管理GUI并传递主应用的队列实例
        # 这样可以确保两个窗口操作的是同一份数据
        emergency_gui = EmergencyResponseGUI(
            management_window,
            self.linked_list_queue,
            self.binary_tree_queue,
            self.heap_queue
        )
        
        # 设置管理界面的当前队列类型以匹配主界面
        emergency_gui.current_queue_type.set(self.current_queue_type.get())
        emergency_gui._on_queue_type_changed()
        
        # 更新显示
        emergency_gui._update_queue_display()
        
        # 更新状态
        self.status_var.set("Emergency management interface opened")
    
    def _open_knn_visualization(self):
        """打开K近邻可视化界面"""
        # 检查队列是否为空
        if self.current_queue.is_empty():
            messagebox.showinfo("Notice", "Queue is empty, please load data first")
            return
        
        # 运行KNN可视化GUI
        run_knn_gui(self.current_queue)
        
        # 更新状态
        self.status_var.set("KNN visualization interface opened")
    
    def _open_statistics(self):
        """打开统计分析界面"""
        # 检查队列是否为空
        if self.current_queue.is_empty():
            messagebox.showinfo("Notice", "Queue is empty, please load data first")
            return
        
        # 从当前队列中获取所有紧急情况
        emergencies = list(self.current_queue)
        
        # 运行统计分析GUI
        run_statistics_gui(emergencies)
        
        # 更新状态
        self.status_var.set("Statistical analysis interface opened")
    
    def _run_performance_comparison(self):
        """运行性能比较"""
        # 检查队列是否为空
        if self.current_queue.is_empty():
            messagebox.showinfo("Notice", "Queue is empty, please load data first")
            return
        
        # 为性能分析创建一个新的顶级窗口
        performance_window = tk.Toplevel(self.root)
        performance_window.title("Performance Analysis")
        performance_window.geometry("900x700")
        
        # 创建主框架
        main_frame = ttk.Frame(performance_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部控制面板
        control_frame = ttk.LabelFrame(main_frame, text="Analysis Settings", padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 数据大小选项
        ttk.Label(control_frame, text="Data Sizes:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # 为数据大小创建复选按钮
        data_sizes = [10, 50, 100, 500, 1000]
        size_vars = []
        
        for i, size in enumerate(data_sizes):
            var = tk.BooleanVar(value=(i < 3))  # 默认选择前3个
            size_vars.append(var)
            ttk.Checkbutton(
                control_frame,
                text=str(size),
                variable=var
            ).grid(row=0, column=i+1, padx=5, pady=5)
        
        # 操作选择
        ttk.Label(control_frame, text="Operation:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        operation_var = tk.StringVar(value="enqueue")
        ttk.Radiobutton(
            control_frame,
            text="Enqueue",
            variable=operation_var,
            value="enqueue"
        ).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Radiobutton(
            control_frame,
            text="Dequeue",
            variable=operation_var,
            value="dequeue"
        ).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Radiobutton(
            control_frame,
            text="Search",
            variable=operation_var,
            value="search"
        ).grid(row=1, column=3, padx=5, pady=5)
        
        # 创建图表显示
        chart_frame = ttk.LabelFrame(main_frame, text="Performance Chart", padding="10")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 为图表创建图形
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        
        # 创建并保存canvas对象作为chart_frame的属性
        chart_frame.canvas = FigureCanvasTkAgg(figure, master=chart_frame)
        chart_frame.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建复杂度信息显示
        complexity_frame = ttk.LabelFrame(main_frame, text="Complexity Analysis", padding="10")
        complexity_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建Treeview以显示时间复杂度
        time_tree = ttk.Treeview(complexity_frame, columns=["operation", "linked_list", "binary_tree", "heap"], show="headings", height=3)
        time_tree.heading("operation", text="Operation")
        time_tree.heading("linked_list", text="Linked List")
        time_tree.heading("binary_tree", text="Binary Tree")
        time_tree.heading("heap", text="Heap")
        
        time_tree.column("operation", width=100)
        time_tree.column("linked_list", width=100)
        time_tree.column("binary_tree", width=100)
        time_tree.column("heap", width=100)
        
        time_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建Treeview以显示空间复杂度
        space_tree = ttk.Treeview(complexity_frame, columns=["data_structure", "complexity"], show="headings", height=3)
        space_tree.heading("data_structure", text="Data Structure")
        space_tree.heading("complexity", text="Space Complexity")
        
        space_tree.column("data_structure", width=150)
        space_tree.column("complexity", width=150)
        
        space_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # 关闭按钮
        ttk.Button(
            main_frame, 
            text="Close",
            command=performance_window.destroy
        ).pack(side=tk.RIGHT, padx=5, pady=10)
        
        # 用理论值预填充复杂度表
        # 时间复杂度
        time_tree.insert("", tk.END, values=("Enqueue", "O(n)", "O(log n)", "O(log n)"))
        time_tree.insert("", tk.END, values=("Dequeue", "O(1)", "O(log n)", "O(log n)"))
        time_tree.insert("", tk.END, values=("Search", "O(n)", "O(n)", "O(n)"))
        
        # 空间复杂度
        space_tree.insert("", tk.END, values=("Linked List", "O(n)"))
        space_tree.insert("", tk.END, values=("Binary Tree", "O(n)"))
        space_tree.insert("", tk.END, values=("Heap", "O(n)"))
        
        # 运行按钮
        ttk.Button(
            control_frame,
            text="Run Analysis",
            command=lambda: self._execute_performance_analysis(
                [data_sizes[i] for i in range(len(data_sizes)) if size_vars[i].get()],
                operation_var.get(),
                chart_frame,
                complexity_frame
            )
        ).grid(row=1, column=5, padx=10, pady=5)
        
        # 更新状态
        self.status_var.set("Performance analysis window opened")
    
    def _execute_performance_analysis(self, data_sizes, operation, chart_frame, complexity_frame):
        """使用选定的设置执行性能分析"""
        if not data_sizes:
            messagebox.showinfo("Notice", "Please select at least one data size")
            return
        
        self.status_var.set(f"Running {operation} performance analysis...")
        
        try:
            # 使用当前队列实例创建分析器
            analyzer = PerformanceAnalyzer()
            
            # 根据选择的操作运行相应的性能测试
            if operation == "enqueue":
                analyzer.measure_enqueue_performance(data_sizes)
            elif operation == "dequeue":
                analyzer.measure_dequeue_performance(data_sizes)
            elif operation == "search":
                analyzer.measure_search_performance(data_sizes)
            
            # 直接使用chart_frame的canvas属性
            if hasattr(chart_frame, 'canvas'):
                canvas = chart_frame.canvas
                figure = canvas.figure
                
                # 清除之前的图表内容
                figure.clear()
                
                # 创建新的子图
                ax = figure.add_subplot(111)
                
                # 绘制结果到图表
                analyzer.plot_results(operation, data_sizes, figure, ax)
                
                # 更新画布显示
                canvas.draw()
                
                self.status_var.set(f"Performance analysis for {operation} completed")
            else:
                messagebox.showerror("Error", "Chart canvas not properly initialized")
                self.status_var.set("Performance analysis failed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Performance analysis failed: {str(e)}")
            self.status_var.set("Performance analysis failed")
    
    def _open_simulation(self):
        """打开应急调度模拟界面"""
        run_simulation_gui()  # 调用emergency_simulation.py中的函数
    
    def _load_data(self):
        """从文件加载紧急情况数据"""
        # 要求用户选择一个文件
        file_path = filedialog.askopenfilename(
            title="Select Emergency Data File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # 更新状态
            self.status_var.set("Loading data...")
            self.root.update()
            
            # 清除现有队列
            self._clear_queues()
            
            # 加载数据
            emergencies = load_emergency_data(file_path)
            
            # 将紧急情况添加到队列中
            for emergency in emergencies:
                self.linked_list_queue.enqueue(emergency)
                self.binary_tree_queue.enqueue(emergency)
                self.heap_queue.enqueue(emergency)
            
            # 根据选择更新当前队列
            if self.current_queue_type.get() == "linked_list":
                self.current_queue = self.linked_list_queue
            elif self.current_queue_type.get() == "binary_tree":
                self.current_queue = self.binary_tree_queue
            else:
                self.current_queue = self.heap_queue
            
            # 更新队列信息
            self.queue_info_var.set(f"Queue size: {len(self.current_queue)}")
            
            # 更新状态
            self.status_var.set(f"Loaded {len(emergencies)} emergencies from {os.path.basename(file_path)}")
            
            # 显示成功消息
            messagebox.showinfo("Success", f"Successfully loaded {len(emergencies)} emergencies")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.status_var.set("Data loading failed")
    
    def _clear_queues(self):
        """清除所有队列"""
        # 清除链表队列
        while not self.linked_list_queue.is_empty():
            self.linked_list_queue.dequeue()
        
        # 清除二叉树队列
        while not self.binary_tree_queue.is_empty():
            self.binary_tree_queue.dequeue()
        
        # 清除堆队列
        while not self.heap_queue.is_empty():
            self.heap_queue.dequeue()
        
        # 更新队列信息
        self.queue_info_var.set("Queue size: 0")

def run_application():
    """运行主应用程序"""
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    run_application() 