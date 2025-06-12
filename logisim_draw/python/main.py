# Logisim Draw

import json
import os
import sys

from helps import 打印帮助信息
from init import 启动
from logisim import Logisim内容
from PIL import Image


# 返回一个字典对象，保存解析出的像素信息
def 解析图像文件(
    图片地址: str,
    offset_x: int = 0,
    offset_y: int = 0,
) -> dict:
    image = Image.open(图片地址)  # 打开图像文件
    image = image.convert("RGB")  # 确保图像是RGB模式
    宽, 高 = image.size  # 获取图像的宽和高

    像素信息 = {
        "offset": {"x": offset_x, "y": offset_y},
        "pixels": [],
    }

    for y in range(高):
        for x in range(宽):
            r, g, b = image.getpixel((x, y))
            color = "#{:02x}{:02x}{:02x}".format(r, g, b)
            像素信息["pixels"].append({"x": x, "y": y, "color": color})

    return 像素信息


# 确认目标 json 文件是否存在，不会创建文件
# 如果文件存在，返回 文件地址，否则返回 空字符串
def 确认目标json文件存在(像素库的文件夹路径: str, 目标circuit名称: str) -> str:
    文件地址 = os.path.join(像素库的文件夹路径, f"{目标circuit名称}.json")
    return 文件地址 if os.path.exists(文件地址) and 文件地址.endswith(".json") else ""


# 确保目标 JSON 文件存在，如果不存在则创建，并返回文件地址
def 确保目标json文件存在(像素库的文件夹路径: str, 目标circuit名称: str) -> str:
    # 确保输出目录存在
    if not os.path.exists(像素库的文件夹路径):
        os.makedirs(像素库的文件夹路径)

    # 确保文件夹路径存在
    if not os.path.isdir(像素库的文件夹路径):
        return None

    # 确保文件地址是一个有效的 JSON 文件路径
    文件地址 = os.path.join(像素库的文件夹路径, f"{目标circuit名称}.json")
    if not 文件地址.endswith(".json"):
        return None

    # 如果文件不存在，则创建一个空文件
    if not os.path.exists(文件地址):
        with open(文件地址, "w", encoding="utf-8") as f:
            f.write("")

    return 文件地址


# 将像素信息保存到 json 文件
# 第一行保存 circuit标签名称
# 第二行保存像素信息
def 保存像素信息到json文件(
    库文件夹路径: str,
    像素信息: dict,
    circuit标签名称: str,
) -> None:

    # 确保输出目录存在
    文件地址 = 确保目标json文件存在(库文件夹路径, circuit标签名称)
    if not 文件地址:
        print(f"错误: 无法创建或确认 {库文件夹路径} 中的 名为 {circuit标签名称}.json 的文件")
        return

    # 写入文件
    with open(文件地址, "w", encoding="utf-8") as f:
        json.dump(像素信息, f, ensure_ascii=False, indent=4)

    print(f"像素信息已保存到 {文件地址}")


# 从指定的 JSON 文件加载像素信息到目标 circ 文件
def 添加像素信息_从库_到circ文件(
    目标circ文件地址: str,
    目标circuit名称: str,
    像素库的文件夹路径: str,
    是否删除原先的像素信息: bool,
) -> None:

    # 确认目标 circ 文件存在
    文件地址 = 确认目标json文件存在(像素库的文件夹路径, 目标circuit名称)
    if not 文件地址:
        print(f"错误: {像素库的文件夹路径} 中未找到 {目标circuit名称}.json 文件")
        return

    # 读取 JSON 文件内容
    with open(文件地址, "r", encoding="utf-8") as f:
        json_content = f.read()

    像素信息: dict = json.loads(json_content)

    # 初始化 Logisim内容对象
    logisim内容 = Logisim内容()
    logisim内容.从文件加载内容(目标circ文件地址)

    # 如果需要删除原有像素信息
    if 是否删除原先的像素信息:
        logisim内容.清除原有像素(目标circuit名称)

    logisim内容.添加新像素(像素信息, 目标circuit名称)
    logisim内容.保存内容到文件(目标circ文件地址)  # 保存到目标 circ 文件

    print(f"已从 {文件地址} 加载像素信息到 {目标circ文件地址} 的 {目标circuit名称} 标签下")

    if 是否删除原先的像素信息:
        print(f"并且已删除 {目标circ文件地址} 中 {目标circuit名称} 标签下的原有像素信息")


