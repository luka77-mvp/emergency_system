"""
用于创建始终置顶的对话框的自定义对话框模块
"""
import tkinter as tk
from tkinter import ttk, messagebox

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