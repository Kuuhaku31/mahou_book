# unrar_test.py

import rarfile

# 设置RAR文件路径和密码
rar_path = "D:/tools/password/def.rar"
password = "141592"

# 打开RAR文件
with rarfile.RarFile(rar_path) as rf:
    # 设置密码
    rf.setpassword(password)

    # 解压所有文件到指定目录
    rf.extractall(path="extracted_files")
