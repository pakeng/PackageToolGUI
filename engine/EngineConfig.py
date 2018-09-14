# -*- coding: UTF-8 -*-

temp_base_dir = ".temp_dir"  # 工作临时文件夹
temp_ori_decompile_dir = "ori_decompile_dir"  # 解包出来的原始文件
temp_work_dir = "work_copy_dir"  # 工作的临时文件夹，拷贝的原始文件副本。打包的时候不用删除然后从 ori文件夹拷贝免去解包

cmd_decompile_str = "apktool.bat d -f -o %s %s "
cmd_compile_str = "apktool.bat b -f -o %s %s "