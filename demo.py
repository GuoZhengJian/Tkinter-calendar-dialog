# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 19:37:35 2023

E-mail: 572078547@QQ.COM

哔哩哔哩UP: 键盘侠十指如飞

哔哩哔哩URL: https://space.bilibili.com/9570945
"""

import tkinter as tk

try:
    # 导入日历对话框.
    from Tk_Calendar import TkCalendar
except:
    # 如果导入出错, 将模块的搜索路径添加到sys.path, 然后再重新导入.
    import sys, os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from Tk_Calendar import TkCalendar


class Tk_Demo(tk.Tk):
    """tkinter调用日历对话框演示.
    
    使用方法为:
        使用小部件的bind事件调用日历对话框TkCalendar(), 详见self.Button_bind()函数.    
    """
    def __init__(self):
        super().__init__()
        self.title('Tkinter的日历对话框')                 # 标题
        self.geometry(newGeometry=self.newGeometry())   # 尺寸和位置
        self.attributes('-topmost', True)               # 置顶窗口
        self.init_labelwidget()                         # 初始化label小部件
        
    def newGeometry(self):
        """设置geometry并返回."""
        screenwidth = int(self.winfo_screenwidth())
        screenheight = int(self.winfo_screenheight())
        width = int(screenwidth*0.3)
        height = int(screenheight*0.35)
        rootx = int(screenwidth*0.7/2)
        rooty = int(screenheight*0.65/2)
        newGeometry = f"{width}x{height}+{rootx}+{rooty}"
        return newGeometry
        
    def init_labelwidget(self):
        """初始化一个label小部件."""
        self.label = tk.Label(self, text='点击调用<日历对话框>', background='#3498db')
        self.label.pack(side='top', fill='x', ipady=10)
        self.label.bind('<Button-1>', self.Button_bind)
        
    def Button_bind(self, event):
        """当鼠标左键点击label小部件时开启bind事件.
        
        TkCalendar(master, widget)
            master: 小部件的父容器, 该参数主要用于自定义部件类之间的通信, 如相互传递参数和状态
            widget: 调用的小部件, 日历对话框会将返回的值写入到该widget的text属性中
        """
        TkCalendar(master = self,
                   widget = event.widget
                   )
    

    @classmethod
    def start_mainloop(cls):
        """classmethod."""
        root = cls()
        root.mainloop()
        

if __name__ == '__main__':
    Tk_Demo.start_mainloop()