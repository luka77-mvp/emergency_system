import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random
import numpy as np
from emergency_response.data_structures.emergency import Emergency, EmergencyType
from emergency_response.data_structures.linked_list import LinkedListPriorityQueue
from emergency_response.data_structures.binary_tree import BinaryTreePriorityQueue
from emergency_response.data_structures.heap import HeapPriorityQueue
from emergency_response.utils.performance_analyzer import PerformanceAnalyzer

class EmergencySimulationGUI:
    """Emergency Dispatch Simulation Interface"""
    
    def __init__(self, root):
        """
        Initialize the interface
        
        Parameters:
            root: tkinter root window
        """
        self.root = root
        self.root.title("Emergency Dispatch Simulation")
        self.root.geometry("1000x700")
        
        # Create queues
        self.linked_list_queue = LinkedListPriorityQueue()
        self.binary_tree_queue = BinaryTreePriorityQueue()
        self.heap_queue = HeapPriorityQueue()
        
        # 创建性能分析器
        self.performance_analyzer = PerformanceAnalyzer()
        
        # Simulation parameters
        self.emergency_count = tk.IntVar(value=1000)
        self.simulation_runs = tk.IntVar(value=5)
        self.emergency_types = [EmergencyType.FIRE, EmergencyType.MEDICAL, EmergencyType.POLICE]
        self.locations = ["Downtown", "Suburbs", "Industrial Zone", "Residential Area", "Commercial District"]
        
        # Create interface components
        self._create_widgets()
        
        # Simulation results
        self.results = {}
    
    def _create_widgets(self):
        """Create interface components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Emergency Dispatch Simulation", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Simulation Parameters", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Emergency count
        count_frame = ttk.Frame(control_frame)
        count_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(count_frame, text="Number of Emergencies:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(
            count_frame, 
            from_=100, 
            to=10000, 
            increment=100, 
            textvariable=self.emergency_count,
            width=8
        ).pack(side=tk.LEFT, padx=5)
        
        # Simulation runs
        runs_frame = ttk.Frame(control_frame)
        runs_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(runs_frame, text="Number of Simulation Runs:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(
            runs_frame, 
            from_=1, 
            to=20, 
            increment=1, 
            textvariable=self.simulation_runs,
            width=8
        ).pack(side=tk.LEFT, padx=5)
        
        # Run buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Run Simulation",
            width=15,
            command=self._run_simulation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Run Space Test",
            width=15,
            command=self._run_space_test
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Clear Results",
            width=15,
            command=self._clear_results
        ).pack(side=tk.LEFT, padx=5)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        tab_control = ttk.Notebook(results_frame)
        tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Processing time comparison tab
        time_tab = ttk.Frame(tab_control, padding="10")
        tab_control.add(time_tab, text="Processing Time")
        
        # Create time comparison chart
        self.time_figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.time_canvas = FigureCanvasTkAgg(self.time_figure, master=time_tab)
        self.time_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Throughput comparison tab
        throughput_tab = ttk.Frame(tab_control, padding="10")
        tab_control.add(throughput_tab, text="Throughput")
        
        # Create throughput comparison chart
        self.throughput_figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.throughput_canvas = FigureCanvasTkAgg(self.throughput_figure, master=throughput_tab)
        self.throughput_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 空间复杂度比较选项卡
        space_tab = ttk.Frame(tab_control, padding="10")
        tab_control.add(space_tab, text="Space Complexity")
        
        # 创建空间复杂度比较图表
        self.space_figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.space_canvas = FigureCanvasTkAgg(self.space_figure, master=space_tab)
        self.space_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Simulation details tab
        details_tab = ttk.Frame(tab_control, padding="10")
        tab_control.add(details_tab, text="Details")
        
        # Create text box to display simulation details
        details_frame = ttk.Frame(details_tab)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(details_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.details_text.yview)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to run simulation")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
    
    def _generate_random_emergencies(self, count):
        """Generate random emergency data"""
        emergencies = []
        
        for i in range(count):
            emergency_id = i + 1
            emergency_type = random.choice(self.emergency_types)
            severity_level = random.randint(1, 10)
            location = random.choice(self.locations)
            
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            
            emergency = Emergency(
                emergency_id=emergency_id,
                emergency_type=emergency_type,
                severity_level=severity_level,
                location=location,
                coordinates=(x, y)
            )
            
            emergencies.append(emergency)
        
        return emergencies
    
    def _run_simulation(self):
        """Run simulation"""
        try:
            # Get parameters
            count = self.emergency_count.get()
            runs = self.simulation_runs.get()
            
            if count <= 0 or runs <= 0:
                messagebox.showerror("Error", "Number of emergencies and simulation runs must be positive")
                return
            
            # Clear results
            self.results = {
                'linked_list': {'enqueue': [], 'dequeue': [], 'total': []},
                'binary_tree': {'enqueue': [], 'dequeue': [], 'total': []},
                'heap': {'enqueue': [], 'dequeue': [], 'total': []}
            }
            
            # Update status
            self.status_var.set("Running simulation...")
            self.root.update()
            
            # Run multiple simulations and average the results
            for run in range(runs):
                # Generate random emergencies
                emergencies = self._generate_random_emergencies(count)
                
                # Simulate each queue type
                self._simulate_queue('linked_list', self.linked_list_queue, emergencies)
                self._simulate_queue('binary_tree', self.binary_tree_queue, emergencies)
                self._simulate_queue('heap', self.heap_queue, emergencies)
                
                # Update progress
                self.status_var.set(f"Running simulation... ({run+1}/{runs})")
                self.root.update()
            
            # Calculate averages
            linked_list_avg = {
                'enqueue': sum(self.results['linked_list']['enqueue']) / runs,
                'dequeue': sum(self.results['linked_list']['dequeue']) / runs,
                'total': sum(self.results['linked_list']['total']) / runs
            }
            
            binary_tree_avg = {
                'enqueue': sum(self.results['binary_tree']['enqueue']) / runs,
                'dequeue': sum(self.results['binary_tree']['dequeue']) / runs,
                'total': sum(self.results['binary_tree']['total']) / runs
            }
            
            heap_avg = {
                'enqueue': sum(self.results['heap']['enqueue']) / runs,
                'dequeue': sum(self.results['heap']['dequeue']) / runs,
                'total': sum(self.results['heap']['total']) / runs
            }
            
            # Plot results
            self._plot_time_comparison(linked_list_avg, binary_tree_avg, heap_avg)
            self._plot_throughput_comparison(linked_list_avg, binary_tree_avg, heap_avg, count)
            
            # Display detailed results
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Simulation Results (Average of {runs} runs, {count} emergencies each):\n\n")
            
            self.details_text.insert(tk.END, "Linked List Priority Queue:\n")
            self.details_text.insert(tk.END, f"  Enqueue Time: {linked_list_avg['enqueue']:.6f} seconds\n")
            self.details_text.insert(tk.END, f"  Dequeue Time: {linked_list_avg['dequeue']:.6f} seconds\n")
            self.details_text.insert(tk.END, f"  Total Time: {linked_list_avg['total']:.6f} seconds\n\n")
            
            self.details_text.insert(tk.END, "Binary Tree Priority Queue:\n")
            self.details_text.insert(tk.END, f"  Enqueue Time: {binary_tree_avg['enqueue']:.6f} seconds\n")
            self.details_text.insert(tk.END, f"  Dequeue Time: {binary_tree_avg['dequeue']:.6f} seconds\n")
            self.details_text.insert(tk.END, f"  Total Time: {binary_tree_avg['total']:.6f} seconds\n\n")
            
            self.details_text.insert(tk.END, "Heap Priority Queue:\n")
            self.details_text.insert(tk.END, f"  Enqueue Time: {heap_avg['enqueue']:.6f} seconds\n")
            self.details_text.insert(tk.END, f"  Dequeue Time: {heap_avg['dequeue']:.6f} seconds\n")
            self.details_text.insert(tk.END, f"  Total Time: {heap_avg['total']:.6f} seconds\n\n")
            
            # Calculate improvement percentages
            ll_total = linked_list_avg['total']
            bt_total = binary_tree_avg['total']
            heap_total = heap_avg['total']
            
            bt_improvement = ((ll_total - bt_total) / ll_total) * 100
            heap_improvement = ((ll_total - heap_total) / ll_total) * 100
            
            self.details_text.insert(tk.END, "Performance Improvement:\n")
            self.details_text.insert(tk.END, f"  Binary Tree vs. Linked List: {bt_improvement:.2f}%\n")
            self.details_text.insert(tk.END, f"  Heap vs. Linked List: {heap_improvement:.2f}%\n\n")
            
            fastest = min(ll_total, bt_total, heap_total)
            if fastest == ll_total:
                fastest_name = "Linked List"
            elif fastest == bt_total:
                fastest_name = "Binary Tree"
            else:
                fastest_name = "Heap"
                
            self.details_text.insert(tk.END, f"Fastest Implementation: {fastest_name} Priority Queue\n")
            
            # Update status
            self.status_var.set("Simulation completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")
            self.status_var.set("Simulation failed")
    
    def _run_space_test(self):
        """运行空间复杂度测试"""
        try:
            # 获取参数
            count = self.emergency_count.get()
            
            if count <= 0:
                messagebox.showerror("Error", "Number of emergencies must be positive")
                return
            
            # 更新状态
            self.status_var.set("Running space complexity test...")
            self.root.update()
            
            # 定义不同的数据大小
            # 使用更多的数据点以获得更平滑的曲线
            max_size = count
            # 确保至少有8个数据点
            data_sizes = []
            if max_size <= 1000:
                # 对于较小的数据集，使用均匀间隔
                step = max(1, max_size // 8)
                data_sizes = list(range(step, max_size + 1, step))
            else:
                # 对于较大的数据集，使用指数间隔，以便更好地观察趋势
                sizes = [100, 200, 400, 600, 800, 1000]
                sizes.extend([s for s in range(2000, max_size + 1, 1000) if s <= max_size])
                if max_size not in sizes:
                    sizes.append(max_size)
                data_sizes = sizes
            
            # 执行空间复杂度测试
            self.performance_analyzer.measure_space_complexity(data_sizes)
            
            # 绘制结果
            self._plot_space_comparison(data_sizes)
            
            # 更新详细信息
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Space Complexity Test Results (Max size: {max_size} emergencies):\n\n")
            
            space_results = self.performance_analyzer.results.get('space', {})
            
            if 'Linked List' in space_results and space_results['Linked List']:
                ll_space = space_results['Linked List'][-1]
                self.details_text.insert(tk.END, f"Linked List Memory Usage: {ll_space:.6f} KB\n\n")
            
            if 'Binary Tree' in space_results and space_results['Binary Tree']:
                bt_space = space_results['Binary Tree'][-1]
                self.details_text.insert(tk.END, f"Binary Tree Memory Usage: {bt_space:.6f} KB\n\n")
            
            if 'Heap' in space_results and space_results['Heap']:
                heap_space = space_results['Heap'][-1]
                self.details_text.insert(tk.END, f"Heap Memory Usage: {heap_space:.6f} KB\n\n")
            
            # 理论复杂度分析
            complexity_analysis = self.performance_analyzer.get_complexity_analysis()
            space_complexity = complexity_analysis['space']
            
            self.details_text.insert(tk.END, "Theoretical Space Complexity:\n")
            for i, structure in enumerate(space_complexity['Data Structure']):
                self.details_text.insert(tk.END, f"  {structure}: {space_complexity['Complexity'][i]}\n")
            
            # 更新状态
            self.status_var.set("Space complexity test completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Space complexity test failed: {str(e)}")
            self.status_var.set("Space complexity test failed")
    
    def _simulate_queue(self, queue_name, queue, emergencies):
        """Simulate operations on a specific queue type"""
        # Clear the queue
        while not queue.is_empty():
            queue.dequeue()
        
        # Measure enqueue time
        start_time = time.perf_counter()
        for emergency in emergencies:
            queue.enqueue(emergency)
        end_time = time.perf_counter()
        enqueue_time = end_time - start_time
        
        # Measure dequeue time
        start_time = time.perf_counter()
        while not queue.is_empty():
            queue.dequeue()
        end_time = time.perf_counter()
        dequeue_time = end_time - start_time
        
        # Calculate total time
        total_time = enqueue_time + dequeue_time
        
        # Store results
        self.results[queue_name]['enqueue'].append(enqueue_time)
        self.results[queue_name]['dequeue'].append(dequeue_time)
        self.results[queue_name]['total'].append(total_time)
    
    def _plot_time_comparison(self, linked_list_avg, binary_tree_avg, heap_avg):
        """Plot time comparison chart"""
        # Clear previous plot
        self.time_figure.clear()
        
        # Create new plot
        ax = self.time_figure.add_subplot(111)
        
        # Data for plotting
        queue_types = ['Linked List', 'Binary Tree', 'Heap']
        enqueue_times = [linked_list_avg['enqueue'], binary_tree_avg['enqueue'], heap_avg['enqueue']]
        dequeue_times = [linked_list_avg['dequeue'], binary_tree_avg['dequeue'], heap_avg['dequeue']]
        
        # Set width of bars
        bar_width = 0.35
        
        # Set position of bar on X axis
        r1 = np.arange(len(queue_types))
        r2 = [x + bar_width for x in r1]
        
        # Make the plot
        ax.bar(r1, enqueue_times, width=bar_width, label='Enqueue Time')
        ax.bar(r2, dequeue_times, width=bar_width, label='Dequeue Time')
        
        # Add labels and title
        ax.set_xlabel('Queue Implementation')
        ax.set_ylabel('Time (seconds)')
        ax.set_title('Processing Time Comparison')
        ax.set_xticks([r + bar_width/2 for r in range(len(queue_types))])
        ax.set_xticklabels(queue_types)
        ax.legend()
        
        # Redraw the canvas
        self.time_canvas.draw()
    
    def _plot_throughput_comparison(self, linked_list_avg, binary_tree_avg, heap_avg, count):
        """Plot throughput comparison chart"""
        # Clear previous plot
        self.throughput_figure.clear()
        
        # Create new plot
        ax = self.throughput_figure.add_subplot(111)
        
        # Calculate throughput (operations per second)
        ll_enqueue_throughput = count / linked_list_avg['enqueue'] if linked_list_avg['enqueue'] > 0 else 0
        ll_dequeue_throughput = count / linked_list_avg['dequeue'] if linked_list_avg['dequeue'] > 0 else 0
        
        bt_enqueue_throughput = count / binary_tree_avg['enqueue'] if binary_tree_avg['enqueue'] > 0 else 0
        bt_dequeue_throughput = count / binary_tree_avg['dequeue'] if binary_tree_avg['dequeue'] > 0 else 0
        
        heap_enqueue_throughput = count / heap_avg['enqueue'] if heap_avg['enqueue'] > 0 else 0
        heap_dequeue_throughput = count / heap_avg['dequeue'] if heap_avg['dequeue'] > 0 else 0
        
        # Data for plotting
        queue_types = ['Linked List', 'Binary Tree', 'Heap']
        enqueue_throughput = [ll_enqueue_throughput, bt_enqueue_throughput, heap_enqueue_throughput]
        dequeue_throughput = [ll_dequeue_throughput, bt_dequeue_throughput, heap_dequeue_throughput]
        
        # Set width of bars
        bar_width = 0.35
        
        # Set position of bar on X axis
        r1 = np.arange(len(queue_types))
        r2 = [x + bar_width for x in r1]
        
        # Make the plot
        ax.bar(r1, enqueue_throughput, width=bar_width, label='Enqueue Throughput')
        ax.bar(r2, dequeue_throughput, width=bar_width, label='Dequeue Throughput')
        
        # Add labels and title
        ax.set_xlabel('Queue Implementation')
        ax.set_ylabel('Operations per Second')
        ax.set_title('Throughput Comparison')
        ax.set_xticks([r + bar_width/2 for r in range(len(queue_types))])
        ax.set_xticklabels(queue_types)
        ax.legend()
        
        # Redraw the canvas
        self.throughput_canvas.draw()
    
    def _plot_space_comparison(self, data_sizes):
        """绘制空间复杂度比较图表"""
        # 清除之前的图表
        self.space_figure.clear()
        
        # 创建新图表
        ax = self.space_figure.add_subplot(111)
        
        # 获取空间复杂度结果
        space_results = self.performance_analyzer.results.get('space', {})
        
        # 绘制每种数据结构的空间使用情况
        for queue_type, memory_usage in space_results.items():
            ax.plot(data_sizes, memory_usage, marker='o', linestyle='-', label=queue_type)
        
        # 添加标签和标题
        ax.set_xlabel('Number of Emergencies (Data Size)')
        ax.set_ylabel('Memory Usage (KB)')
        ax.set_title('Space Complexity Comparison')
        ax.legend()
        ax.grid(True)
        
        # 重绘画布
        self.space_canvas.draw()
    
    def _clear_results(self):
        """Clear simulation results"""
        # Clear results data
        self.results = {}
        
        # Clear plots
        self.time_figure.clear()
        self.time_canvas.draw()
        
        self.throughput_figure.clear()
        self.throughput_canvas.draw()
        
        self.space_figure.clear()
        self.space_canvas.draw()
        
        # Clear details text
        self.details_text.delete(1.0, tk.END)
        
        # Update status
        self.status_var.set("Results cleared")

def run_simulation_gui():
    """Run the emergency dispatch simulation GUI"""
    # Create a new window
    simulation_window = tk.Toplevel()
    EmergencySimulationGUI(simulation_window)
    
    # Return the window object so it doesn't get garbage collected
    return simulation_window

if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencySimulationGUI(root)
    root.mainloop() 