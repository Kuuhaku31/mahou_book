import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

found = False


# 利用 7zip 解压 RAR 文件
def extract_rar_with_7zip(解压密码):
    global found

    if found:
        return

    文件地址 = "./target.rar"

    # 调用 7z 命令解压 RAR 文件，并自动确认所有提示
    # 7z t -p"141592" "./def.rar"
    result = subprocess.run(
        f'7z t -p"{str(解压密码).zfill(8)}" "{文件地址}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode == 0:
        found = True
        print(f"密码是: {解压密码}")


# 使用示例
start_time = time.time()  # 记录开始时间
with ThreadPoolExecutor(max_workers=16) as executor:

    # 密码范围: 0 到 99441000
    for current_password in range(79900000, 100000000):
        if found:
            break

        # 提交任务到线程池
        executor.submit(extract_rar_with_7zip, current_password)

        if current_password % 100000 == 0:
            print(
                f"\r尝试密码到: {str(current_password).zfill(8)} 目前耗时: {time.time() - start_time:.2f} 秒",
                end="",
            )

end_time = time.time()  # 记录结束时间

print()
print(f"目前尝试密码到: {str(current_password).zfill(8)} 耗时: {end_time - start_time:.2f} 秒")

# cd D:\tools\password\ ; python password2.py
# 尝试密码: 99441000
# 目前耗时: 9021.33 秒
# 16.14 秒/1000 次

# 00000000
# 21200000
# 32100000
# 尝试密码: 49900000 目前耗时: 200.56 秒
# 尝试密码到: 59900000 目前耗时: 105.09 秒
# 尝试密码到: 69900000 目前耗时: 103.36 秒
# 尝试密码到: 79900000 目前耗时: 100.18 秒
# 尝试密码到: 99900000 目前耗时: 213.27 秒
