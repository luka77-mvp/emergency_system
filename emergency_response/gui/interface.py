import tkinter as tk
from tkinter import ttk, messagebox
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
        # 创建包含队列显示和图表的框架
        display_frame = ttk.Frame(self.main_frame)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧队列显示
        queue_frame = ttk.LabelFrame(display_frame, text="Emergency Queue", padding="10")
        queue_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建Treeview以显示队列内容
        columns = ("id", "type", "severity", "location")
        self.queue_tree = ttk.Treeview(queue_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.queue_tree.heading("id", text="ID")
        self.queue_tree.heading("type", text="Type")
        self.queue_tree.heading("severity", text="Severity (Lower value = Higher priority)")
        self.queue_tree.heading("location", text="Location")
        
        # 设置列宽
        self.queue_tree.column("id", width=50)
        self.queue_tree.column("type", width=100)
        self.queue_tree.column("severity", width=100)
        self.queue_tree.column("location", width=150)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(queue_frame, orient=tk.VERTICAL, command=self.queue_tree.yview)
        self.queue_tree.configure(yscroll=scrollbar.set)
        
        # 放置组件
        self.queue_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
        self.queue_tree.bind("<Motion>", self._on_tree_hover)
        self.queue_tree.bind("<Button-1>", self._on_tree_click)
    
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
        processed_ll = self.linked_list_queue.dequeue()
        processed_bt = self.binary_tree_queue.dequeue()
        processed_heap = self.heap_queue.dequeue()
        
        # 理论上，因为它们是同步的，所以它们应该是相同的
        # 我们只显示其中一个的结果
        messagebox.showinfo(
            "Emergency Processed",
            f"Processed Emergency:\n\n"
            f"ID: {processed_heap.emergency_id}\n"
            f"Type: {processed_heap.type.name}\n"
            f"Severity: {processed_heap.severity_level}"
        )
        
        self._update_queue_display()
    
    def _search_emergency(self):
        """按ID搜索紧急情况"""
        # 询问紧急情况ID
        emergency_id = askinteger(self.root, "Search Emergency", "Enter Emergency ID:")
        
        if emergency_id is None:
            return
        
        # 在当前队列中搜索
        start_time = time.perf_counter()
        emergency = self.current_queue.search(emergency_id)
        end_time = time.perf_counter()
        search_time = end_time - start_time
        
        if emergency:
            messagebox.showinfo(
                "Emergency Found",
                f"ID: {emergency.emergency_id}\n"
                f"Type: {emergency.type.name}\n"
                f"Severity: {emergency.severity_level} (Lower value = Higher priority)\n"
                f"Location: {emergency.location}\n"
                f"Coordinates: {emergency.coordinates}\n\n"
                f"Search time: {search_time:.6f} seconds"
            )
            
            # 更新状态
            self.status_var.set(f"Found emergency {emergency_id} in {search_time:.6f} seconds")
        else:
            messagebox.showinfo("Not Found", f"No emergency found with ID {emergency_id}")
            
            # 更新状态
            self.status_var.set(f"Emergency {emergency_id} not found")
    
    def _change_priority(self):
        """更改紧急情况的优先级（严重性级别）"""
        # 询问紧急情况ID
        emergency_id = askinteger(self.root, "Change Priority", "Enter Emergency ID:")
        
        if emergency_id is None:
            return
        
        # 在当前队列中搜索
        emergency = self.current_queue.search(emergency_id)
        
        if not emergency:
            messagebox.showinfo("Not Found", f"No emergency found with ID {emergency_id}")
            return
        
        # 询问新的严重性级别
        new_severity = askinteger(
            self.root,
            "Change Priority", 
            f"Current severity: {emergency.severity_level}\nEnter new severity level (1-10):\n\nNote: Lower value = Higher priority (1 is most urgent)",
            minvalue=1, 
            maxvalue=10
        )
        
        if new_severity is None:
            return
        
        # 在所有队列中更改优先级
        self.linked_list_queue.change_priority(emergency_id, new_severity)
        self.binary_tree_queue.change_priority(emergency_id, new_severity)
        self.heap_queue.change_priority(emergency_id, new_severity)
        
        # 更新显示
        self._update_queue_display()
        
        # 更新状态
        self.status_var.set(f"Changed priority of emergency {emergency_id} to {new_severity}")
    
    def _show_statistics(self):
        """显示队列统计信息"""
        # 从当前队列中获取所有紧急情况
        emergencies = list(self.current_queue)
        
        if not emergencies:
            messagebox.showinfo("Notice", "No emergencies in the queue to analyze")
            return
        
        # 运行统计GUI
        run_statistics_gui(emergencies)
    
    def _run_performance_analysis(self):
        """运行性能分析"""
        # 此方法现在为空，因为性能分析已被移除
        pass
    
    def _update_queue_display(self):
        """更新队列显示"""
        # 清除现有项目
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        
        # 从当前队列添加紧急情况
        for emergency in self.current_queue:
            self.queue_tree.insert(
                "", 
                "end", 
                values=(
                    emergency.emergency_id,
                    emergency.type.name,
                    emergency.severity_level,
                    emergency.location
                ),
                tags=(str(emergency.emergency_id),)
            )
        
        # 更新队列信息
        queue_size = len(self.current_queue)
        queue_type = self._get_queue_type_name()
        self.queue_info_var.set(f"Queue: {queue_type}, Size: {queue_size}")
        
        # 更新统计图表
        self._update_statistics_chart()
    
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
        """处理树视图上的鼠标悬停"""
        # 获取光标下的项目
        item = self.queue_tree.identify_row(event.y)
        if not item:
            return
        
        # 从项目中获取紧急情况ID
        values = self.queue_tree.item(item, 'values')
        if not values:
            return
        
        emergency_id = int(values[0])
        
        # 在当前队列中查找紧急情况
        emergency = self.current_queue.search(emergency_id)
        if not emergency:
            return
        
        # 使用紧急情况信息更新状态栏
        self.status_var.set(
            f"ID: {emergency.emergency_id}, "
            f"Type: {emergency.type.name}, "
            f"Severity: {emergency.severity_level} (Lower value = Higher priority), "
            f"Location: {emergency.location}"
        )
    
    def _on_tree_click(self, event):
        """处理树视图上的点击"""
        # 获取光标下的项目
        item = self.queue_tree.identify_row(event.y)
        if not item:
            return
        
        # 从项目中获取紧急情况ID
        values = self.queue_tree.item(item, 'values')
        if not values:
            return
        
        emergency_id = int(values[0])
        
        # 在当前队列中查找紧急情况
        emergency = self.current_queue.search(emergency_id)
        if not emergency:
            return
        
        # 显示紧急情况详情对话框
        details_dialog = tk.Toplevel(self.root)
        details_dialog.title(f"Emergency {emergency_id} Details")
        details_dialog.geometry("400x300")
        details_dialog.transient(self.root)
        details_dialog.grab_set()
        
        # 创建详情框架
        details_frame = ttk.Frame(details_dialog, padding="20")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # 显示紧急情况详情
        ttk.Label(details_frame, text="Emergency Details", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        ttk.Label(details_frame, text="ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=str(emergency.emergency_id)).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(details_frame, text="Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=emergency.type.name).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(details_frame, text="Severity:").grid(row=3, column=0, sticky=tk.W, pady=5)
        severity_frame = ttk.Frame(details_frame)
        severity_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Label(severity_frame, text=str(emergency.severity_level)).pack(side=tk.LEFT)
        ttk.Label(severity_frame, text=" (Lower value = Higher priority)", font=("Arial", 9, "italic")).pack(side=tk.LEFT)
        
        ttk.Label(details_frame, text="Location:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=emergency.location).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(details_frame, text="Coordinates:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=f"({emergency.coordinates[0]}, {emergency.coordinates[1]})").grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # 添加按钮
        buttons_frame = ttk.Frame(details_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # 更改优先级按钮
        def on_change_priority():
            # 询问新的严重性级别
            new_severity = askinteger(
                details_dialog,
                "Change Priority", 
                f"Current severity: {emergency.severity_level}\nEnter new severity level (1-10):\n\nNote: Lower value = Higher priority (1 is most urgent)",
                minvalue=1, 
                maxvalue=10
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
            details_dialog.destroy()
            
            # 更新状态
            self.status_var.set(f"Changed priority of emergency {emergency_id} to {new_severity}")
        
        ttk.Button(buttons_frame, text="Change Priority", command=on_change_priority).pack(side=tk.LEFT, padx=5)
        
        # 删除按钮
        def on_delete():
            # 请求确认
            if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete emergency {emergency_id}?", parent=details_dialog):
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
            details_dialog.destroy()
            
            # 更新状态
            self.status_var.set(f"Deleted emergency {emergency_id}")
        
        ttk.Button(buttons_frame, text="Delete", command=on_delete).pack(side=tk.LEFT, padx=5)
        
        # 关闭按钮
        ttk.Button(buttons_frame, text="Close", command=details_dialog.destroy).pack(side=tk.LEFT, padx=5)

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

def run_gui():
    """运行应急响应管理系统GUI"""
    root = tk.Tk()
    app = EmergencyResponseGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui() 