# 将指定 circ 文件的指定 circuit 标签下的像素信息存储到指定的 HTML 文件中
def 添加像素信息_从circ文件_到库(
    目标circ文件地址: str,
    目标circuit名称: str,
    像素库的文件夹路径: str,
) -> None:
    print(f"正在将 {目标circuit名称} 标签下的像素信息存储到 {像素库的文件夹路径}")

    # 初始化 Logisim内容对象
    logisim内容 = Logisim内容()
    logisim内容.从文件加载内容(目标circ文件地址)
    像素信息 = logisim内容.获取像素信息(目标circuit名称)

    # 写入文件
    # 会覆盖掉原有的同名文件
    # 确保输出目录存在
    文件地址 = 确保目标json文件存在(像素库的文件夹路径, 目标circuit名称)
    if not 文件地址:
        return

    with open(文件地址, "w", encoding="utf-8") as f:
        json.dump({"circuit_name": 目标circuit名称, "pixels": 像素信息}, f, ensure_ascii=False, indent=4)

    print(f"已将 {目标circuit名称} 标签下的像素信息存储到 {文件地址}")


# 源 circ 文件中去除**所有** circuit 标签下的所有像素，并保存到目标地址
def 去图(目标circ文件地址: str, 源circuit地址: str) -> None:

    print(f"正在从 {源circuit地址} 中去除所有像素信息，并保存到 {目标circ文件地址}")

    # 初始化 Logisim内容对象
    logisim内容 = Logisim内容()
    logisim内容.从文件加载内容(源circuit地址)
    logisim内容.清除所有原有像素()  # 清除所有 circuit 标签下的原有像素
    logisim内容.保存内容到文件(目标circ文件地址)  # 保存到目标 circ 文件

    print(f"已将 {源circuit地址} 中的所有像素信息去除，并保存到 {目标circ文件地址}")


# main
if __name__ == "__main__":

    print("Logisim Draw 像素处理工具")

    启 = 启动()
    启.解析参数(sys.argv[1:])

    模式: str = 启.是否可以启动模式()

    if 模式 == "False":
        print("启动失败，请检查参数是否正确")
        打印帮助信息()
        sys.exit(1)

    elif 模式 == "del":
        logisim内容 = Logisim内容()
        logisim内容.从文件加载内容(启.目标)
        logisim内容.清除原有像素(启.circuit名称)
        logisim内容.保存内容到文件(启.目标)

    elif 模式 == "add":
        logisim内容 = Logisim内容()
        logisim内容.从文件加载内容(启.目标)

        if 启.是否删除原先的像素信息:
            logisim内容.清除原有像素(启.circuit名称)

        像素信息 = 解析图像文件(启.源)
        logisim内容.添加新像素(启.circuit名称, 像素信息)
        logisim内容.保存内容到文件(启.目标)

    elif 模式 == "conv":
        像素信息 = 解析图像文件(启.源)
        保存像素信息到json文件(
            启.目标,
            像素信息,
            启.circuit名称,
        )

    elif 模式 == "load":
        添加像素信息_从库_到circ文件(
            启.目标,  # 目标 circ 文件地址
            启.circuit名称,
            启.源,  # 像素库的文件夹路径
            启.是否删除原先的像素信息,
        )

    elif 模式 == "store":
        添加像素信息_从circ文件_到库(
            启.源,
            启.circuit名称,
            启.目标,
        )

    elif 模式 == "去图":
        去图(启.目标, 启.源)

    print("程序结束")
