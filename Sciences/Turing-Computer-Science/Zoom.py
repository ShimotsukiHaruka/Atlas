import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFont
import os
import platform

class TextMagnifier:
    def __init__(self, root):
        self.root = root
        self.root.title("汉字与英语单词放大显示程序")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # 设置字体
        self.setup_fonts()
        
        # 创建界面
        self.create_widgets()
        
    def setup_fonts(self):
        """设置可用的中文字体"""
        self.available_fonts = []
        
        # 不同系统的字体路径
        font_paths = []
        system = platform.system()
        
        if system == "Windows":
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",  # 黑体
                "C:/Windows/Fonts/simsun.ttc",  # 宋体
                "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
                "C:/Windows/Fonts/simkai.ttf",  # 楷体
            ]
        elif system == "Darwin":  # macOS
            font_paths = [
                "/System/Library/Fonts/PingFang.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc",
            ]
        else:  # Linux
            font_paths = [
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            ]
        
        # 测试字体可用性
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    # 测试字体是否能加载
                    test_font = ImageFont.truetype(font_path, 20)
                    self.available_fonts.append(font_path)
                    print(f"找到可用字体: {font_path}")
                except:
                    continue
        
        # 如果没有找到系统字体，使用PIL的默认字体
        if not self.available_fonts:
            print("未找到系统字体，使用默认字体")
            self.default_font = ImageFont.load_default()
        else:
            self.default_font = None
        
        # 当前字体索引
        self.current_font_index = 0
        self.current_font_size = 100
    
    def get_current_font(self, size):
        """获取当前字体"""
        if self.available_fonts:
            try:
                return ImageFont.truetype(self.available_fonts[self.current_font_index], size)
            except:
                pass
        return ImageFont.load_default()
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(self.root, text="汉字与英语单词放大显示器", 
                              font=("Arial", 18, "bold"), 
                              bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=15)
        
        # 输入区域框架
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10, fill='x', padx=20)
        
        # 输入标签
        input_label = tk.Label(input_frame, text="输入文本:", 
                              font=("Arial", 12), bg='#f0f0f0')
        input_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # 输入框
        self.text_var = tk.StringVar()
        self.text_entry = tk.Entry(input_frame, textvariable=self.text_var, 
                                  font=("Arial", 14), width=50)
        self.text_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.text_entry.bind('<Return>', self.magnify_text)
        
        input_frame.columnconfigure(1, weight=1)
        
        # 控制面板
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=10, fill='x', padx=20)
        
        # 字体大小调整
        size_label = tk.Label(control_frame, text="字体大小:", 
                             font=("Arial", 10), bg='#f0f0f0')
        size_label.grid(row=0, column=0, padx=5, sticky='w')
        
        self.size_var = tk.IntVar(value=self.current_font_size)
        size_scale = tk.Scale(control_frame, from_=50, to=300, 
                             orient=tk.HORIZONTAL,
                             variable=self.size_var,
                             command=self.update_display,
                             length=200, font=("Arial", 8))
        size_scale.grid(row=0, column=1, padx=5, sticky='w')
        
        # 字体选择（如果有多个字体可用）
        if len(self.available_fonts) > 1:
            font_label = tk.Label(control_frame, text="选择字体:", 
                                 font=("Arial", 10), bg='#f0f0f0')
            font_label.grid(row=0, column=2, padx=(20,5), sticky='w')
            
            font_names = [os.path.basename(f) for f in self.available_fonts]
            self.font_var = tk.StringVar(value=font_names[0])
            font_combo = ttk.Combobox(control_frame, textvariable=self.font_var, 
                                     values=font_names, state="readonly",
                                     width=15)
            font_combo.grid(row=0, column=3, padx=5, sticky='w')
            font_combo.bind('<<ComboboxSelected>>', self.change_font)
        
        # 按钮框架
        button_frame = tk.Frame(control_frame, bg='#f0f0f0')
        button_frame.grid(row=0, column=4, padx=(20,0), sticky='e')
        
        # 放大按钮
        magnify_btn = tk.Button(button_frame, text="放大显示", 
                               font=("Arial", 10), 
                               command=self.magnify_text,
                               bg='#4CAF50', fg='white',
                               width=10, height=1)
        magnify_btn.pack(side='left', padx=5)
        
        # 清空按钮
        clear_btn = tk.Button(button_frame, text="清空", 
                             font=("Arial", 10), 
                             command=self.clear_text,
                             bg='#f44336', fg='white',
                             width=8, height=1)
        clear_btn.pack(side='left', padx=5)
        
        control_frame.columnconfigure(4, weight=1)
        
        # 显示区域
        display_frame = tk.Frame(self.root, bg='white', relief='sunken', bd=2)
        display_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        # 创建文本显示标签（直接使用Tkinter的Label，支持大字体）
        self.display_label = tk.Label(display_frame, text="", 
                                     bg='white', fg='black',
                                     font=("Arial", self.current_font_size),
                                     wraplength=800)
        self.display_label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # 状态信息
        self.status_var = tk.StringVar()
        status_label = tk.Label(self.root, textvariable=self.status_var,
                               font=("Arial", 9), bg='#f0f0f0', fg='#666666')
        status_label.pack(pady=5)
        
        # 更新状态信息
        self.update_status()
        
        # 提示文字
        hint_label = tk.Label(self.root, 
                             text="提示：输入汉字或英语单词后点击'放大显示'或按回车键",
                             font=("Arial", 10), bg='#f0f0f0', fg='#666666')
        hint_label.pack(pady=5)
        
        # 示例文本按钮
        example_btn = tk.Button(self.root, text="插入示例文本", 
                               font=("Arial", 9),
                               command=self.insert_example,
                               bg='#2196F3', fg='white')
        example_btn.pack(pady=5)
        
        # 焦点设置在输入框
        self.text_entry.focus()
    
    def update_status(self):
        """更新状态信息"""
        font_count = len(self.available_fonts)
        if font_count > 0:
            current_font = os.path.basename(self.available_fonts[self.current_font_index])
            self.status_var.set(f"找到 {font_count} 种字体 | 当前字体: {current_font} | 字体大小: {self.current_font_size}")
        else:
            self.status_var.set("使用默认字体 | 字体大小: {self.current_font_size}")
    
    def change_font(self, event=None):
        """更改字体"""
        selected_font = self.font_var.get()
        for i, font_path in enumerate(self.available_fonts):
            if os.path.basename(font_path) == selected_font:
                self.current_font_index = i
                break
        self.update_display()
        self.update_status()
    
    def magnify_text(self, event=None):
        """放大显示文本"""
        text = self.text_var.get().strip()
        
        if not text:
            messagebox.showwarning("提示", "请输入要放大的文本")
            return
        
        # 直接使用Tkinter的Label显示大字体文本
        font_size = self.size_var.get()
        self.current_font_size = font_size
        
        # 创建字体（使用系统支持的字体）
        font_spec = ("Arial", font_size)
        
        # 尝试使用中文字体
        if self.available_fonts:
            try:
                # 获取字体名称（不带扩展名）
                font_name = os.path.basename(self.available_fonts[self.current_font_index]).split('.')[0]
                font_spec = (font_name, font_size)
            except:
                pass
        
        # 更新显示
        self.display_label.config(text=text, font=font_spec)
        self.update_status()
    
    def update_display(self, value=None):
        """更新显示（滑块回调）"""
        if self.text_var.get().strip():
            self.magnify_text()
    
    def clear_text(self):
        """清空文本"""
        self.text_var.set("")
        self.display_label.config(text="")
        self.text_entry.focus()
    
    def insert_example(self):
        """插入示例文本"""
        examples = [
            "你好 Hello World!",
            "汉字 Chinese Characters", 
            "放大效果 Magnification",
            "Python 编程 Programming",
            "测试中文显示 Test Chinese Display",
            "这是一个测试 This is a test"
        ]
        import random
        example = random.choice(examples)
        self.text_var.set(example)
        self.magnify_text()
        self.text_entry.focus()

def main():
    # 创建主窗口
    root = tk.Tk()
    
    # 创建应用程序
    app = TextMagnifier(root)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()
