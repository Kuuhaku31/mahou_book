import subprocess
import time
from concurrent.futures import ThreadPoolExecutor


# 利用 7zip 解压 RAR 文件
def extract_rar_with_7zip(解压密码):

    if 解压密码 == 141592:
        print(解压密码)
        return

    密码位数 = 6
    文件地址 = "./def.rar"

    # 调用 7z 命令解压 RAR 文件，并自动确认所有提示
    # 7z t -p"141592" "./def.rar"
    指令 = f'7z t -p"{str(解压密码).zfill(密码位数)}" "{文件地址}"'
    result = subprocess.run(指令, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"\n密码是: {str(解压密码).zfill(密码位数)}")


# 使用示例
start_time = time.time()  # 记录开始时间
with ThreadPoolExecutor(max_workers=32) as executor:

    # 密码范围:
    for current_password in range(10_00_00, 1_00_00_00):
        # 提交任务到线程池
        executor.submit(extract_rar_with_7zip, current_password)

        if current_password % 100000 == 0:
            print(
                f"尝试密码到: {str(current_password).zfill(6)} 目前耗时: {time.time() - start_time:.2f} 秒",
            )

    print(f"\n尝试密码到: {str(current_password).zfill(6)} 目前耗时: {time.time() - start_time:.2f} 秒")


# cd D:\tools\password\ ; python test.py

# 141592
