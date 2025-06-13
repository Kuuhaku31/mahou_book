# logisim.py

import xml.etree.ElementTree as ET
from math import inf


# 成员变量：
# - 内容：存储 circ 文件的内容
#
# 成员函数：
# - 从文件加载内容：从指定文件加载 circ 文件内容
# - 保存到文件：将内容保存到指定文件
# - 清除原有像素：删除指定 circuit 标签下的所有 height="1" 且 width="1" 的 <rect> 标签
# - 添加新像素：将新像素添加到指定 circuit 标签下的 <appear> 标签中
# - 获取像素信息：获取指定 circuit 标签下的 <appear> 标签中的像素信息
class Logisim内容:
    def __init__(己):
        己.HTML根: ET.Element = None  # 初始化内容为 None
        己.文件路径: str = None

    def __格式打印(己, 打印内容: str, 打印颜色: str = "default") -> None:

        前: str = ""
        后: str = ""

        if 打印颜色 == "red":
            前 = "\033[31m"
            后 = "\033[0m"
        elif 打印颜色 == "green":
            前 = "\033[32m"
            后 = "\033[0m"
        elif 打印颜色 == "yellow":
            前 = "\033[33m"
            后 = "\033[0m"

        print(f"\033[34mLogisim内容在处理[{己.文件路径}]:\033[0m {前}{打印内容}{后}")

    def __终止程序(己, 错误信息: str) -> None:
        # 用红色字体打印
        print(f"\033[31mLogisim内容在处理[{己.文件路径}]: 终止程序 错误信息: {错误信息}\033[0m")
        exit(1)

    def 从文件加载内容(己, 文件路径: str) -> None:
        try:
            tree = ET.parse(文件路径)
            己.HTML根 = tree.getroot()
            己.文件路径 = 文件路径

            己.__格式打印(f"已成功加载文件 {文件路径}", "green")

        except FileNotFoundError:
            己.__终止程序(f"文件 {文件路径} 未找到")
        except Exception as e:
            己.__终止程序(f"加载文件时发生错误: {e}")

    def 保存内容到文件(己, 文件路径: str) -> None:
        try:
            tree = ET.ElementTree(己.HTML根)
            tree.write(文件路径, encoding="utf-8", xml_declaration=True)
            己.__格式打印("内容已保存到文件: " + 文件路径, "green")

        except Exception as e:
            己.__终止程序(f"保存文件时发生错误: {e}")

    # 函数逻辑：
    # 遍历 <appear> 标签下的所有标签
    # 仅删除 height="1" 且 width="1" 的 <rect> 标签
    def 清除原有像素(己, 目标circuit名称: str) -> None:
        for c in 己.HTML根.findall(".//circuit"):
            if c.attrib.get("name") == 目标circuit名称:
                appear = c.find("appear")
                if appear is not None:
                    rect_list = list(appear.findall("rect"))
                    for rect in rect_list:
                        if rect.attrib.get("width") == "1" and rect.attrib.get("height") == "1":
                            appear.remove(rect)
        己.__格式打印(f"已删除[{目标circuit名称}]标签下的所有像素", "green")

    # 清除所有circuit下的像素
    def 清除所有原有像素(己) -> None:
        for c in 己.HTML根.findall(".//circuit"):
            appear = c.find("appear")
            if appear is not None:
                rect_list = list(appear.findall("rect"))
                for rect in rect_list:
                    if rect.attrib.get("width") == "1" and rect.attrib.get("height") == "1":
                        appear.remove(rect)
        己.__格式打印("已删除所有标签下的所有像素", "green")

    # 添加新像素到指定circuit
    def 添加新像素(己, 像素信息: dict, 目标circuit名称: str, 像素偏移向量: tuple[int, int] = None) -> None:

        像素数量 = len(像素信息["pixels"]) if 像素信息 and "pixels" in 像素信息 else 0

        # 用醒目的颜色打印警告信息
        # 并要求用户输入 y 确认
        if 像素数量 > 90000:
            己.__格式打印("警告: 添加的像素数量超过 90000 个，这可能会导致 Logisim 无法正常工作。", "yellow")
            确认 = input("  是否继续添加？(y/n): ")
            if 确认.lower() != "y":
                己.__格式打印("已取消本次添加像素操作", "yellow")
                return

        # 确认像素信息合法性
        if 像素信息 is None or not isinstance(像素信息, dict):
            己.__格式打印("像素信息格式不正确", "yellow")
            return
        if "pixels" not in 像素信息 or not isinstance(像素信息["pixels"], list):
            己.__格式打印("像素信息格式不正确或缺少 'pixels' 键", "yellow")
            return
        if "offset" not in 像素信息:
            像素信息["offset"] = {"x": 0, "y": 0}
            己.__格式打印("像素信息中缺少 'offset' 键，已自动添加默认值: (0, 0)", "yellow")

        for c in 己.HTML根.findall(".//circuit"):
            if c.attrib.get("name") == 目标circuit名称:
                appear = c.find("appear")
                if appear is None:
                    appear = ET.SubElement(c, "appear")
                for pixel in 像素信息["pixels"]:
                    if 像素偏移向量:
                        x = pixel["x"] + 像素偏移向量[0]
                        y = pixel["y"] + 像素偏移向量[1]
                    else:
                        x = pixel["x"] + 像素信息["offset"]["x"]
                        y = pixel["y"] + 像素信息["offset"]["y"]
                    color = pixel["color"]
                    ET.SubElement(
                        appear,
                        "rect",
                        {
                            "x": str(x),
                            "y": str(y),
                            "width": "1",
                            "height": "1",
                            "fill": color,
                        },
                    )

        己.__格式打印(f"已向 {目标circuit名称} 添加 {像素数量} 个像素", "green")

    # 获取 内容 中指定 circuit 标签下的像素信息
    def 获取像素信息(己, 目标circuit名称: str) -> dict:

        # 找到目标 circuit
        circuit = None
        for c in 己.HTML根.findall(".//circuit"):
            if c.attrib.get("name") == 目标circuit名称:
                circuit = c
                break

        if circuit is None:
            己.__格式打印(f"未找到指定circuit: {目标circuit名称}", "yellow")
            return None

        # 找到 appear 标签
        appear = circuit.find("appear")
        if appear is None:
            己.__格式打印(f"未找到 {目标circuit名称} 的 appear 标签", "yellow")
            return None

        # 提取所有 width="1" height="1" 的 rect
        pixels = []
        min_x = inf
        min_y = inf
        for rect in appear.findall("rect"):
            if rect.attrib.get("width") == "1" and rect.attrib.get("height") == "1":
                x = int(rect.attrib.get("x", 0))
                y = int(rect.attrib.get("y", 0))
                color = rect.attrib.get("fill", "#000000")
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                pixels.append({"x": x, "y": y, "color": color})

        # 偏移归零
        for p in pixels:
            p["x"] -= min_x
            p["y"] -= min_y

        # 如果没有找到任何像素，返回 None
        if not pixels:
            己.__格式打印(f"{目标circuit名称} 中未找到任何像素", "yellow")
            return None
        else:
            己.__格式打印(f"已找到 {目标circuit名称} 中 {len(pixels)} 个像素", "green")
            return {"offset": {"x": min_x, "y": min_y}, "pixels": pixels}

    # 获取 内容 中所有 circuit 标签名称
    def 获取所有circuit标签名称(己) -> list[str]:
        res = [c.attrib.get("name") for c in 己.HTML根.findall(".//circuit") if c.attrib.get("name")]

        己.__格式打印(f"已找到 {len(res)} 个 circuit 标签名称: {', '.join(res)}", "green")
        return res
