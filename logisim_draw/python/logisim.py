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

    def 从文件加载内容(己, 文件路径: str) -> None:
        try:
            print(f"正在加载文件 {文件路径}...")

            tree = ET.parse(文件路径)
            己.HTML根 = tree.getroot()
            print(f"已成功加载文件 {文件路径}")

        except FileNotFoundError:
            print(f"文件 {文件路径} 未找到")
        except Exception as e:
            print(f"加载文件时发生错误: {e}")

    def 保存内容到文件(己, 文件路径: str) -> None:
        try:
            print(f"正在保存内容到 {文件路径}...")
            tree = ET.ElementTree(己.HTML根)
            tree.write(文件路径, encoding="utf-8", xml_declaration=True)
            print(f"内容已保存到 {文件路径}")

        except Exception as e:
            print(f"保存文件时发生错误: {e}")

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

    # 清除所有circuit下的像素
    def 清除所有原有像素(己) -> None:
        for c in 己.HTML根.findall(".//circuit"):
            appear = c.find("appear")
            if appear is not None:
                rect_list = list(appear.findall("rect"))
                for rect in rect_list:
                    if rect.attrib.get("width") == "1" and rect.attrib.get("height") == "1":
                        appear.remove(rect)

    # 添加新像素到指定circuit
    def 添加新像素(己, 像素信息: dict, 目标circuit名称: str, 像素偏移向量: tuple[int, int] = None) -> None:

        if 像素信息 is not None:
            print(f"正在向 {目标circuit名称} 添加 {len(像素信息['pixels'])} 个像素")
        else:
            print("像素信息是 None")

        # 确认像素信息合法性
        if 像素信息 is None or not isinstance(像素信息, dict):
            print("错误: 像素信息格式不正确")
            return
        if "pixels" not in 像素信息 or not isinstance(像素信息["pixels"], list):
            print("错误: 像素信息格式不正确或缺少 'pixels' 键")
            return
        if "offset" not in 像素信息:
            像素信息["offset"] = {"x": 0, "y": 0}

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

        print(f"已向 {目标circuit名称} 添加 {len(像素信息['pixels'])} 个像素")

    # 获取 内容 中指定 circuit 标签下的像素信息
    def 获取像素信息(己, 目标circuit名称: str) -> dict:

        # 找到目标 circuit
        circuit = None
        for c in 己.HTML根.findall(".//circuit"):
            if c.attrib.get("name") == 目标circuit名称:
                circuit = c
                break
        if circuit is None:
            print(f"未找到指定circuit: {目标circuit名称}")
            return None

        # 找到 appear 标签
        appear = circuit.find("appear")
        if appear is None:
            print(f"未找到 {目标circuit名称} 的 appear 标签")
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
            print(f"{目标circuit名称} 中未找到任何像素")
            return None
        else:
            return {"offset": {"x": min_x, "y": min_y}, "pixels": pixels}

    # 获取 内容 中所有 circuit 标签名称
    def 获取所有circuit标签名称(己) -> list:
        return [c.attrib.get("name") for c in 己.HTML根.findall(".//circuit") if c.attrib.get("name")]
