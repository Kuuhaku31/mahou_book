# password.py

import subprocess
import time

输出目录 = "output_directory"


# 利用 7zip 解压 RAR 文件
def extract_rar_with_7zip(文件地址, 解压密码):
    # 调用 7z 命令解压 RAR 文件，并自动确认所有提示
    指令 = ["7z", "t", f"-p{解压密码}", 文件地址]  # 使用 "t" 测试密码是否正确
    result = subprocess.run(指令, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        # 密码正确，解压文件
        指令 = ["7z", "x", "-y", f"-p{解压密码}", 文件地址, f"-o{输出目录}"]
        subprocess.run(指令, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    else:
        return False


# 使用示例
文件地址 = "./（已校对）Python核心编程 第3版 (卫斯理·春,Wesley Chun).rar"
密码 = "your_password"  # 如果没有密码，可以设为None

start_time = time.time()  # 记录开始时间
循环次数 = 99999999
while not extract_rar_with_7zip(文件地址, str(循环次数)):
    if 循环次数 % 1000 == 0:
        print(f"尝试密码: {str(循环次数)}")
        print(f"目前耗时: {time.time() - start_time:.2f} 秒")
    循环次数 -= 1
end_time = time.time()  # 记录结束时间

print(f"密码是: {str(循环次数)}")
print(f"解压完成，耗时: {end_time - start_time:.2f} 秒")
