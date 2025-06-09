# 控制鼠标


import ctypes
import time

import keyboard

# 鼠标事件常量
MOUSEEVENTF_MOVE = 0x0001  # 鼠标移动
MOUSEEVENTF_LEFTDOWN = 0x0002  # 鼠标左键按下
MOUSEEVENTF_LEFTUP = 0x0004  # 鼠标左键抬起
MOUSEEVENTF_ABSOLUTE = 0x8000  # 绝对坐标


# 模拟鼠标移动（绝对坐标，0~65535）
def move_to(x, y):
    ctypes.windll.user32.mouse_event(
        MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        int(x * 65535 / ctypes.windll.user32.GetSystemMetrics(0)),
        int(y * 65535 / ctypes.windll.user32.GetSystemMetrics(1)),
        0,
        0,
    )


# 模拟鼠标点击（左键）
def click_mouse():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def mouse_drag(start, end, duration=1.0):
    move_to(*start)
    time.sleep(0.1)

    # 按下左键
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)

    # 拖动（线性插值模拟平滑拖动）
    steps = 30
    for i in range(1, steps + 1):
        x = start[0] + (end[0] - start[0]) * i / steps
        y = start[1] + (end[1] - start[1]) * i / steps
        move_to(x, y)
        time.sleep(duration / steps)

    # 松开左键
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 使用示例
is_continue = True


def on_key(event):
    if event.name == "esc":
        global is_continue
        is_continue = False
        print(f"你按下了：{event.name}")
        print("退出程序")


# 开始监听
keyboard.on_press(on_key)

while is_continue:
    click_mouse()
    time.sleep(1.75)
