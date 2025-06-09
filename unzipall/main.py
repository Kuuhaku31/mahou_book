# 批量解压当前目录下的所有压缩文件
# 利用7zip.exe解压缩

import os
import subprocess

EXE7zip路径 = "E:/Program Files/7-Zip/7z.exe"
支持解压的格式列表 = [
    ".zip",
    ".rar",
    ".7z",
]


当前工作路径 = os.getcwd()
print("当前工作路径: ", 当前工作路径)


# 获取当前目录下的所有压缩文件
所有压缩文件 = []
for 文件或文件夹 in os.listdir(当前工作路径):
    # 判断是否是文件
    if os.path.isfile(文件或文件夹):
        # 判断是否是压缩文件
        for 格式 in 支持解压的格式列表:
            if 文件或文件夹.endswith(格式):
                所有压缩文件.append(文件或文件夹)
                break


# 打印所有压缩文件
print("当前目录下的所有压缩文件:")
for 压缩文件 in 所有压缩文件:
    print(压缩文件)


# 解压缩所有压缩文件
for 压缩文件 in 所有压缩文件:
    # 获取文件名和扩展名
    # 创建解压缩后的文件夹
    文件名, 扩展名 = os.path.splitext(压缩文件)
    解压缩后的文件夹 = os.path.join(当前工作路径, 文件名)
    if not os.path.exists(解压缩后的文件夹):
        os.makedirs(解压缩后的文件夹)

    # 解压缩
    print(f"正在解压缩 {压缩文件} 到 {解压缩后的文件夹}...")
    # 关闭shell输
    subprocess.run(
        [EXE7zip路径, "x", 压缩文件, f"-o{解压缩后的文件夹}", "-y"],
        stdout=subprocess.DEVNULL,  # 关闭标准输出
        stderr=subprocess.DEVNULL,  # 关闭标准错误输出
    )
