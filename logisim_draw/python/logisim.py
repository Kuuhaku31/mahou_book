# logisim.py

import re
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
    def __init__(self):
        self.内容 = ""

    def 从文件加载内容(self, 文件路径: str) -> None:
        """从指定文件加载内容"""
        try:
            with open(文件路径, "r", encoding="utf-8") as f:
                self.内容 = f.read()
        except FileNotFoundError:
            print(f"文件 {文件路径} 未找到")
        except Exception as e:
            print(f"加载文件时发生错误: {e}")

    def 保存内容到文件(self, 文件路径: str) -> None:
        """将内容保存到指定文件"""
        try:
            with open(文件路径, "w", encoding="utf-8") as f:
                f.write(self.内容)
        except Exception as e:
            print(f"保存文件时发生错误: {e}")

    # 函数逻辑：
    # 遍历 <appear> 标签下的所有标签
    # 仅删除 height="1" 且 width="1" 的 <rect> 标签
    def 清除原有像素(self, 目标circuit名称: str) -> None:

        # 找到指定circuit下的<appear>...</appear>
        pattern = rf'(<circuit\s+name="{re.escape(目标circuit名称)}"[^>]*>.*?<appear>)(.*?)(</appear>)'
        match = re.search(pattern, self.内容, flags=re.DOTALL)
        if not match:
            print("未找到指定circuit或appear标签")
            return

        appear_content = match.group(2)

        # 删除 height="1" 且 width="1" 的 <rect> 标签
        appear_content = re.sub(r'<rect[^>]*height="1"[^>]*width="1"[^>]*\/>', "", appear_content)

        # 替换 appear 内容
        self.内容 = re.sub(pattern, rf"\1\n{appear_content}\3", self.内容, flags=re.DOTALL)

    # 清除所有 circuit 标签下的原有像素
    def 清除所有原有像素(self) -> None:
        # 获取所有 circuit 标签名称
        circuit_names = self.获取所有circuit标签名称()
        for circuit_name in circuit_names:
            self.清除原有像素(circuit_name)

    # 添加新像素到指定的circuit标签下的<appear>标签中
    def 添加新像素(self, 像素信息: dict, 目标circuit名称: str, 像素偏移向量: tuple[int, int]) -> None:

        # 遍历像素列表，生成 <rect> 标签
        新内容 = ""
        for pixel in 像素信息["pixels"]:

            # 计算 x 和 y 坐标
            # 如果提供了像素偏移向量，则使用它
            # 否则使用像素信息中的偏移量
            if 像素偏移向量:
                x = pixel["x"] + 像素偏移向量[0]
                y = pixel["y"] + 像素偏移向量[1]
            else:
                x = pixel["x"] + 像素信息["offset"]["x"]
                y = pixel["y"] + 像素信息["offset"]["y"]

            color = pixel["color"]

            # 生成 <rect> 标签
            新内容 += f'<rect x="{x}" y="{y}" width="1" height="1" fill="{color}" />\n'

        # 找到指定circuit下的<appear>...</appear>
        pattern = rf'(<circuit\s+name="{re.escape(目标circuit名称)}"[^>]*>.*?<appear>)(.*?)(</appear>)'
        match = re.search(pattern, self.内容, flags=re.DOTALL)
        if not match:
            print("未找到指定circuit或appear标签")
            return

        appear_content = match.group(2)

        # 在 appear_content 中添加新内容
        appear_content += 新内容

        # 替换 appear 内容
        self.内容 = re.sub(pattern, rf"\1\n{appear_content}\3", self.内容, flags=re.DOTALL)

    # 获取 内容 中指定 circuit 标签下的像素信息
    def 获取像素信息(self, 目标circuit名称: str) -> dict:
        # 找到指定circuit下的<appear>...</appear>
        pattern = rf'(<circuit\s+name="{re.escape(目标circuit名称)}"[^>]*>.*?<appear>)(.*?)(</appear>)'
        match = re.search(pattern, self.内容, flags=re.DOTALL)
        if not match:
            print(f"未找到指定circuit: {目标circuit名称} 或 appear 标签")
            return None

        appear_content = match.group(2)

        # 使用正则表达式匹配所有 <rect> 标签的 x, y 和 fill 属性
        # 注意：这里假设所有 <rect> 标签都是 height="1" 且 width="1"
        # <rect fill="#ffffff" height="65" stroke="#000000" stroke-width="2" width="88" x="90" y="112" />
        src_pixels = re.findall(
            r'<rect\b(?=[^>]*\bx="(\d+)")(?=[^>]*\by="(\d+)")(?=[^>]*\bwidth="1")(?=[^>]*\bheight="1")(?=[^>]*\bfill="([^"]+)")[^>]*\/>',
            appear_content,
        )

        像素信息: dict = {
            "offset": {"x": 0, "y": 0},  # 假设偏移量为 (0, 0)，可以根据需要修改
            "pixels": [],
        }

        # 将像素信息存入字典 pixels

        # 先获取偏移向量
        min_x: int = inf
        min_y: int = inf
        for pixel in src_pixels:
            x, y, color = pixel
            min_x = min(min_x, int(x))
            min_y = min(min_y, int(y))

        for pixel in src_pixels:
            x, y, color = pixel
            dst_pixels: list = 像素信息["pixels"]
            dst_pixels.append({"x": int(x) - min_x, "y": int(y) - min_y, "color": color})

        # 将 offset 设置为所有像素的最小 x 和 y 坐标
        像素信息["offset"] = {"x": min_x, "y": min_y}

        return 像素信息

    # 获取 内容 中所有 circuit 标签名称
    def 获取所有circuit标签名称(self) -> list:
        # 使用正则表达式匹配所有 <circuit name="..."> 标签
        pattern = r'<circuit\s+name="([^"]+)"'
        matches = re.findall(pattern, self.内容)
        return matches  # 返回所有匹配到的 circuit 名称列表
