# shutdown.py

import os
import sys
import time

# 获取用户输入的关机延迟时间（秒）

delay = sys.argv[1] if len(sys.argv) > 1 else "60"


print(f"系统将在 {delay} 秒后关机...")
time.sleep(int(delay))

# 执行关机命令（Windows）
os.system("shutdown /s /t 0")
