import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.simpledialog import askinteger
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import numpy as np
import random
import time
from ..data_structures.emergency import Emergency, EmergencyType
from ..data_structures.linked_list import LinkedListPriorityQueue
from ..data_structures.binary_tree import BinaryTreePriorityQueue
from ..data_structures.heap import HeapPriorityQueue
from ..utils.data_loader import load_emergency_data, initialize_priority_queues
# 导入性能分析工具
from ..utils.performance_analyzer import compare_performance
# 导入自定义对话框
from .custom_dialogs import AddEmergencyDialog
from .statistics import run_statistics_gui

class EmergencyResponseGUI:
    """应急响应管理系统的图形用户界面"""
    
    def __init__(self, root, linked_list_queue, binary_tree_queue, heap_queue):
        """
        初始化GUI
        
        Parameters:
            root: tkinter根窗口
            linked_list_queue: 共享的链表队列实例
            binary_tree_queue: 共享的二叉树队列实例
            heap_queue: 共享的堆队列实例
        """
        self.root = root
        self.root.title("Emergency Response Management System")
        self.root.geometry("1200x700")
        self.root.minsize(800, 600)
        
        # 使用从主应用传递过来的共享队列实例
        self.linked_list_queue = linked_list_queue
        self.binary_tree_queue = binary_tree_queue
        self.heap_queue = heap_queue
        
        # 当前选择的队列类型
        self.current_queue_type = tk.StringVar(value="heap")
        
        # 当前选择的队列
        self.current_queue = self.heap_queue
        
        # 创建界面组件
        self._create_widgets()
        
        # 绑定事件
        self._bind_events()
        
        # 不自动加载示例数据，等待用户操作
        # self._load_sample_data()
        
        # 更新显示
        self._update_queue_display()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部控制面板
        self._create_control_panel()
        
        # 创建队列显示区域
        self._create_queue_display()
        
        # 创建底部状态栏
        self._create_status_bar()
    
    def _create_control_panel(self):
        """创建顶部控制面板"""
        control_frame = ttk.LabelFrame(self.main_frame, text="Control Panel", padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 队列类型选择
        queue_type_frame = ttk.Frame(control_frame)
        queue_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(queue_type_frame, text="Queue Type:").pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            queue_type_frame, 
            text="Linked List", 
            variable=self.current_queue_type,
            value="linked_list",
            command=self._on_queue_type_changed
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            queue_type_frame, 
            text="Binary Tree", 
            variable=self.current_queue_type,
            value="binary_tree",
            command=self._on_queue_type_changed
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            queue_type_frame, 
            text="Heap", 
            variable=self.current_queue_type,
            value="heap",
            command=self._on_queue_type_changed
        ).pack(side=tk.LEFT, padx=5)
        
        # 操作按钮
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            buttons_frame, 
            text="Add Emergency",
            command=self._add_emergency
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame, 
            text="Process Highest Priority",
            command=self._process_emergency
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame, 
            text="Search Emergency",
            command=self._search_emergency
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame, 
            text="Change Priority",
            command=self._change_priority
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_queue_display(self):
        """创建队列显示区域"""
        display_frame = ttk.Frame(self.main_frame)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        queue_frame = ttk.LabelFrame(display_frame, text="Emergency Queue", padding="10")
        queue_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建一个容器来管理 Treeview 和 Canvas
        self.queue_display_container = ttk.Frame(queue_frame)
        self.queue_display_container.pack(fill=tk.BOTH, expand=True)
        
        # 1. Treeview (用于列表显示)
        columns = ("id", "type", "severity", "location")
        self.queue_tree_view = ttk.Treeview(self.queue_display_container, columns=columns, show="headings")
        self.queue_tree_view.heading("id", text="ID")
        self.queue_tree_view.heading("type", text="Type")
        self.queue_tree_view.heading("severity", text="Severity (Lower value = Higher priority)")
        self.queue_tree_view.heading("location", text="Location")
        self.queue_tree_view.column("id", width=50, anchor='center')
        self.queue_tree_view.column("type", width=100, anchor='center')
        self.queue_tree_view.column("severity", width=100, anchor='center')
        self.queue_tree_view.column("location", width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(self.queue_display_container, orient=tk.VERTICAL, command=self.queue_tree_view.yview)
        self.queue_tree_view.configure(yscroll=scrollbar.set)
        
        # 默认不直接 pack，由 _update_queue_display 控制
        
        # 2. Canvas (用于树状显示)
        self.tree_canvas = tk.Canvas(self.queue_display_container, bg="white")
        # 存储树节点的位置信息，用于点击检测
        self.tree_nodes = {}  # 格式: {emergency_id: (x, y, radius)}
        
        # 右侧图表显示
        self.chart_frame = ttk.LabelFrame(display_frame, text="Statistics Chart", padding="10")
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建图表
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _create_status_bar(self):
        """创建底部状态栏"""
        status_frame = ttk.Frame(self.main_frame, relief=tk.SUNKEN, padding=(2, 2, 2, 2))
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=2)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(fill=tk.X)
        
        # 队列信息标签
        self.queue_info_var = tk.StringVar(value="Queue size: 0")
        queue_info_label = ttk.Label(status_frame, textvariable=self.queue_info_var, anchor=tk.E)
        queue_info_label.pack(side=tk.RIGHT, padx=5)
    
    def _bind_events(self):
        """将事件绑定到小部件"""
        # 绑定树视图事件
        self.queue_tree_view.bind("<Motion>", self._on_tree_hover)
        self.queue_tree_view.bind("<Button-1>", self._on_tree_click)
        
        # 绑定树状图 Canvas 事件
        self.tree_canvas.bind("<Button-1>", self._on_canvas_click)
        self.tree_canvas.bind("<Motion>", self._on_canvas_hover)
    
    def _on_queue_type_changed(self, event=None):
        """处理队列类型更改"""
        queue_type = self.current_queue_type.get()
        
        if queue_type == "linked_list":
            self.current_queue = self.linked_list_queue
        elif queue_type == "binary_tree":
            self.current_queue = self.binary_tree_queue
        else:  # 堆
            self.current_queue = self.heap_queue
        
        self._update_queue_display()
        self.status_var.set(f"Switched to {self._get_queue_type_name()} priority queue")
    
    def _get_queue_type_name(self):
        """获取当前队列类型的名称"""
        queue_type = self.current_queue_type.get()
        
        if queue_type == "linked_list":
            return "Linked List"
        elif queue_type == "binary_tree":
            return "Binary Tree"
        else:  # 堆
            return "Heap"
    
    def _add_emergency(self):
        """添加新的紧急情况"""
        dialog = AddEmergencyDialog(self.root)
        
        if dialog.result:
            new_emergency = dialog.result
            
            # 将新的紧急情况添加到所有三个队列中以保持同步
            self.linked_list_queue.enqueue(new_emergency)
            self.binary_tree_queue.enqueue(new_emergency)
            self.heap_queue.enqueue(new_emergency)

            # 更新显示
            self._update_queue_display()
            messagebox.showinfo("Success", "Emergency added successfully.")
    
    def _process_emergency(self):
        """处理最高优先级的紧急情况"""
        if self.current_queue.is_empty():
            messagebox.showinfo("Notice", "The queue is empty.")
            return
        
        # 从所有三个队列中移除最高优先级的紧急情况
        removed_from_linked_list = self.linked_list_queue.dequeue()
        removed_from_binary_tree = self.binary_tree_queue.dequeue()
        removed_from_heap = self.heap_queue.dequeue()
        
        # 检查一致性
        if not (removed_from_linked_list == removed_from_binary_tree and removed_from_binary_tree == removed_from_heap):
            messagebox.showwarning("Warning", "Data inconsistency detected between queues after processing an emergency.")
        
        # 更新显示
        self._update_queue_display()
        messagebox.showinfo("Processed", f"Processed emergency: {removed_from_linked_list}")
    
    def _search_emergency(self):
        """搜索紧急情况"""
        # 询问要搜索的紧急情况ID
        emergency_id = askinteger("Search Emergency", "Enter Emergency ID:")
        if emergency_id is None:  # 用户取消
            return
        
        # 在当前队列中搜索
        emergency = self.current_queue.search(emergency_id)
        
        if emergency:
            messagebox.showinfo(
                "Emergency Found", 
                f"ID: {emergency.emergency_id}\n"
                f"Type: {emergency.type.name}\n"
                f"Severity: {emergency.severity_level}\n"
                f"Location: {emergency.location}\n"
                f"Coordinates: {emergency.coordinates}"
            )
        else:
            messagebox.showinfo("Not Found", f"No emergency with ID {emergency_id} found.")
    
    def _change_priority(self):
        """更改紧急情况优先级"""
        # 询问要更改优先级的紧急情况ID
        emergency_id = askinteger("Change Priority", "Enter Emergency ID:")
        if emergency_id is None:  # 用户取消
            return
        
        # 在当前队列中搜索
        emergency = self.current_queue.search(emergency_id)
        if not emergency:
            messagebox.showinfo("Not Found", f"No emergency with ID {emergency_id} found.")
            return
        
        # 询问新的严重程度
        new_severity = askinteger(
            "Change Priority",
            f"Current severity: {emergency.severity_level}\nEnter new severity level (1-10):\n\nNote: Lower value = Higher priority (1 is most urgent)",
            minvalue=1,
            maxvalue=10
        )
        
        if new_severity is None:  # 用户取消
            return
        
        # 更新所有队列
        success = self.current_queue.change_priority(emergency_id, new_severity)
        
        if success:
            # 同步更新其他队列
            if self.current_queue_type.get() == "linked_list":
                self.binary_tree_queue.change_priority(emergency_id, new_severity)
                self.heap_queue.change_priority(emergency_id, new_severity)
            elif self.current_queue_type.get() == "binary_tree":
                self.linked_list_queue.change_priority(emergency_id, new_severity)
                self.heap_queue.change_priority(emergency_id, new_severity)
            else: # heap
                self.linked_list_queue.change_priority(emergency_id, new_severity)
                self.binary_tree_queue.change_priority(emergency_id, new_severity)
                
            self._update_queue_display()
            messagebox.showinfo("Success", "Priority changed successfully.")
        else:
            messagebox.showerror("Error", "Failed to change priority.")
    
    def _show_statistics(self):
        """显示队列统计信息"""
        if self.current_queue.is_empty():
            messagebox.showinfo("Notice", "Queue is empty, no statistics to show.")
            return
        
        emergencies = list(self.current_queue)
        run_statistics_gui(emergencies, self.root)
    
    def _run_performance_analysis(self):
        """运行性能分析"""
        compare_performance(self.root)
    
    def _update_queue_display(self):
        """更新队列显示，根据队列类型选择列表或树状图"""
        # 清空当前所有视图
        self.queue_tree_view.delete(*self.queue_tree_view.get_children())
        self.tree_canvas.delete("all")
        
        # 隐藏所有视图
        self.queue_tree_view.pack_forget()
        self.tree_canvas.pack_forget()
        
        queue_type = self.current_queue_type.get()
        
        if self.current_queue.is_empty():
            self.tree_canvas.pack(fill=tk.BOTH, expand=True)
            self.tree_canvas.create_text(
                self.tree_canvas.winfo_width() / 2, 
                self.tree_canvas.winfo_height() / 2, 
                text="Queue is empty",
                font=("Arial", 16)
            )
        elif queue_type == 'linked_list':
            # 显示 Treeview
            self.queue_tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # 填充 Treeview
            for emergency in self.current_queue:
                self.queue_tree_view.insert(
                    "", 
                    "end", 
                    values=(
                        emergency.emergency_id,
                        emergency.type.name,
                        emergency.severity_level,
                        emergency.location
                    )
                )
        else:
            # 显示 Canvas
            self.tree_canvas.pack(fill=tk.BOTH, expand=True)
            # 强制更新UI以获取正确的Canvas尺寸
            self.root.update_idletasks()
            # 在 Canvas 上绘制树
            self._draw_tree()

        # 更新统计图和状态栏
        self._update_statistics_chart()
        self.queue_info_var.set(f"Queue size: {len(self.current_queue)}")

    def _draw_tree(self):
        self.tree_canvas.delete("all")
        self.tree_nodes = {}  # 清空节点位置信息
        queue_type = self.current_queue_type.get()

        # 获取画布的当前宽度
        canvas_width = self.tree_canvas.winfo_width()
        if canvas_width <= 1: # 如果画布还没完全渲染，给一个默认值
            canvas_width = 800

        # 动态计算初始位置和水平间距
        initial_x = canvas_width / 2
        initial_y = 50  # 增加顶部的边距
        initial_h_gap = canvas_width / 4 # 水平间距为宽度的1/4

        if queue_type == 'binary_tree' and self.current_queue.root:
            self._draw_binary_tree_node(self.current_queue.root, initial_x, initial_y, initial_h_gap)
        elif queue_type == 'heap' and not self.current_queue.is_empty():
            self._draw_heap_node(1, initial_x, initial_y, initial_h_gap)

    def _draw_binary_tree_node(self, node, x, y, h_gap):
        if not node:
            return

        v_gap = 70  # 固定的垂直间距
        node_radius = 30  # 节点半径

        # 绘制节点
        text = f"S:{node.data.severity_level}\nID:{node.data.emergency_id}"
        self.tree_canvas.create_oval(x-node_radius, y-node_radius, x+node_radius, y+node_radius, fill="lightblue", outline="black", tags=f"node_{node.data.emergency_id}")
        self.tree_canvas.create_text(x, y, text=text, font=("Arial", 9), tags=f"text_{node.data.emergency_id}")
        
        # 存储节点位置信息，用于点击检测
        self.tree_nodes[node.data.emergency_id] = (x, y, node_radius)

        # 绘制到左子节点的连线
        if node.left:
            x_left = x - h_gap
            y_left = y + v_gap
            self.tree_canvas.create_line(x, y + node_radius, x_left, y_left - node_radius)
            self._draw_binary_tree_node(node.left, x_left, y_left, h_gap / 2)

        # 绘制到右子节点的连线
        if node.right:
            x_right = x + h_gap
            y_right = y + v_gap
            self.tree_canvas.create_line(x, y + node_radius, x_right, y_right - node_radius)
            self._draw_binary_tree_node(node.right, x_right, y_right, h_gap / 2)

    def _draw_heap_node(self, index, x, y, h_gap):
        if index > self.current_queue.count:
            return
        
        v_gap = 70  # 固定的垂直间距
        node_radius = 30  # 节点半径

        # 绘制节点
        node_data = self.current_queue.heap[index]
        text = f"S:{node_data.severity_level}\nID:{node_data.emergency_id}"
        self.tree_canvas.create_oval(x-node_radius, y-node_radius, x+node_radius, y+node_radius, fill="lightgreen", outline="black", tags=f"node_{node_data.emergency_id}")
        self.tree_canvas.create_text(x, y, text=text, font=("Arial", 9), tags=f"text_{node_data.emergency_id}")
        
        # 存储节点位置信息，用于点击检测
        self.tree_nodes[node_data.emergency_id] = (x, y, node_radius)

        left_child_index = 2 * index
        right_child_index = 2 * index + 1

        # 绘制到左子节点的连线
        if left_child_index <= self.current_queue.count:
            x_left = x - h_gap
            y_left = y + v_gap
            self.tree_canvas.create_line(x, y + node_radius, x_left, y_left - node_radius)
            self._draw_heap_node(left_child_index, x_left, y_left, h_gap / 2)

        # 绘制到右子节点的连线
        if right_child_index <= self.current_queue.count:
            x_right = x + h_gap
            y_right = y + v_gap
            self.tree_canvas.create_line(x, y + node_radius, x_right, y_right - node_radius)
            self._draw_heap_node(right_child_index, x_right, y_right, h_gap / 2)

    def _update_statistics_chart(self):
        """更新统计图表"""
        # 清除之前的图表
        self.figure.clear()
        
        # 获取当前队列中的所有紧急事件
        emergencies = list(self.current_queue)
        
        if not emergencies:
            # 如果队列为空，则不更新图表
            self.canvas.draw()
            return
        
        # 创建两个子图
        ax1 = self.figure.add_subplot(211)  # 上面的子图 - 类型分布
        ax2 = self.figure.add_subplot(212)  # 下面的子图 - 严重程度分布
        
        # 计算类型统计
        type_counts = {}
        for e in emergencies:
            type_name = e.type.name
            if type_name in type_counts:
                type_counts[type_name] += 1
            else:
                type_counts[type_name] = 1
        
        # 绘制类型分布饼图
        labels = list(type_counts.keys())
        sizes = list(type_counts.values())
        colors = ['red', 'green', 'blue']
        
        ax1.pie(
            sizes, 
            labels=labels,
            colors=colors, 
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90
        )
        ax1.axis('equal')
        ax1.set_title('Emergency Type Distribution')
        
        # 计算严重程度统计
        severity_counts = {}
        for e in emergencies:
            severity = e.severity_level
            if severity in severity_counts:
                severity_counts[severity] += 1
            else:
                severity_counts[severity] = 1
        
        # 绘制严重程度条形图
        x = sorted(severity_counts.keys())
        y = [severity_counts[i] for i in x]
        
        bars = ax2.bar(x, y, color='skyblue', edgecolor='black')
        
        # 在条形上方添加数值标签
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax2.text(
                    bar.get_x() + bar.get_width()/2.,
                    height + 0.1,
                    str(int(height)),
                    ha='center', 
                    va='bottom'
                )
        
        ax2.set_xlabel('Severity (Lower value = Higher priority)')
        ax2.set_ylabel('Count')
        ax2.set_title('Emergency Severity Distribution')
        
        # 调整子图之间的间距
        self.figure.tight_layout()
        
        # 更新画布
        self.canvas.draw()
    
    def _on_tree_hover(self, event):
        """当鼠标悬停在Treeview项目上时"""
        # 重命名 self.queue_tree 为 self.queue_tree_view
        item = self.queue_tree_view.identify_row(event.y)
        if item:
            self.status_var.set(f"Hovering over: {self.queue_tree_view.item(item)['values']}")
        else:
            self.status_var.set("Ready")
    
    def _on_tree_click(self, event):
        """当鼠标点击Treeview项目时，显示上下文菜单"""
        # 重命名 self.queue_tree 为 self.queue_tree_view
        item_id = self.queue_tree_view.identify_row(event.y)
        if not item_id:
            return

        # 选中被点击的行
        self.queue_tree_view.selection_set(item_id)
        
        # 获取紧急情况ID
        emergency_id_str = self.queue_tree_view.item(item_id)["values"][0]
        emergency_id = int(emergency_id_str)
        
        # 创建上下文菜单
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Change Priority", command=lambda: on_change_priority())
        context_menu.add_command(label="Delete", command=lambda: on_delete())
        
        # 更改优先级按钮
        def on_change_priority():
            # 询问新的严重性级别
            new_severity = askinteger(
                "Change Priority", 
                f"Current severity: {self.current_queue.search(emergency_id).severity_level}\nEnter new severity level (1-10):\n\nNote: Lower value = Higher priority (1 is most urgent)",
                minvalue=1, 
                maxvalue=10,
                parent=self.root
            )
            
            if new_severity is None:
                return
            
            # 在所有队列中更改优先级
            self.linked_list_queue.change_priority(emergency_id, new_severity)
            self.binary_tree_queue.change_priority(emergency_id, new_severity)
            self.heap_queue.change_priority(emergency_id, new_severity)
            
            # 更新显示
            self._update_queue_display()
            
            # 关闭对话框
            self.root.update()
            
            # 更新状态
            self.status_var.set(f"Changed priority of emergency {emergency_id} to {new_severity}")
        
        # 删除按钮
        def on_delete():
            # 请求确认
            if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete emergency {emergency_id}?", parent=self.root):
                return
            
            # 我们不能直接从优先级队列中删除，所以我们需要重建它们
            
            # 获取除要删除的紧急情况外的所有紧急情况
            linked_list_emergencies = [e for e in self.linked_list_queue if e.emergency_id != emergency_id]
            binary_tree_emergencies = [e for e in self.binary_tree_queue if e.emergency_id != emergency_id]
            heap_emergencies = [e for e in self.heap_queue if e.emergency_id != emergency_id]
            
            # 清除队列
            self._clear_queue()
            
            # 重新添加紧急情况
            for e in linked_list_emergencies:
                self.linked_list_queue.enqueue(e)
            
            for e in binary_tree_emergencies:
                self.binary_tree_queue.enqueue(e)
            
            for e in heap_emergencies:
                self.heap_queue.enqueue(e)
            
            # 更新显示
            self._update_queue_display()
            
            # 关闭对话框
            self.root.update()
            
            # 更新状态
            self.status_var.set(f"Deleted emergency {emergency_id}")
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def _clear_queue(self):
        """清空所有队列中的所有紧急情况"""
        # 清空所有三个队列以保持同步
        while not self.linked_list_queue.is_empty():
            self.linked_list_queue.dequeue()
        while not self.binary_tree_queue.is_empty():
            self.binary_tree_queue.dequeue()
        while not self.heap_queue.is_empty():
            self.heap_queue.dequeue()

        self._update_queue_display()
        messagebox.showinfo("Success", "All queues have been cleared.")

    def _on_canvas_hover(self, event):
        """当鼠标在Canvas上移动时，检测是否悬停在节点上"""
        emergency_id = self._find_node_at_position(event.x, event.y)
        if emergency_id:
            emergency = self.current_queue.search(emergency_id)
            if emergency:
                self.status_var.set(f"ID: {emergency.emergency_id}, Type: {emergency.type.name}, Severity: {emergency.severity_level}, Location: {emergency.location}")
                self.tree_canvas.config(cursor="hand2")  # 改变鼠标指针
            else:
                self.status_var.set("Ready")
                self.tree_canvas.config(cursor="")
        else:
            self.status_var.set("Ready")
            self.tree_canvas.config(cursor="")

    def _on_canvas_click(self, event):
        """当点击Canvas上的节点时，显示上下文菜单"""
        emergency_id = self._find_node_at_position(event.x, event.y)
        if not emergency_id:
            return
            
        emergency = self.current_queue.search(emergency_id)
        if not emergency:
            return
            
        # 创建上下文菜单
        context_menu = tk.Menu(self.root, tearoff=0)
        
        # 更改优先级菜单项
        context_menu.add_command(
            label="Change Priority", 
            command=lambda: self._change_node_priority(emergency_id)
        )
        
        # 删除菜单项
        context_menu.add_command(
            label="Delete", 
            command=lambda: self._delete_node(emergency_id)
        )
        
        # 显示上下文菜单
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def _find_node_at_position(self, x, y):
        """检查给定的坐标是否在某个节点内"""
        for emergency_id, (node_x, node_y, radius) in self.tree_nodes.items():
            # 使用距离公式检查点是否在圆内
            if (x - node_x) ** 2 + (y - node_y) ** 2 <= radius ** 2:
                return emergency_id
        return None

    def _change_node_priority(self, emergency_id):
        """更改节点优先级"""
        # 获取当前紧急情况
        emergency = self.current_queue.search(emergency_id)
        if not emergency:
            return
            
        # 询问新的严重程度
        new_severity = askinteger(
            "Change Priority",
            f"Current severity: {emergency.severity_level}\nEnter new severity level (1-10):\n\nNote: Lower value = Higher priority (1 is most urgent)",
            minvalue=1,
            maxvalue=10,
            parent=self.root
        )
        
        if new_severity is None:  # 用户取消
            return
            
        # 更新所有队列
        if self.current_queue_type.get() == "linked_list":
            self.linked_list_queue.change_priority(emergency_id, new_severity)
            self.binary_tree_queue.change_priority(emergency_id, new_severity)
            self.heap_queue.change_priority(emergency_id, new_severity)
        elif self.current_queue_type.get() == "binary_tree":
            self.binary_tree_queue.change_priority(emergency_id, new_severity)
            self.linked_list_queue.change_priority(emergency_id, new_severity)
            self.heap_queue.change_priority(emergency_id, new_severity)
        else:  # heap
            self.heap_queue.change_priority(emergency_id, new_severity)
            self.linked_list_queue.change_priority(emergency_id, new_severity)
            self.binary_tree_queue.change_priority(emergency_id, new_severity)
            
        # 更新显示
        self._update_queue_display()
        self.status_var.set(f"Changed priority of emergency {emergency_id} to {new_severity}")

    def _delete_node(self, emergency_id):
        """删除节点"""
        from tkinter import messagebox
        
        # 请求确认
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete emergency {emergency_id}?", parent=self.root):
            return
            
        # 从所有队列中删除
        # 首先从当前队列中获取紧急情况对象
        emergency = self.current_queue.search(emergency_id)
        if not emergency:
            return
            
        # 从链表队列中删除
        temp_list = []
        while not self.linked_list_queue.is_empty():
            item = self.linked_list_queue.dequeue()
            if item.emergency_id != emergency_id:
                temp_list.append(item)
                
        # 重新入队
        for item in temp_list:
            self.linked_list_queue.enqueue(item)
            
        # 从二叉树队列中删除
        self.binary_tree_queue.remove(emergency_id)
        
        # 从堆队列中删除
        # 由于堆没有直接的删除方法，我们需要重建堆
        temp_list = []
        while not self.heap_queue.is_empty():
            item = self.heap_queue.dequeue()
            if item.emergency_id != emergency_id:
                temp_list.append(item)
                
        # 重新入队
        for item in temp_list:
            self.heap_queue.enqueue(item)
            
        # 更新显示
        self._update_queue_display()
        self.status_var.set(f"Deleted emergency {emergency_id}")

def run_gui():
    """运行应急响应管理系统GUI"""
    root = tk.Tk()
    app = EmergencyResponseGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui() 