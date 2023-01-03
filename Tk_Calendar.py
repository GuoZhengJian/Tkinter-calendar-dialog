# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:12:21 2022

E-mail: 572078547@QQ.COM

哔哩哔哩UP: 键盘侠十指如飞

哔哩哔哩URL: https://space.bilibili.com/9570945
"""

import tkinter as tk
import datetime


class ScrollFrame(tk.Frame):
    """滚动框架.

    如果需要将内容滚动, 请将内容放置self.canvas_frame内.
    """

    def __init__(self, master, SharedClassOBJ=None, QueueOBJ=None):
        super().__init__(master)
        self.master = master
        self.config({'bg': '#FFFFFF', 'highlightthickness': 0})
        # self.place(relx=0, rely=0, relheight=1, relwidth=1)  # 设置布局

        # 1)
        self.canvas = tk.Canvas(self)
        self.canvas.config({'bg': '#FFFFFF', 'highlightthickness': 0})    # canvas和canvas_frame均可单独配置
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # 2)
        self.canvas_frame = tk.Frame(self.canvas)
        self.canvas_frame.config({'bg': '#FFFFFF', 'highlightthickness': 0})  # canvas和canvas_frame均可单独配置

        # 3) 画布窗口对象create_window()方法允许放置小组件或框架, 可以稍后使用itemconfigure设置参数选项. (该步骤会显示小组件或框架的布局)
        self.canvas_window_id = self.canvas.create_window(0, 0, anchor='nw')

        # 4)
        self.canvas_scrollbar = tk.Scrollbar(self.canvas)
        self.canvas_scrollbar.config({'elementborderwidth': 0, 'width': 15})
        self.canvas_scrollbar.pack(side='right', fill='y')

        # 5)
        self.canvas.config(yscrollcommand=self.canvas_scrollbar.set)
        self.canvas_scrollbar.config(command=self.canvas.yview)

        # ==========================================================================================
        #         注意所有bind的命名, 请避免与父对象的bind时间命名重复, 如果重复可能会造成意料之外的BUG
        # ==========================================================================================
        # 6)
        self.canvas_frame.bind("<Configure>", self.Canvasbind_task_display_region, add='+')
        self.canvas_frame.bind('<Button-1>', self.Canvasbind_Button_bind, add='+')

        # 7) 鼠标进入当前Canvas时, 触发全局鼠标滚轮事件
        self.canvas.bind('<Enter>', self.Canvasbind_bound_to_mousewheel, add='+')
        self.canvas.bind('<Leave>', self.Canvasbind_unbound_to_mousewheel, add='+')

        # 8)
        self.canvas.bind('<Configure>', self.Canvasbind_up_size, add='+')
        self.canvas.bind('<Button-1>', self.Canvasbind_Button_1, add='+')

        # 9)
        # 如果需要将内容滚动, 请将内容放置self.canvas_frame内

    def Canvasbind_bound_to_mousewheel(self, event):
        """当鼠标进入当前Canvas时, 绑定滚轮bind事件."""
        # 使用bind_all是因为一般情况下Canvas上面都覆盖有其他部件, bind事件是不能直接控制Canvas的
        self.canvas.bind_all("<MouseWheel>", self.task_display_mousewheel)

    def Canvasbind_unbound_to_mousewheel(self, event):
        """当鼠标离开当前Canvas时, 解除滚轮bind事件."""
        self.canvas.unbind_all("<MouseWheel>")
        
    def Canvasbind_Button_bind(self, event):
        """当鼠标按下时开启bind事件."""
        event.widget.focus_set()

    def Canvasbind_task_display_region(self, event):
        """设置画布可以滚动的区域有多大, bbox返回对象的区域参数:(左, 上, 右, 下).

        如果需要 当Frame高度 < Canvas高度时不滚动, 也就是控件未填满Canvas空间时不
        滚动, 那么只需要把滚动区域为Frame当前的高度即可.
        """
        canvas_height = self.canvas.winfo_height()              # Canvas总高度
        canvas_frame_height = self.canvas_frame.winfo_height()  # Frame总高度

        if canvas_height >= canvas_frame_height:
            # Canvas高度 >= Frame的高度, 设置为不可以滚动
            bbox_bottom = canvas_height - canvas_frame_height
        else:
            bbox_bottom = 0

        # left, top, right, bottom = self.canvas.bbox('all')
        left, top, right, bottom = self.canvas.bbox(self.canvas_window_id)
        self.canvas.config(scrollregion=(left, top, right, sum((bottom, bbox_bottom))))

    def task_display_mousewheel(self, event):
        """设置鼠标滚轮每次可以滚动多少画布."""
        scroll_int = 0
        if event.delta > 0:
            scroll_int = -1
        if event.delta < 0:
            scroll_int = 1
        self.canvas.yview('scroll', scroll_int, 'units')

    def Canvasbind_up_size(self, event):
        """窗口尺寸发生变化时, 调用该事件来更改canvas_window_id的选项参数."""
        self.canvas.itemconfigure(self.canvas_window_id,
                                  window=self.canvas_frame,
                                  width=self.winfo_width(),
                                  )

    def Canvasbind_Button_1(self, event):
        """当鼠标点击canvas时聚焦到canvas, 如果不设置canvas是不会聚焦的."""
        self.canvas = event.widget
        self.canvas.focus_set()

class DatetimeFrame(tk.LabelFrame):
    """日期和时间框架."""

    def __init__(self, master, SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.SharedClassOBJ = SharedClassOBJ

        # init class method
        self.start_layout()
        self.put_class()
        self.init_datetimeframe()

        # anchor
        self.DateFrame_viewable = False    # date 选择类是否可见
        self.TimeFrame_viewable = False    # time 选择类是否可见

    def start_layout(self):
        """启动布局."""
        self.config({'background': '#FFFFFF', 'bd': 0, 'height': 1, 'width': 1})
        self.pack(side='top', fill='x', padx=0, pady=0, ipadx=0, ipady=10)

    def put_class(self):
        """put_class"""
        self.SharedClassOBJ.update({'DatetimeFrame': self})

    def init_datetimeframe(self):
        """初始化日期时间框架."""

        # 当前标签的时间,如果当前标签的时间为None (一般指的是结束时间标签)
        TkCalendar = self.SharedClassOBJ.get('TkCalendar')
        widget_text = TkCalendar.widget.cget('text')
        if widget_text[:4] in ['创建时间', '开始时间', '结束时间'] and widget_text[6:] != 'None':
            current_datetime = datetime.datetime.strptime(widget_text[6:], "%Y-%m-%d %H:%M:%S")
        else:
            current_datetime = datetime.datetime.today().replace(microsecond=0)

        self.topwidget_year = tk.Label(self)
        self.topwidget_month = tk.Label(self)
        self.topwidget_hour = tk.Label(self)
        self.topwidget_minute = tk.Label(self)

        self.topwidget_year.config({'width': 1, 'height': 1, 'anchor': 'e', 'text': "%s 年" % current_datetime.year})
        self.topwidget_month.config({'width': 1, 'height': 1, 'anchor': 'w', 'text': "%s 月" % current_datetime.month})
        self.topwidget_hour.config({'width': 1, 'height': 1, 'anchor': 'e', 'text': "%s 时" % current_datetime.hour})
        self.topwidget_minute.config({'width': 1, 'height': 1, 'anchor': 'w',
                                     'text': "%s 分" % current_datetime.minute})

        self.topwidget_year.config({'font': ['normal', 8, 'bold', 'roman'], 'background':'#ffffff'})
        self.topwidget_month.config({'font': ['normal', 8, 'bold', 'roman'], 'background':'#ffffff'})
        self.topwidget_hour.config({'font': ['normal', 8, 'bold', 'roman'], 'background':'#ffffff'})
        self.topwidget_minute.config({'font': ['normal', 8, 'bold', 'roman'], 'background':'#ffffff'})

        self.topwidget_year.pack(side='left', fill='both', expand=True)
        self.topwidget_month.pack(side='left', fill='both', expand=True)
        self.topwidget_hour.pack(side='left', fill='both', expand=True)
        self.topwidget_minute.pack(side='left', fill='both', expand=True)

        # 鼠标进入时的样式
        self.topwidget_year.bind('<Enter>', self.Enter_bind, add='+')
        self.topwidget_month.bind('<Enter>', self.Enter_bind, add='+')
        self.topwidget_hour.bind('<Enter>', self.Enter_bind, add='+')
        self.topwidget_minute.bind('<Enter>', self.Enter_bind, add='+')

        # 鼠标离开时的样式
        self.topwidget_year.bind('<Leave>', self.Leave_bind, add='+')
        self.topwidget_month.bind('<Leave>', self.Leave_bind, add='+')
        self.topwidget_hour.bind('<Leave>', self.Leave_bind, add='+')
        self.topwidget_minute.bind('<Leave>', self.Leave_bind, add='+')

        # 鼠标左键点击时调用的功能
        self.topwidget_year.bind('<Button-1>', self.Button_1_bind, add='+')
        self.topwidget_month.bind('<Button-1>', self.Button_1_bind, add='+')
        self.topwidget_hour.bind('<Button-1>', self.Button_1_bind, add='+')
        self.topwidget_minute.bind('<Button-1>', self.Button_1_bind, add='+')

    def Enter_bind(self, event):
        """当鼠标进入控件上方时触发."""
        widget_text = event.widget.cget('text')[-1]
        if widget_text == '年' or widget_text == '月':
            self.topwidget_year.config({'background': '#a4b0be'})
            self.topwidget_month.config({'background': '#a4b0be'})

        if widget_text == '时' or widget_text == '分':
            self.topwidget_hour.config({'background': '#a4b0be'})
            self.topwidget_minute.config({'background': '#a4b0be'})

    def Leave_bind(self, event):
        """当鼠标离开控件上方时触发."""
        widget_text = event.widget.cget('text')[-1]
        if widget_text == '年' or widget_text == '月':
            self.topwidget_year.config({'background': '#ffffff'})
            self.topwidget_month.config({'background': '#ffffff'})

        if widget_text == '时' or widget_text == '分':
            self.topwidget_hour.config({'background': '#ffffff'})
            self.topwidget_minute.config({'background': '#ffffff'})

    def Button_1_bind(self, event):
        """鼠标左键点击时调用的功能."""
        event.widget.focus_set()
        
        # 隐藏以下对象: WeekFrame, CalendarFrame, ConfirmFrame
        WeekFrame = self.SharedClassOBJ.get('WeekFrame')
        CalendarFrame = self.SharedClassOBJ.get('CalendarFrame')
        ConfirmFrame = self.SharedClassOBJ.get('ConfirmFrame')
        WeekFrame.pack_forget()
        CalendarFrame.pack_forget()
        ConfirmFrame.pack_forget()

        # 执行日期框架或时间框架
        widget_text = event.widget.cget('text')[-1]
        if widget_text == '年' or widget_text == '月':
            current_year = self.topwidget_year.cget('text')[:-2]
            current_month = self.topwidget_month.cget('text')[:-2]
            current_date = datetime.date(int(current_year), int(current_month), 1)

            # 实例化date框架 (如果未实例化DateFrame, 则调用下述代码)
            if not self.DateFrame_viewable:
                TkCalendar = self.SharedClassOBJ.get('TkCalendar')
                DateFrame(TkCalendar, current_date, self.SharedClassOBJ)
                self.DateFrame_viewable = True

        if widget_text == '时' or widget_text == '分':
            current_hour = self.topwidget_hour.cget('text')[:-2]
            current_minute = self.topwidget_minute.cget('text')[:-2]
            current_time = datetime.time(int(current_hour), int(current_minute))

            # 实例化date框架 (如果未实例化DateFrame, 则调用下述代码)
            if not self.TimeFrame_viewable:
                TkCalendar = self.SharedClassOBJ.get('TkCalendar')
                TimeFrame(TkCalendar, current_time, 'hour', self.SharedClassOBJ)
                TimeFrame(TkCalendar, current_time, 'minute', self.SharedClassOBJ)
                self.TimeFrame_viewable = True


class WeekFrame(tk.LabelFrame):
    """周框架."""

    def __init__(self, master, SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.SharedClassOBJ = SharedClassOBJ

        # init class method
        self.start_layout()
        self.put_class()
        self.init_weekframe()

    def start_layout(self):
        """启动布局."""
        self.config({'background': '#34495e', 'bd': 0})
        self.config({'height': 1, 'width': 1})
        self.pack(side='top', fill='x', padx=0, pady=1, ipadx=0, ipady=5)

    def put_class(self):
        """put_class"""
        self.SharedClassOBJ.update({'WeekFrame': self})

    def init_weekframe(self):
        """初始化周框架."""
        weeklist = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        for week in range(7):
            week_label = tk.Label(self, text=weeklist[week])
            week_label.config({'width': 1, 'height': 1})
            week_label.pack(side='left', fill='both', expand=True, padx=0)


class CalendarFrame(ScrollFrame):
    """日历框架."""

    def __init__(self, master, SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.SharedClassOBJ = SharedClassOBJ

        # init class attribute
        self.current_day = None
        self.return_datetime = None

        # 更改基类属性
        self.canvas.config()
        self.canvas_frame.config()
        self.canvas_scrollbar.config({'width': 10})
        self.canvas_scrollbar.pack_forget()
        self.pack(side='top', fill='both', expand=True, padx=0, pady=0, ipadx=0, ipady=0)

        # bind
        self.canvas.bind('<Enter>', self.bound_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbound_to_mousewheel)

        # init class method
        self.put_class()
        self.date_anchor()
        self.init_calendarframe(self.today)

    def put_class(self):
        """put_class"""
        self.SharedClassOBJ.update({'CalendarFrame': self})

    def date_anchor(self):
        """日期锚点."""
        self.lastday = None
        self.today = datetime.date.today()
        self.nextday = None

    def init_calendarframe(self, date=None):
        """初始化日历小部件, 小部件尺寸为6x7."""
        start_day = 0
        end_day = 0

        for num in range(6):
            end_day += 7
            self.create_datelabelframe(date, start_day, end_day)
            start_day = end_day

    def create_datelabelframe(self, date, start_day, end_day):
        """该类负责创建显示到滚动画布中的日期."""
        tomonth_start, tostart_labelordinal = self.tomonth_date(date)

        start_ordinal = tostart_labelordinal + start_day
        end_ordinal = tostart_labelordinal + end_day
        ordinal_list = [ordinal for ordinal in range(start_ordinal, end_ordinal)]
        Calendar_LabelFrame(master=self.canvas_frame,
                            current_month=tomonth_start,
                            tablecontent=ordinal_list,
                            SharedClassOBJ=self.SharedClassOBJ
                            )

    def bound_to_mousewheel(self, event):
        """当鼠标进入当前Canvas时, 绑定滚轮bind事件."""
        # 使用bind_all是因为一般情况下Canvas上面都覆盖有其他部件, bind事件是不能直接控制Canvas的
        self.canvas.bind_all("<MouseWheel>", self.add_datelabelframe)

    def unbound_to_mousewheel(self, event):
        """当鼠标离开当前Canvas时, 解除滚轮bind事件."""
        self.canvas.unbind_all("<MouseWheel>")

    def add_datelabelframe(self, event):
        """当画布滚动时, 添加日期框架."""
        # 删除所有子部件
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        # 滚轮向上滚动, 意为减少日期
        if event.delta > 0:
            self.lastday = self.upmonth_date(self.today)[0]
            self.init_calendarframe(self.lastday)
            self.today = self.lastday

        # 滚轮向下滚动, 意为增加日期(如果当前日历显示了6个周, 那么开始和结束也要加上6周的天数)
        if event.delta < 0:
            self.nextday = self.dnmonth_date(self.today)[0]
            self.init_calendarframe(self.nextday)
            self.today = self.nextday

        DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
        DatetimeFrame.topwidget_year.config({'text': "%s 年" % self.today.year})
        DatetimeFrame.topwidget_month.config({'text': "%s 月" % self.today.month})

    def tomonth_date(self, date=None):
        """相对于当前日期date, 本月整月的日期."""
        tomonth_start = datetime.date(date.year, date.month, 1)                            # 月初1号
        tostart_labelordinal = tomonth_start.toordinal() - tomonth_start.isoweekday() + 1  # 当前月第一个标签日期的格列高利历序号
        return (tomonth_start, tostart_labelordinal)

    def upmonth_date(self, date=None):
        """相对于当前日期date, 上月整月的日期."""
        tomonth_start = datetime.date(date.year, date.month, 1)                            # 月初1号
        lastmonth = datetime.date.fromordinal(tomonth_start.toordinal() - 1)                 # 上月月末
        lastmonth_start = datetime.date(lastmonth.year, lastmonth.month, 1)                      # 上月第一天
        laststart_labelordinal = lastmonth_start.toordinal() - lastmonth_start.isoweekday() + 1  # 上月第一个标签日期的格列高利历序号
        return (lastmonth_start, laststart_labelordinal)

    def dnmonth_date(self, date=None):
        """相对于当前日期date, 次月整月的日期."""
        tomonth_start = datetime.date(date.year, date.month, 1)                            # 月初1号
        nextmonth = datetime.date.fromordinal(tomonth_start.toordinal() + 31)                # 次月的某一天
        nextmonth_start = datetime.date(nextmonth.year, nextmonth.month, 1)                      # 次月第一天
        nextstart_labelordinal = nextmonth_start.toordinal() - nextmonth_start.isoweekday() + 1  # 次月第一个标签日期的格列高利历序号
        return (nextmonth_start, nextstart_labelordinal)


class ConfirmFrame(tk.LabelFrame):
    """用户确认框架."""

    def __init__(self, master, SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.SharedClassOBJ = SharedClassOBJ

        # init class method
        self.start_layout()
        self.put_class()
        self.init_confirmframe()

    def start_layout(self):
        """启动布局."""
        self.config({'background': '#34495e', 'bd': 0})
        self.config({'height': 1, 'width': 1})
        self.pack(side='top', fill='x', padx=0, pady=1, ipadx=0, ipady=5)

    def put_class(self):
        """put_class"""
        self.SharedClassOBJ.update({'ConfirmFrame': self})

    def init_confirmframe(self):
        """初始化用户确认框架."""
        for text in ['取消', '确认']:
            self.label = tk.Label(self, text=text)
            self.label.config({'width': 1, 'height': 1, 'background': '#FFFFFF'})
            self.label.pack(side='left', fill='both', expand=True, padx=0)

            self.label.bind('<Enter>', self.Enter_bind, add='+')      # 鼠标或按键飘过时的样式;
            self.label.bind('<Leave>', self.Leave_bind, add='+')      # 鼠标或按键飘过时的样式;
            self.label.bind('<Button-1>', self.Button_1_bind, add='+')  # 鼠标或按键按下和释放时的样式;

    def Enter_bind(self, event):
        """鼠标飘过的事件."""
        if event.widget.cget('text') == '取消':
            event.widget.config({'background': '#e67e22'})
        if event.widget.cget('text') == '确认':
            event.widget.config({'background': '#1abc9c'})

    def Leave_bind(self, event):
        """鼠标离开的事件."""
        event.widget.config({'background': '#ffffff'})

    def Button_1_bind(self, event):
        """鼠标按下的事件."""
        widget_text = event.widget.cget('text')
        CalendarFrame = self.SharedClassOBJ.get('CalendarFrame')

        if widget_text == "取消":
            # CalendarFrame.return_datetime = datetime.datetime.today().replace(microsecond=0)
            # 取消上述功能: 点击取消返回当前时间 today
            pass

        if widget_text == "确认":
            DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
            current_hour = DatetimeFrame.topwidget_hour.cget('text')[:-2]
            current_minut = DatetimeFrame.topwidget_minute.cget('text')[:-2]
            
            if not CalendarFrame.current_day:
                # 如果未选择日期, 未选择时间 - 返回当前日期 + 当前时间
                # 如果未选择日期, 选择了时间 - 返回当前日期 + 选择的时间
                # 如果选择了日期, 选择了时间 - 返回选择的日期和时间
                current_date = datetime.date.today()
                CalendarFrame.return_datetime = datetime.datetime(int(current_date.year),
                                                                  int(current_date.month),
                                                                  int(current_date.day),
                                                                  int(current_hour),
                                                                  int(current_minut),
                                                                  )
            else:
                current_year = DatetimeFrame.topwidget_year.cget('text')[:-2]
                current_month = DatetimeFrame.topwidget_month.cget('text')[:-2]
                current_day = CalendarFrame.current_day
                get_datetime = datetime.datetime(int(current_year),
                                                 int(current_month),
                                                 int(current_day),
                                                 int(current_hour),
                                                 int(current_minut),
                                                 )
                CalendarFrame.return_datetime = get_datetime
                CalendarFrame.current_day = None  # 将 self.current_day 恢复默认值None

        # 当选择取消或确认后, calendar就会关闭并销毁, 这会影响 TkCalendar.master.anchor_calendar_show "或门"的逻辑
        # 所以这里将anchor_calendar_show的值更改为True, 目的是为了修正"或门"的逻辑
        Calendar_master = self.SharedClassOBJ.get('Calendar_master')
        Calendar_master.anchor_calendar_show = True

        # 激活FocusOut事件让其销毁
        TkCalendar = self.SharedClassOBJ.get('TkCalendar')
        TkCalendar.event_generate('<FocusOut>')


class Calendar_LabelFrame(tk.LabelFrame):
    """日历框架的标签框架, 将数据库内的所有表格做成标签框架, 并保存至容器内, 以供 时间分类布局类 使用."""

    def __init__(self, master=None, current_month=None, tablecontent=None, SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.current_month = current_month
        self.tablecontent = tablecontent
        self.SharedClassOBJ = SharedClassOBJ

        # init class method
        self.start_layout()
        self.create_label()

    def start_layout(self):
        """启动布局."""
        self.config({'borderwidth': 0, 'background': '#FFFFFF'})
        self.config({'height': 1, 'width': 1})
        self.pack(side='top', fill='x', padx=0, pady=0, ipadx=0, ipady=0)

    def create_label(self):
        """创建Label."""
        if isinstance(self.tablecontent, list):
            for ordinal in self.tablecontent:
                current_date = datetime.date.fromordinal(ordinal)
                self.label = tk.Label(self, text=current_date.day)
                self.label.config({'width': 1, 'height': 1, 'background': '#FFFFFF', 'activebackground':  '#1abc9c'})
                self.label.pack(side='left', fill='both', expand=True, pady=1, padx=1, ipadx=10, ipady=10)

                # bind事件
                self.label.bind('<Enter>', self.Enter_bind, add='+')         # 鼠标或按键飘过时的样式;
                self.label.bind('<Leave>', self.Leave_bind, add='+')         # 鼠标或按键飘过时的样式;
                self.label.bind('<Button-1>', self.Button_1_bind, add='+')   # 鼠标或按键按下和释放时的样式;
                self.label.bind('<Double-Button-1>', self.Double_Button_1_bind, add='+')   # 鼠标双击时的样式;
                self.label.bind('<FocusIn>', self.FocusIn_bind, add='+')     # 组件获得和失去焦点时的样式;
                self.label.bind('<FocusOut>', self.FocusOut_bind, add='+')   # 组件获得和失去焦点时的样式;

                # 本月所有天的样式
                if self.current_month.month == current_date.month:
                    self.label.config({'background': '#FFFFFF', 'fg': '#000000', 'font': ['幼圆', 10, 'bold', 'roman']})
                else:
                    self.label.config({'foreground': '#a4b0be'})

    def Enter_bind(self, event):
        """鼠标进入组件时触发."""
        event.widget.config({'background': '#ecf0f1'})

    def Leave_bind(self, event):
        """鼠标离开组件时触发."""
        event.widget.config({'background': '#FFFFFF'})

    def Button_1_bind(self, event):
        """鼠标按下时触发."""
        event.widget.focus_set()

        CalendarFrame = self.SharedClassOBJ.get('CalendarFrame')
        CalendarFrame.current_day = event.widget.cget('text')

    def FocusIn_bind(self, event):
        """组件获得焦点时触发."""
        event.widget.config({'state': 'active'})

    def FocusOut_bind(self, event):
        """组件失去焦点时触发."""
        event.widget.config({'state': 'normal'})

    def Double_Button_1_bind(self, event):
        """鼠标双击时的事件."""
        DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')

        current_year = DatetimeFrame.topwidget_year.cget('text')[:-2]
        current_month = DatetimeFrame.topwidget_month.cget('text')[:-2]
        current_day = event.widget.cget('text')
        current_hour = DatetimeFrame.topwidget_hour.cget('text')[:-2]
        current_minut = DatetimeFrame.topwidget_minute.cget('text')[:-2]
        get_datetime = datetime.datetime(int(current_year),
                                         int(current_month),
                                         int(current_day),
                                         int(current_hour),
                                         int(current_minut),
                                         )

        # 将日期赋值给 CalendarFrame.return_datetime 属性, 以便其他对象调用.
        CalendarFrame = self.SharedClassOBJ.get('CalendarFrame')
        CalendarFrame.return_datetime = get_datetime

        # 当双击日期后, calendar就会关闭并销毁, 这会影响 TkCalendar.master.anchor_calendar_show "或门"的逻辑
        # 所以这里将anchor_calendar_show的值更改为True, 目的是为了修正"或门"的逻辑
        Calendar_master = self.SharedClassOBJ.get('Calendar_master')
        Calendar_master.anchor_calendar_show = True

        # 激活FocusOut事件让其销毁
        TkCalendar = self.SharedClassOBJ.get('TkCalendar')
        TkCalendar.event_generate('<FocusOut>')


class DateFrame(ScrollFrame):
    """当点击日期时, 跳转到日期框架."""

    def __init__(self, master, current_date, SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.current_date = current_date
        self.SharedClassOBJ = SharedClassOBJ

        # 更改基类属性
        self.canvas.config()
        self.canvas_frame.config()
        self.canvas_scrollbar.config({'width': 10})
        self.canvas_scrollbar.pack_forget()
        self.pack(side='top', fill='both', expand=True, padx=0, pady=1, ipadx=0, ipady=0)

        # bind
        self.canvas.bind('<Enter>', self.bound_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbound_to_mousewheel)

        # init class method
        self.destroy_otherframe()
        self.put_class()
        self.date_anchor()
        self.init_calendarframe(self.current_year)

    def put_class(self):
        """put_class"""
        self.SharedClassOBJ.update({'DateFrame': self})
        
    def destroy_otherframe(self):
        """销毁其他frame."""
        # 以下几个对象如果正在显示的话同样隐藏掉
        TimeFrame_hour_obj = self.SharedClassOBJ.get('TimeFrame_hour')
        TimeFrame_minute_obj = self.SharedClassOBJ.get('TimeFrame_minute')
        if TimeFrame_minute_obj and TimeFrame_hour_obj:
            TimeFrame_hour_obj.destroy()
            TimeFrame_minute_obj.destroy()
            
            DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
            DatetimeFrame.TimeFrame_viewable = False

    def date_anchor(self):
        """日期锚点."""
        self.current_year = self.current_date.year

    def init_calendarframe(self, year):
        """初始化日期小部件, 小部件尺寸为5x4."""
        current_year = year                    # 当前标签的年
        start_month = 1                        # 开始月份的锚点
        end_month = 1                          # 结束月份的锚点

        for num in range(6):
            end_month += 4
            self.create_datelabelframe(current_year, start_month, end_month)
            start_month = end_month

            if start_month > 12 or end_month > 12:
                start_month = 1
                end_month = 1
                current_year += 1

    def create_datelabelframe(self, current_year, start_month, end_month):
        """该类负责创建显示到滚动画布中的日期."""
        ordinal_list = []
        for month in range(start_month, end_month):
            ordinal = datetime.date.toordinal(datetime.date(current_year, month, 1))
            ordinal_list.append(ordinal)

        DateFrame_Label(master=self.canvas_frame,
                        current_year=self.current_date,
                        tablecontent=ordinal_list,
                        SharedClassOBJ=self.SharedClassOBJ,
                        )

    def bound_to_mousewheel(self, event):
        """当鼠标进入当前Canvas时, 绑定滚轮bind事件."""
        # 使用bind_all是因为一般情况下Canvas上面都覆盖有其他部件, bind事件是不能直接控制Canvas的
        self.canvas.bind_all("<MouseWheel>", self.add_datelabelframe)

    def unbound_to_mousewheel(self, event):
        """当鼠标离开当前Canvas时, 解除滚轮bind事件."""
        self.canvas.unbind_all("<MouseWheel>")

    def add_datelabelframe(self, event):
        """当画布滚动时, 添加日期框架."""
        # 删除所有子部件
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        # 滚轮向上滚动, 意为减少日期
        if event.delta > 0:
            self.current_year -= 1
            self.init_calendarframe(self.current_year)

        # 滚轮向下滚动, 意为增加日期(如果当前日历显示了6个周, 那么开始和结束也要加上6周的天数)
        if event.delta < 0:
            self.current_year += 1
            self.init_calendarframe(self.current_year)


class DateFrame_Label(tk.LabelFrame):
    """当点击日期时, 跳转到时间-年月框架."""

    def __init__(self, master=None, current_year=None, tablecontent=None, SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.current_year = current_year
        self.tablecontent = tablecontent
        self.SharedClassOBJ = SharedClassOBJ

        # init class method
        self.start_layout()
        self.create_label()

    def start_layout(self):
        """启动布局."""
        self.config({'borderwidth': 0, 'background': '#FFFFFF'})
        self.pack(side='top', fill='both', expand=True, padx=0, pady=0, ipadx=0, ipady=0)

    def create_label(self):
        """创建Label."""
        if isinstance(self.tablecontent, list):
            for ordinal in self.tablecontent:
                current_date = datetime.date.fromordinal(ordinal)
                self.label = tk.Label(self, text=f'{current_date.year}.{current_date.month}')
                self.label.config({'width': 1, 'height': 1, 'background': '#FFFFFF', 'activebackground':  '#1abc9c'})
                self.label.pack(side='left', fill='both', expand=True, pady=1, padx=1, ipadx=10, ipady=10)

                # bind事件
                self.label.bind('<Enter>', self.Enter_bind, add='+')         # 鼠标或按键飘过时的样式;
                self.label.bind('<Leave>', self.Leave_bind, add='+')         # 鼠标或按键飘过时的样式;
                self.label.bind('<Button-1>', self.Button_1_bind, add='+')   # 鼠标或按键按下和释放时的样式;

                # 今年所有月的样式
                if self.current_year.year == current_date.year:
                    self.label.config({'background': '#FFFFFF', 'fg': '#000000', 'font': ['幼圆', 10, 'bold', 'roman']})
                else:
                    self.label.config({'foreground': '#a4b0be'})

    def Enter_bind(self, event):
        """鼠标进入组件时触发."""
        event.widget.config({'background': '#ecf0f1'})

        # 更新日期标签的值
        widget_text = event.widget.cget('text').split('.')
        DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
        DatetimeFrame.topwidget_year.config({'text': "%s 年" % widget_text[0]})
        DatetimeFrame.topwidget_month.config({'text': "%s 月" % widget_text[1]})

    def Leave_bind(self, event):
        """鼠标离开组件时触发."""
        event.widget.config({'background': '#FFFFFF'})

    def Button_1_bind(self, event):
        """鼠标按下时触发."""
        event.widget.focus_set()

        # 销毁DateFrame
        DateFrame = self.SharedClassOBJ.get('DateFrame')
        DateFrame.destroy()

        # 重新显示以下对象: WeekFrame, CalendarFrame, ConfirmFrame
        WeekFrame = self.SharedClassOBJ.get('WeekFrame')
        CalendarFrame = self.SharedClassOBJ.get('CalendarFrame')
        ConfirmFrame = self.SharedClassOBJ.get('ConfirmFrame')
        WeekFrame.pack(side='top', fill='x', padx=0, pady=1, ipadx=0, ipady=5)
        CalendarFrame.pack(side='top', fill='both', expand=True, padx=0, pady=0, ipadx=0, ipady=0)
        ConfirmFrame.pack(side='top', fill='x', padx=0, pady=1, ipadx=0, ipady=5)

        # 将anchor锚点设为: 未见
        DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
        DatetimeFrame.DateFrame_viewable = False


class TimeFrame(ScrollFrame):
    """当点击时间时, 跳转到时间-小时框架."""

    def __init__(self, master, current_time, model='hour', SharedClassOBJ=None):
        super().__init__(master)
        self.master = master
        self.current_time = current_time
        self.model = model
        self.SharedClassOBJ = SharedClassOBJ

        # init class args
        if self.model == 'hour':
            self.time = 24
        if self.model == 'minute':
            self.time = 60

        # 更改基类属性
        self.canvas.config()
        self.canvas_frame.config({'background': '#34495e'})
        self.canvas_scrollbar.config({'width': 10})
        self.canvas_scrollbar.pack_forget()
        self.pack(side='left', fill='both', expand=True, padx=0, pady=1, ipadx=0, ipady=0)

        # bind
        self.canvas.bind('<Enter>', self.bound_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbound_to_mousewheel)

        # init class method
        self.destroy_otherframe()
        self.put_class()
        self.date_anchor()
        self.init_calendarframe(self.current_hour_or_minute) 
        
    def destroy_otherframe(self):
        """销毁其他frame."""
        # 以下几个对象如果正在显示的话同样隐藏掉
        DateFrame = self.SharedClassOBJ.get('DateFrame')
        if DateFrame:
            DateFrame.destroy()
            DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
            DatetimeFrame.DateFrame_viewable = False

    def put_class(self):
        """put_class"""
        if self.model == 'hour':
            self.SharedClassOBJ.update({'TimeFrame_hour': self})
        if self.model == 'minute':
            self.SharedClassOBJ.update({'TimeFrame_minute': self})

    def date_anchor(self):
        """时间锚点."""
        if self.model == 'hour':
            self.current_hour_or_minute = self.current_time.hour
            self.time_list = [i for i in range(0, 24)]
            
        if self.model == 'minute':
            self.current_hour_or_minute = self.current_time.minute
            self.time_list = [i for i in range(0, 60)]

    def init_calendarframe(self, current_time):
        """初始化小时的小部件."""
        # 将小时往前推3个时间单位, 这样可以使当前时间居中
        if current_time >= 3:
            current_time -= 3
        else:
            current_time = self.time-(3-current_time)

        # 生成一个拥有7小时的时间序列列表 或 生成一个有用60分钟的时间序列列表
        if self.time-current_time >= 7:
            current_timelist = self.time_list[current_time: current_time+7]
        else:
            current_timelist = self.time_list[current_time: self.time] + self.time_list[: 7-(self.time-current_time)]

        # 将时间序列列表迭代成label标签
        for h in current_timelist:
            self.label = tk.Label(self.canvas_frame)
            self.label.pack(side='top', fill='both', expand=True, padx=0, pady=0, ipadx=0, ipady=10)
            self.label.config({'text': h, 'background': '#ffffff'})
            self.label.bind('<Button-1>', self.Button_1_bind, add='+')

            if current_timelist.index(h) == 3:
                # 将第三个label变色并将值更新至顶部时间标签
                self.label.config({'background': '#bdc3c7'})
                # 将值更新至顶部时间标签
                DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
                if self.model == 'hour':
                    DatetimeFrame.topwidget_hour.config({'text': "%s 时" % self.label.cget("text")})
                if self.model == 'minute':
                    DatetimeFrame.topwidget_minute.config({'text': "%s 分" % self.label.cget("text")})
            else:
                # 鼠标或按键飘过时的样式;
                self.label.bind('<Enter>', lambda event: event.widget.config({'background': '#ecf0f1'}), add='+')
                self.label.bind('<Leave>', lambda event: event.widget.config({'background': '#ffffff'}), add='+')

    def Button_1_bind(self, event):
        """Button_1_bind."""
        
        # 将值更新至顶部时间标签
        DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
        if self.model == 'hour':
            DatetimeFrame.topwidget_hour.config({'text': "%s 时" % event.widget.cget("text")})
        if self.model == 'minute':
            DatetimeFrame.topwidget_minute.config({'text': "%s 分" % event.widget.cget("text")})
            
        # 销毁两个TimeFrame (记得销毁的部件要放倒最后, 请避免在调用前销毁)
        TimeFrame_minute = self.SharedClassOBJ.get('TimeFrame_minute')
        TimeFrame_hour = self.SharedClassOBJ.get('TimeFrame_hour')
        TimeFrame_minute.destroy()
        TimeFrame_hour.destroy()       

        # 重新显示以下对象: WeekFrame, CalendarFrame, ConfirmFrame
        WeekFrame = self.SharedClassOBJ.get('WeekFrame')
        CalendarFrame = self.SharedClassOBJ.get('CalendarFrame')
        ConfirmFrame = self.SharedClassOBJ.get('ConfirmFrame')
        WeekFrame.pack(side='top', fill='x', padx=0, pady=1, ipadx=0, ipady=5)
        CalendarFrame.pack(side='top', fill='both', expand=True, padx=0, pady=0, ipadx=0, ipady=0)
        ConfirmFrame.pack(side='top', fill='x', padx=0, pady=1, ipadx=0, ipady=5)

        # 将anchor锚点设为: 未见
        DatetimeFrame = self.SharedClassOBJ.get('DatetimeFrame')
        DatetimeFrame.TimeFrame_viewable = False        

    def bound_to_mousewheel(self, event):
        """当鼠标进入当前Canvas时, 绑定滚轮bind事件."""
        # 使用bind_all是因为一般情况下Canvas上面都覆盖有其他部件, bind事件是不能直接控制Canvas的
        self.canvas.bind_all("<MouseWheel>", self.add_datelabelframe)

    def unbound_to_mousewheel(self, event):
        """当鼠标离开当前Canvas时, 解除滚轮bind事件."""
        self.canvas.unbind_all("<MouseWheel>")

    def add_datelabelframe(self, event):
        """当画布滚动时, 添加日期框架."""
        # 删除所有子部件
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        # 滚轮向上滚动, 意为减少日期
        if event.delta > 0:
            self.current_hour_or_minute -= 1
            if self.current_hour_or_minute < 0:
                self.current_hour_or_minute = self.time-1
            self.init_calendarframe(self.current_hour_or_minute)

        # 滚轮向下滚动, 意为增加日期
        if event.delta < 0:
            self.current_hour_or_minute += 1
            if self.current_hour_or_minute > self.time-1:
                self.current_hour_or_minute = 0
            self.init_calendarframe(self.current_hour_or_minute)


class TkCalendar(tk.Toplevel):
    """日期时间选择对话框的顶层窗口."""

    def __init__(self, master, widget):
        super().__init__(master)
        self.master = master
        self.widget = widget
        self.SharedClassOBJ = {'TkCalendar': self, 'Calendar_master': self.master}

        # init class args
        # self.config({'background': '#9b59b6', 'borderwidth': 2})
        self.config({'background': '#95a5a6', 'borderwidth': 2})
        master_height = self.widget.winfo_height()
        master_width = self.widget.winfo_width()
        master_rootx = self.widget.winfo_rootx()
        master_rooty = self.widget.winfo_rooty()
        self.newGeometry = "%sx%s+%s+%s" % (master_width-8, 355, master_rootx+4, master_rooty+master_height+4)

        # toplevel 的属性
        self.title('TkCalendar')                      # 标题
        self.overrideredirect(True)                   # 是否隐藏窗口标题栏
        self.geometry(newGeometry=self.newGeometry)   # 尺寸和位置
        self.attributes('-transparentcolor', None)    # 将顶层窗口以及所有子控件的指定颜色(包括背景色和前景色)变为完全透明, 且透明部分鼠标可以穿透
        self.attributes('-disabled', False)           # 禁用窗口, bool
        self.attributes('-fullscreen', False)         # 全屏窗口, bool
        self.attributes('-toolwindow', False)         # 工具窗口, bool
        self.attributes('-topmost', True)             # 置顶窗口, bool
        self.resizable(height=False, width=False)     # 是否允许更改宽高尺寸
        self.maxsize()                                # 窗口最大尺寸
        self.aspect()                                 # 设置窗口的宽高比
        self.focus_set()                              # 聚焦
        
        # init class method
        self.init_widget()

        # bind
        self.bind('<Destroy>', self.Destroy_bind, add='+')
        self.bind('<FocusOut>', self.FocusOut_bind, add='+')
        self.bind('<Map>', self.Map_bind, add='+')

    def init_widget(self):
        """实例化子部件对象."""        
        DatetimeFrame(self, self.SharedClassOBJ)
        WeekFrame(self, self.SharedClassOBJ)
        CalendarFrame(self, self.SharedClassOBJ)
        ConfirmFrame(self, self.SharedClassOBJ)

    def Update_alpha(self):
        """更新主窗口透明度, 目的是为了缓解视觉卡顿."""
        # (init初始化时设置'-alpha'参数<1.0 会出现软件不会跟随屏幕切换, 但是在Map事件内设置不会出现该BUG)
        if self.alpha_value <= 1.0:
            self.attributes('-alpha', self.alpha_value)
            self.alpha_value += 0.1
            self.after(10, self.Update_alpha)
            
    def Map_bind(self, event):
        """渐变可见, 缓解实例化造成的视觉卡顿."""
        if event.widget is event.widget.winfo_toplevel():
            self.alpha_value = 0.0
            self.Update_alpha()

    def FocusOut_bind(self, event):
        """FocusOut_bind."""
        if event.widget is event.widget.winfo_toplevel():
            event.widget.destroy()

    def Destroy_bind(self, event):
        """Destroy_bind."""
        if event.widget is event.widget.winfo_toplevel():
            CalendarFrame = self.SharedClassOBJ.get('CalendarFrame')
            widget_datetime = CalendarFrame.return_datetime
            self.widget.config({'text': widget_datetime})
            pass


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(newGeometry="566x355+966+0")

    def Button_bind(event):
        TkCalendar(root, event.widget)

    label = tk.Label(root, text='点击调用', background='#b39ddb')
    label.pack(side='top', fill='x', ipady=10)
    label.bind('<Button-1>', Button_bind)

    root.mainloop()


