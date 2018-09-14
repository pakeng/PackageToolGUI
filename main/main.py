#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from Tkinter import *
import tkFileDialog as ChooseFileDialog
import tkMessageBox


#  定义Application类
from beans.ConfigBean import Configuration
from engine.engine import PackageTool


class Application(Frame):

    # 创建view
    def create_view(self):
        # 当前源文件名称
        self.file_name_label = Label(self, text="")
        file_name_label = Label(self, text="当前文件:")
        # 源文件选择按钮
        self.file_choose_btn = Button(self, text="选择文件", command=self.choose_file)
        # 渠道名称
        channel_name_label = Label(self, text="渠道名称:")
        self.channel_name_input = Entry(self, text="渠道名称:")
        # umengTAG
        channel_TAG_label = Label(self, text="统计TAG:")
        self.channel_TAG_input = Entry(self, text="请输入TAG:")
        # 测试标识
        debug_level_label = Label(self, text="测试标识:")
        self.debug_level_input = Entry(self)
        debug_level_label_info = Label(self, text="应当输入数值，例如 1， 当大于100的时候是测试包，否者是正式包")
        # 选择输出目录
        output_dir_label = Label(self, text="输出路径:")
        self.output_dir_label = Label(self)
        self.output_dir_btn = Button(self, text="输出路径", command=self.choose_out_dir)

        # 打包view布局
        row_int = 0
        # 文件名称
        file_name_label.grid(row=row_int, column=0, padx=10, pady=10, sticky=E)
        self.file_name_label.grid(row=row_int, column=1, padx=10, pady=10)
        self.file_choose_btn.grid(row=row_int, column=2, sticky=W)
        row_int += 1
        # 渠道名称
        channel_name_label.grid(row=row_int, column=0, padx=10, pady=10, sticky=E)
        self.channel_name_input.grid(row=row_int, column=1, padx=10, pady=10)
        row_int += 1
        # 统计tag
        channel_TAG_label.grid(row=row_int, column=0, padx=10, pady=10, sticky=E)
        self.channel_TAG_input.grid(row=row_int, column=1, padx=10, pady=10)
        row_int += 1
        # 测试标识
        debug_level_label.grid(row=row_int, column=0, padx=10, pady=10, sticky=E)
        self.debug_level_input.grid(row=row_int, column=1, padx=10, pady=10)
        row_int += 1
        debug_level_label_info.grid(row=row_int, column=1, columnspan=2, sticky=W+E+N+S)
        row_int += 1
        # 选择输出目录
        output_dir_label.grid(row=row_int, column=0, padx=10, pady=10, sticky=E)
        self.output_dir_label.grid(row=row_int, column=1, padx=10, pady=10)
        self.output_dir_btn.grid(row=row_int, column=2, sticky=W)
        row_int += 1
        # 打包按钮
        self.re_pack_btn = Button(self, text="开始打包", command=self.re_pack)
        self.re_pack_btn.grid(row=row_int, column=0, columnspan=2, padx=10, pady=20, sticky=W+E+N+S)

    def refresh_configuration(self):

        self.output_dir_label.config(text=self.configuration.out_file_dir)
        self.channel_name_input.insert(0, self.configuration.name)
        self.debug_level_input.insert(0, self.configuration.debug_level)
        self.file_name_label.config(text=self.configuration.src_file_name)
        self.channel_TAG_input.insert(0, self.configuration.u_tag)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.create_view()
        self.configuration = Configuration()
        self.refresh_configuration()
        self.pack()

    # 选择文件按钮方法
    def choose_file(self):
        file_name = ChooseFileDialog.askopenfilename(initialdir="..")
        if file_name != "":
            fn, ext = os.path.splitext(file_name)
            if ext not in ('.apk', '.APK'):
                self.show_err_dialog("请选择正确的APK文件！")
                return
            self.configuration.src_file_name = file_name
            self.configuration.file_name = os.path.basename(file_name)
            self.file_name_label.config(text=file_name)
        else:
            self.file_name_label.config(text="您没有选择任何文件")

    # 选择输出路径按钮方法
    def choose_out_dir(self):
        file_name = ChooseFileDialog.askdirectory()
        if file_name != "":
            self.configuration.out_file_dir = file_name
            self.output_dir_label.config(text=file_name)
        else:
            self.output_dir_label.config(text="您没有选择任何文件夹")

    def re_pack(self):
        print "start repack"
        if self._check_configuration():
            tool = PackageTool(self.configuration)
            tool.test()
        else:
            pass

    def _check_configuration(self):
        if self.configuration.src_file_name == '':
            self.show_err_dialog("请选择源文件！")
            return False
        if self.channel_name_input.get() != '':
            self.configuration.name = self.channel_name_input.get()
        else:
            self.show_err_dialog("请输入渠道名称！")
            return False
        if self.channel_TAG_input.get() != '':
            self.configuration.u_tag = self.channel_TAG_input.get()
        else:
            self.show_err_dialog("请输入统计TAG！")
            return False
        if self.debug_level_input.get() != '':
            self.configuration.debug_level = self.debug_level_input.get()
        else:
            self.show_err_dialog("请输入调试等级！")
            return False
        if self.configuration.out_file_dir == '':
            self.show_err_dialog("请选择输出目录！")
            return False
        print self.configuration
        return True

    @staticmethod
    def show_err_dialog(msg):
        tkMessageBox.showerror("错误信息", "错误信息："+ msg)

# 创建主界面
def make_window():
    root = Tk()
    panel = Frame(root)
    app = Application(panel)
    panel.pack()
    statue_bar = Frame(root)
    statue_label_info = Label(statue_bar, text="当前状态：")
    statue_label = Label(statue_bar, text="----")
    statue_label_info.pack(side=LEFT)
    statue_label.pack(side=RIGHT)
    statue_bar.pack(side=BOTTOM)
    root.title("APK渠道打包工具")
    root.minsize(800, 600)  # 设置窗口大小 最小尺寸
    # root.maxsize(800, 800)  # 设置窗口大小 最大尺寸
    app.mainloop()


if __name__ == '__main__':
    make_window()
