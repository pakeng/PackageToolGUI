#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import subprocess
import time
from threading import Thread
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import EngineConfig
from beans import ConfigBean


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


# 工具基础
class PackageTool(object):

    def __init__(self, channel_config):
        self._init_config()
        self._file_path = channel_config.src_file_name
        self._package_name = channel_config.package_name
        self._channel_name = channel_config.name
        self._sub_channel_name = channel_config.name
        self._u_meng_tag = channel_config.u_tag
        self._debug_level = channel_config.debug_level
        self._lebian_clientChId = channel_config.name
        self.output_dir = channel_config.out_file_dir

    def start(self):
        self._copy_files()
        self._fix_file()
        self._compile()

    @async
    def decompile(self):
        cmd_str = EngineConfig.cmd_decompile_str % (os.path.join(self._base_dir, EngineConfig.temp_ori_decompile_dir),
                                                    self._file_path)
        print os.popen(cmd_str).read().decode('gb2312')
        process = subprocess.Popen(cmd_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        while process.poll() is None:
            line = process.stdout.readline()
            line = line.strip()
            if line:
                print 'Decompile output: [{}]'.format(line)
        if process.returncode == 0:
            print 'Decompile success'
        else:
            print'Decompile failed'

    def test(self):
        print 'base_dir ' + self._base_dir
        print 'work_dir ' + self._work_dir
        print time.time()
        self.decompile()
        print time.time()

    def _init_config(self):
        self._base_dir = os.path.join(os.getcwd(), "..")
        self._base_dir = os.path.join(self._base_dir, EngineConfig.temp_base_dir)
        self._work_dir = os.path.join(self._base_dir, EngineConfig.temp_work_dir)
        self._android_manifest_file_path = os.path.join(self._work_dir, "AndroidManifest.xml")


    def _fix_file(self):
        # 打开 XML 文档
        dom_tree = xml.dom.minidom.parse(self._android_manifest_file_path)
        self._collection = dom_tree.documentElement
        if self._collection.hasAttribute("package"):
            self._collection.setAttribute("package", self._package_name)
        metas = self._collection.getElementsByTagName("meta-data")
        for meta in metas:
            if meta.hasAttribute("android:name"):
                if meta.getAttribute("android:name") == "ChannelName":
                    meta.setAttribute("android:value", self._channel_name)
                if meta.getAttribute("android:name") == "SubChannelName":
                    meta.setAttribute("android:value", self._sub_channel_name)
                if meta.getAttribute("android:name") == "UmengTag":
                    meta.setAttribute("android:value", self._u_meng_tag)
                if meta.getAttribute("android:name") == "dbclf":
                    meta.setAttribute("android:value", self._debug_level)
                if meta.getAttribute("android:name") == "ClientChId":
                    meta.setAttribute("android:value", self._lebian_clientChId)

    def _write_file(self):
        f = open(self._android_manifest_file_path, "wb+")
        string = "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>"
        string = string.encode('utf-8')
        f.write(string)
        f.write(self._collection.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
        f.close()

    # 准备文件夹，并拷贝相关文件
    def _copy_files(self):
        src_dir = os.path.join(self._base_dir, EngineConfig.temp_ori_decompile_dir)
        if os.path.exists(self._work_dir):
            shutil.rmtree(self._work_dir)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, self._work_dir)
        else:
            return False

    @async
    def _compile(self):
        cmd_str = EngineConfig.cmd_compile_str % (self.output_dir, self._work_dir)
        print os.popen(cmd_str).read().decode('gb2312')
        process = subprocess.Popen(cmd_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        while process.poll() is None:
            line = process.stdout.readline()
            line = line.strip()
            if line:
                print 'Decompile output: [{}]'.format(line)
        if process.returncode == 0:
            print 'Decompile success'
        else:
            print'Decompile failed'

def test():
    bean = ConfigBean.Configuration()
    tool = PackageTool(bean)
    tool.test()


if __name__ == '__main__':
    test()


