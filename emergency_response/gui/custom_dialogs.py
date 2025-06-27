"""
用于创建始终置顶的对话框的自定义对话框模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
from ..data_structures.emergency import Emergency, EmergencyType

class CustomIntegerDialog:
    """始终置顶的自定义整数输入对话框"""
    
    def __init__(self, parent, title, prompt, initialvalue=None, minvalue=None, maxvalue=None):
        """
        初始化对话框
        
        Parameters:
            parent: 父窗口
            title: 对话框标题
            prompt: 提示文本
            initialvalue: 初始值
            minvalue: 最小值
            maxvalue: 最大值
        """
        self.result = None
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#f0f0f0")  # 设置背景颜色
        
        # 设置为模态和顶层
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.focus_set()
        
        # 始终置顶
        self.dialog.attributes('-topmost', True)
        
        # 创建对话框内容 - 使用简单的Frame而不是ttk.Frame
        main_frame = tk.Frame(self.dialog, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 提示文本 - 使用标准的tk.Label
        tk.Label(main_frame, text=prompt, wraplength=250, font=("Arial", 10), bg="#f0f0f0").pack(pady=(0, 15))
        
        # 输入字段
        self.value_var = tk.IntVar()
        if initialvalue is not None:
            self.value_var.set(initialvalue)
        
        # 设置验证命令
        vcmd = (self.dialog.register(self._validate), '%P')
        
        # 创建输入字段 - 使用标准的tk.Entry
        self.entry = tk.Entry(
            main_frame, 
            textvariable=self.value_var, 
            validate="key", 
            validatecommand=vcmd,
            width=15,
            font=("Arial", 11),
            justify=tk.CENTER,  # 居中对齐文本
            relief=tk.SUNKEN,   # 添加凹陷效果
            borderwidth=2       # 设置边框宽度
        )
        self.entry.pack(pady=10)
        self.entry.focus_set()
        
        # 保存最小值和最大值
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # 使用标准的tk.Button而不是ttk.Button以确保在所有平台上的正确显示
        # OK按钮
        ok_btn = tk.Button(button_frame, text="OK", width=10, 
                          command=self._on_ok, font=("Arial", 10),
                          bg="#e1e1e1", relief=tk.RAISED, borderwidth=2)
        ok_btn.pack(side=tk.LEFT, padx=20, expand=True)
        
        # 取消按钮
        cancel_btn = tk.Button(button_frame, text="Cancel", width=10,
                              command=self._on_cancel, font=("Arial", 10),
                              bg="#e1e1e1", relief=tk.RAISED, borderwidth=2)
        cancel_btn.pack(side=tk.RIGHT, padx=20, expand=True)
        
        # 绑定Enter和Escape键
        self.dialog.bind("<Return>", lambda event: self._on_ok())
        self.dialog.bind("<Escape>", lambda event: self._on_cancel())
        
        # 等待窗口关闭
        parent.wait_window(self.dialog)
    
    def _validate(self, value):
        """验证输入是否为整数"""
        if value == "":
            return True
        
        try:
            val = int(value)
            
            # 检查最小值和最大值
            if self.minvalue is not None and val < self.minvalue:
                return False
            if self.maxvalue is not None and val > self.maxvalue:
                return False
            
            return True
        except ValueError:
            return False
    
    def _on_ok(self):
        """OK按钮回调"""
        try:
            self.result = self.value_var.get()
            
            # 验证值是否在范围内
            if self.minvalue is not None and self.result < self.minvalue:
                tk.messagebox.showerror("Error", f"Value must be greater than or equal to {self.minvalue}")
                return
            
            if self.maxvalue is not None and self.result > self.maxvalue:
                tk.messagebox.showerror("Error", f"Value must be less than or equal to {self.maxvalue}")
                return
            
            self.dialog.destroy()
        except tk.TclError:
            tk.messagebox.showerror("Error", "Please enter a valid integer")
    
    def _on_cancel(self):
        """取消按钮回调"""
        self.dialog.destroy()

def askinteger(parent, title, prompt, initialvalue=None, minvalue=None, maxvalue=None):
    """
    显示整数输入对话框
    
    Parameters:
        parent: 父窗口
        title: 对话框标题
        prompt: 提示文本
        initialvalue: 初始值
        minvalue: 最小值
        maxvalue: 最大值
        
    Returns:
        用户输入的整数，如果用户取消则为None
    """
    dialog = CustomIntegerDialog(parent, title, prompt, initialvalue, minvalue, maxvalue)
    return dialog.result

class AddEmergencyDialog:
    """用于添加新紧急情况的自定义对话框"""
    
    def __init__(self, parent):
        """
        初始化对话框
        
        参数:
            parent: 父窗口
        """
        self.result = None
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Emergency")
        self.dialog.geometry("400x300")
        
        # 设置为模态
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 创建表单字段
        form_frame = ttk.Frame(self.dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 紧急情况ID
        ttk.Label(form_frame, text="Emergency ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_var = tk.IntVar(value=random.randint(1000, 9999))
        ttk.Entry(form_frame, textvariable=self.id_var, width=30).grid(row=0, column=1, pady=5)
        
        # 紧急情况类型
        ttk.Label(form_frame, text="Emergency Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="FIRE")
        type_combo = ttk.Combobox(form_frame, textvariable=self.type_var, width=27)
        type_combo['values'] = [e.name for e in EmergencyType]
        type_combo.grid(row=1, column=1, pady=5)
        
        # 严重性级别
        ttk.Label(form_frame, text="Severity Level (1-10):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.severity_var = tk.IntVar(value=5)
        ttk.Spinbox(form_frame, from_=1, to=10, textvariable=self.severity_var, width=28).grid(row=2, column=1, pady=5)
        
        # 添加严重性级别说明
        severity_note = ttk.Label(form_frame, text="Note: 1 is most urgent", font=("Arial", 9, "italic"))
        severity_note.grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # 位置
        ttk.Label(form_frame, text="Location:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.location_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.location_var, width=30).grid(row=3, column=1, pady=5)
        
        # 坐标
        ttk.Label(form_frame, text="Coordinates (x, y):").grid(row=4, column=0, sticky=tk.W, pady=5)
        coord_frame = ttk.Frame(form_frame)
        coord_frame.grid(row=4, column=1, pady=5)
        
        self.x_var = tk.DoubleVar(value=round(random.uniform(0, 100), 2))
        self.y_var = tk.DoubleVar(value=round(random.uniform(0, 100), 2))
        
        ttk.Entry(coord_frame, textvariable=self.x_var, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Label(coord_frame, text=",").pack(side=tk.LEFT)
        ttk.Entry(coord_frame, textvariable=self.y_var, width=12).pack(side=tk.LEFT, padx=2)
        
        # 提交按钮
        ttk.Button(form_frame, text="Add Emergency", command=self._on_submit).grid(row=5, column=0, columnspan=2, pady=20)
        
        # 等待窗口关闭
        self.dialog.wait_window(self.dialog)

    def _on_submit(self):
        """提交按钮回调"""
        try:
            # 从表单中获取值
            emergency_id = self.id_var.get()
            emergency_type_str = self.type_var.get()
            severity_level = self.severity_var.get()
            location = self.location_var.get()
            x = self.x_var.get()
            y = self.y_var.get()
            
            # 验证输入
            if not location:
                messagebox.showerror("Error", "Please enter a location", parent=self.dialog)
                return
            
            if not (1 <= severity_level <= 10):
                messagebox.showerror("Error", "Severity level must be between 1 and 10", parent=self.dialog)
                return
            
            # 将字符串转换为EmergencyType枚举
            emergency_type = EmergencyType[emergency_type_str]
            
            # 创建紧急情况对象并将其存储在结果中
            self.result = Emergency(
                emergency_id=emergency_id,
                emergency_type=emergency_type,
                severity_level=severity_level,
                location=location,
                coordinates=(x, y)
            )
            
            # 关闭对话框
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.dialog) 