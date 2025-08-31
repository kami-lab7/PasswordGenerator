import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("随机密码生成器")
        self.root.geometry("600x800")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置根窗口的网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🔐 随机密码生成器", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 密码长度设置
        length_frame = ttk.LabelFrame(main_frame, text="密码长度", padding="15")
        length_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(length_frame, from_=4, to=50, 
                                variable=self.length_var, orient=tk.HORIZONTAL)
        length_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 15))
        
        length_label = ttk.Label(length_frame, textvariable=self.length_var, 
                                font=("Arial", 14, "bold"), width=3)
        length_label.grid(row=0, column=1)
        
        # 字符类型选择
        chars_frame = ttk.LabelFrame(main_frame, text="字符类型", padding="15")
        chars_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(chars_frame, text="大写字母 (A-Z)", 
                       variable=self.uppercase_var).grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(chars_frame, text="小写字母 (a-z)", 
                       variable=self.lowercase_var).grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(chars_frame, text="数字 (0-9)", 
                       variable=self.numbers_var).grid(row=2, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(chars_frame, text="特殊符号 (!@#$%^&*)", 
                       variable=self.symbols_var).grid(row=3, column=0, sticky=tk.W, pady=3)
        
        # 生成按钮
        generate_btn = ttk.Button(main_frame, text="生成密码", 
                                 command=self.generate_password, style="Accent.TButton")
        generate_btn.grid(row=3, column=0, columnspan=2, pady=(0, 15))
        
        # 密码显示区域
        password_frame = ttk.LabelFrame(main_frame, text="生成的密码", padding="15")
        password_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                  font=("Courier", 16), state="readonly")
        password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 15))
        
        copy_btn = ttk.Button(password_frame, text="复制", command=self.copy_password)
        copy_btn.grid(row=0, column=1)
        
        # 历史记录
        history_frame = ttk.LabelFrame(main_frame, text="历史记录", padding="15")
        history_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # 创建树形视图显示历史记录
        columns = ("时间", "密码", "长度", "字符类型")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        
        # 设置列标题和宽度
        column_widths = [80, 200, 60, 120]
        for i, col in enumerate(columns):
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=column_widths[i], anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 清空历史按钮
        clear_history_btn = ttk.Button(main_frame, text="清空历史", 
                                      command=self.clear_history)
        clear_history_btn.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        
        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        length_frame.columnconfigure(0, weight=1)
        password_frame.columnconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # 绑定双击事件
        self.history_tree.bind("<Double-1>", self.on_history_double_click)
        
        # 初始化历史记录
        self.password_history = []
        
        # 设置最小窗口大小
        self.root.update()
        self.root.minsize(600, 700)
        
    def generate_password(self):
        """生成随机密码"""
        # 检查是否至少选择了一种字符类型
        if not any([self.uppercase_var.get(), self.lowercase_var.get(), 
                   self.numbers_var.get(), self.symbols_var.get()]):
            messagebox.showerror("错误", "请至少选择一种字符类型！")
            return
        
        # 构建字符池
        chars = ""
        if self.uppercase_var.get():
            chars += string.ascii_uppercase
        if self.lowercase_var.get():
            chars += string.ascii_lowercase
        if self.numbers_var.get():
            chars += string.digits
        if self.symbols_var.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # 生成密码
        length = self.length_var.get()
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # 显示密码
        self.password_var.set(password)
        
        # 添加到历史记录
        self.add_to_history(password)
        
    def add_to_history(self, password):
        """添加密码到历史记录"""
        # 获取字符类型描述
        char_types = []
        if self.uppercase_var.get():
            char_types.append("大写")
        if self.lowercase_var.get():
            char_types.append("小写")
        if self.numbers_var.get():
            char_types.append("数字")
        if self.symbols_var.get():
            char_types.append("符号")
        
        char_type_str = ", ".join(char_types)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # 添加到历史记录列表
        self.password_history.append({
            "time": current_time,
            "password": password,
            "length": len(password),
            "char_types": char_type_str
        })
        
        # 更新树形视图
        self.update_history_tree()
        
    def update_history_tree(self):
        """更新历史记录树形视图"""
        # 清空现有项目
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 添加历史记录（最多显示20条）
        for record in self.password_history[-20:]:
            self.history_tree.insert("", "end", values=(
                record["time"],
                record["password"],
                record["length"],
                record["char_types"]
            ))
    
    def copy_password(self):
        """复制密码到剪贴板"""
        password = self.password_var.get()
        if password:
            # 使用tkinter的内置剪贴板功能
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("成功", "密码已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "请先生成密码！")
    
    def clear_history(self):
        """清空历史记录"""
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？"):
            self.password_history.clear()
            self.update_history_tree()
    
    def on_history_double_click(self, event):
        """双击历史记录项时复制密码"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            password = item['values'][1]
            self.password_var.set(password)
            self.copy_password()

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
