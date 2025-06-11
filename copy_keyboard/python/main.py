# 模拟键盘输入

import sys
from time import sleep

import pyautogui

if __name__ == "__main__":

    # 获取参数列表
    path = sys.argv[1]

    text = ""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    sleep(1)
    pyautogui.click()  # 点击一下窗口，确保输入焦点在当前窗口
    pyautogui.write(text, interval=0.005)  # 输入文本
