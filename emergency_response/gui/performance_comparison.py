# 创建滚动条
self.scrollbar = tk.Scrollbar(self.complexity_frame)
self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 创建一个框架来放置复杂度信息
self.complexity_frame = tk.Frame(self.root)
self.complexity_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 将复杂度信息放入框架中
self.complexity_text = tk.Text(self.complexity_frame, yscrollcommand=self.scrollbar.set)
self.complexity_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
self.scrollbar.config(command=self.complexity_text.yview)

# 添加复杂度信息
self.complexity_text.insert(tk.END, "Time Complexity:\nEnqueue O(n), Dequeue O(1), Search O(n) for Linked List; Enqueue O(log n), Dequeue O(log n), Search O(n) for Binary Tree; Enqueue O(log n), Dequeue O(log n), Search O(1) for Heap\n\nSpace Complexity:\nO(n) for all structures") 