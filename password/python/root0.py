import subprocess
import sys
import time

密码位数 = 8
密码 = None
找到密码 = False


# 保存日志
def saveLog(尝试密码的范围, 目前耗时):
    with open("log.txt", "a") as f:
        f.write(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"尝试密码范围: {str(尝试密码的范围[0]).zfill(密码位数)} 到 {str(尝试密码的范围[1]).zfill(密码位数)} 之前 "
            f"耗时: {目前耗时:.2f} 秒 "
            f"是否找到密码: {f'{密码}' if 找到密码 else '否'}\n"
        )


# 利用 7zip 解压 RAR 文件
def extract_rar_with_7zip(解压密码):
    global 密码
    global 找到密码

    文件地址 = "./target.rar"

    # 调用 7z 命令解压 RAR 文件，并自动确认所有提示
    # 7z t -p"141592" "./def.rar"
    指令 = f'7z t -p"{str(解压密码).zfill(密码位数)}" "{文件地址}"'
    result = subprocess.run(指令, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"\n密码是: {str(解压密码).zfill(密码位数)}")
        密码 = str(解压密码).zfill(密码位数)
        找到密码 = True


# f"尝试密码范围: {str(尝试密码的范围[0]).zfill(密码位数)} 到 {str(尝试密码的范围[1]).zfill(密码位数)} 之前 "
print(f"开始尝试密码范围: {sys.argv[1]} 到 {sys.argv[2]} 之前")

开始时间 = time.time()  # 记录开始时间
for i in range(int(sys.argv[1]), int(sys.argv[2])):
    print(f"\r尝试密码到: {str(i).zfill(密码位数)} 目前耗时: {time.time() - 开始时间:.2f} 秒", end="")
    extract_rar_with_7zip(i)
    if 找到密码:
        break


saveLog((int(sys.argv[1]), int(sys.argv[2])), time.time() - 开始时间)

if not 找到密码:
    print(f"\n在范围 {sys.argv[1]} 到 {sys.argv[2]} 之前中没有找到密码")

# cd D:\tools\password\ ; python root0.py 10000 20000

# 在范围 00000000 到 00100000 中没有找到密码
#  100000 到 1000000 之前
#  1002000 到 2000000 之前
#  2000000 到 3_000_000 之前
# 尝试密码范围: 01000000 到 01001000 耗时: 18.82 秒 是否找到密码: 否
# [2025-04-27 20:53:55] 尝试密码范围: 01001000 到 01002000 耗时: 19.12 秒 是否找到密码: 否尝试密码到: 00130000 目前耗时: 621.15 秒
# 尝试密码到: 00100000 目前耗时: 0.00 秒
# 尝试密码到: 00110000 目前耗时: 208.60 秒
# 尝试密码到: 00120000 目前耗时: 415.05 秒
# 尝试密码到: 00140000 目前耗时: 816.15 秒
# 尝试密码到: 00150000 目前耗时: 1011.07 秒
# 尝试密码到: 00160000 目前耗时: 1205.14 秒
# 尝试密码到: 00170000 目前耗时: 1402.52 秒
# 尝试密码到: 00180000 目前耗时: 1600.54 秒
# 尝试密码到: 00190000 目前耗时: 1798.06 秒
# 尝试密码到: 00200000 目前耗时: 2007.04 秒
# 尝试密码到: 00210000 目前耗时: 2233.72 秒
# 尝试密码到: 00220000 目前耗时: 2455.11 秒
# 尝试密码到: 00230000 目前耗时: 2679.61 秒
# 尝试密码到: 00240000 目前耗时: 2902.75 秒
